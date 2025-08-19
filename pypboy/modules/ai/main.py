import pygame
import config
import pypboy.modules
import threading # <-- Import threading for background AI processing
from .vince_prompt import SYSTEM_PROMPT

# --- MODIFICATION: Attempt to import the AI library ---
try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False


class Module(pypboy.modules.SubModule):
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        
        self.chat_history = []
        self.input_text = ""
        self.input_active = True
        self.processing_query = False # Flag to prevent multiple submissions

        # Add initial welcome message from V.I.N.C.E.
        self.add_message("V.I.N.C.E.", "V.I.N.C.E. online. Awaiting your command, Operator.")
        
        self.redraw_display()

    def add_message(self, sender, text):
        """Adds a message to the chat history."""
        self.chat_history.append(f"{sender}: {text}")
        if len(self.chat_history) > 10: # Keep history shorter for the prompt
            self.chat_history.pop(0)
        self.redraw_display()

    def redraw_display(self):
        """Redraws the entire AI interface."""
        self.image.fill((0, 0, 0))

        # Title
        title_text = "V.I.N.C.E. INTERFACE"
        title_render = config.FONT_LRG.render(title_text, True, config.TINTCOLOUR)
        title_pos = ((self.image.get_width() - title_render.get_width()) // 2, 20)
        self.image.blit(title_render, title_pos)

        # Chat History Area
        chat_box_rect = pygame.Rect(40, 70, config.WIDTH - 80, config.HEIGHT - 220)
        pygame.draw.rect(self.image, config.TINTCOLOUR, chat_box_rect, 1)
        
        # Render chat history
        line_y = chat_box_rect.y + 10
        for line in self.chat_history:
            words = line.split(' ')
            line_render = ""
            for word in words:
                test_line = line_render + word + " "
                if config.FONT_MED.size(test_line)[0] > chat_box_rect.width - 20:
                    text_surface = config.FONT_MED.render(line_render, True, config.TINTCOLOUR)
                    self.image.blit(text_surface, (chat_box_rect.x + 10, line_y))
                    line_y += config.FONT_MED.get_linesize()
                    line_render = word + " "
                else:
                    line_render = test_line
            
            text_surface = config.FONT_MED.render(line_render, True, config.TINTCOLOUR)
            self.image.blit(text_surface, (chat_box_rect.x + 10, line_y))
            line_y += config.FONT_MED.get_linesize()

        # Text Input Box
        input_box_rect = pygame.Rect(40, config.HEIGHT - 140, config.WIDTH - 80, 50)
        pygame.draw.rect(self.image, config.TINTCOLOUR, input_box_rect, 1)

        # Display the text the user is typing or a processing message
        display_text = "> " + self.input_text
        if self.processing_query:
            display_text = "V.I.N.C.E. is processing your request..."

        input_render = config.FONT_MED.render(display_text, True, config.TINTCOLOUR)
        self.image.blit(input_render, (input_box_rect.x + 10, input_box_rect.y + 10))

        # Blinking cursor
        if self.input_active and not self.processing_query and pygame.time.get_ticks() % 1000 < 500:
            cursor_pos_x = input_box_rect.x + 10 + config.FONT_MED.size("> " + self.input_text)[0]
            cursor_pos_y1 = input_box_rect.y + 12
            cursor_pos_y2 = cursor_pos_y1 + config.FONT_MED.get_height()
            pygame.draw.line(self.image, config.TINTCOLOUR, (cursor_pos_x, cursor_pos_y1), (cursor_pos_x, cursor_pos_y2), 2)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.input_active and not self.processing_query:
            if event.key == pygame.K_RETURN:
                self.submit_query()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode
            self.redraw_display()

    def submit_query(self):
        if not self.input_text.strip() or self.processing_query:
            return
            
        query = self.input_text
        self.add_message("Operator", query)
        self.input_text = ""
        self.processing_query = True
        self.redraw_display()

        # --- MODIFICATION: Start AI inference in a background thread ---
        threading.Thread(target=self.ask_vince_threaded, args=(query,)).start()

    def ask_vince_threaded(self, query):
        """Constructs the prompt and calls the LLM in a separate thread."""
        llm = self.pypboy.llm
        if not llm or not LLAMA_CPP_AVAILABLE:
            response_text = "AI core offline. Check model configuration and dependencies."
        else:
            try:
                # Construct the full prompt
                history_str = "\n".join(self.chat_history)
                full_prompt = f"{SYSTEM_PROMPT}\n\n== Chat History ==\n{history_str}\n\nOperator: {query}\nV.I.N.C.E.:"
                
                # Get the AI's response
                output = llm(full_prompt, max_tokens=256, stop=["Operator:", "\n"], echo=False)
                response_text = output['choices'][0]['text'].strip()
            except Exception as e:
                print(f"Error during AI inference: {e}")
                response_text = f"Computational error detected in positronic brain. Details: {e}"
        
        # Add the response and re-enable input
        self.add_message("V.I.N.C.E.", response_text)
        self.processing_query = False
        self.redraw_display()

    def update(self, *args, **kwargs):
        self.redraw_display()
        super(Module, self).update(*args, **kwargs)

    def handle_resume(self):
        self.parent.pypboy.header.headline = "V.I.N.C.E."
        self.parent.pypboy.header.title = ["VAULT-TEC INTEGRATED NETWORK & COMPUTATION ENGINE"]
        super(Module, self).handle_resume()
