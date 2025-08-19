import pygame
import config
import pypboy.modules

class Module(pypboy.modules.SubModule):
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        
        self.image = pygame.Surface((config.WIDTH, config.HEIGHT - 80))
        self.image.fill((0, 0, 0))

        # --- MODIFICATION: Define Navigation Buttons ---
        self.buttons = []
        self.button_rects = []
        self.selected_button = 0
        
        # Define the modules we want buttons for
        self.nav_modules = ["HOME", "STATS", "ITEMS", "DATA", "AI"]
        
        self.create_buttons()
        self.draw_buttons()

    def create_buttons(self):
        """Create the button labels and positions."""
        button_y_start = 200
        button_spacing = 80
        for i, label in enumerate(self.nav_modules):
            # Create a render for the text
            text_render = config.FONT_LRG.render(label, True, config.TINTCOLOUR)
            
            # Center the button horizontally
            pos_x = (self.image.get_width() - text_render.get_width()) // 2
            pos_y = button_y_start + (i * button_spacing)
            
            # Create a rectangle for click detection
            rect = text_render.get_rect(topleft=(pos_x, pos_y))
            
            self.buttons.append({'label': label, 'render': text_render, 'pos': (pos_x, pos_y)})
            self.button_rects.append(rect)

    def draw_buttons(self):
        """Draw the buttons and the selector onto the surface."""
        self.image.fill((0, 0, 0)) # Clear the screen first

        # Redraw title
        title_text = "PYPBOY 5000 MAIN MENU"
        title_render = config.FONT_LRG.render(title_text, True, config.TINTCOLOUR)
        title_pos = ((self.image.get_width() - title_render.get_width()) // 2, 40)
        self.image.blit(title_render, title_pos)

        # Draw each button label
        for button in self.buttons:
            self.image.blit(button['render'], button['pos'])
            
        # Draw the selector bracket around the selected button
        selected_rect = self.button_rects[self.selected_button]
        selector_pos_left = (selected_rect.left - 20, selected_rect.centery)
        selector_pos_right = (selected_rect.right + 20, selected_rect.centery)
        
        # Simple text-based brackets for the selector
        bracket_render = config.FONT_LRG.render("[    ]", True, config.TINTCOLOUR)
        bracket_rect = bracket_render.get_rect(center=selected_rect.center)
        # A little hacky, but resize the bracket render to fit the text
        bracket_scaled = pygame.transform.scale(bracket_render, (selected_rect.width + 20, selected_rect.height + 10))
        bracket_scaled_rect = bracket_scaled.get_rect(center=selected_rect.center)

        self.image.blit(bracket_scaled, bracket_scaled_rect.topleft)


    def handle_action(self, action):
        """Handle keyboard navigation for buttons."""
        if action == "dial_up":
            if self.selected_button > 0:
                self.selected_button -= 1
                self.draw_buttons()
        elif action == "dial_down":
            if self.selected_button < len(self.buttons) - 1:
                self.selected_button += 1
                self.draw_buttons()
        elif action == "knob_up": # Assuming a button press action
            self.select_module()

    def select_module(self):
        """Switch to the currently selected module."""
        selected_label = self.buttons[self.selected_button]['label'].lower()
        self.pypboy.switch_module(selected_label)

    def handle_event(self, event):
        """Handle mouse click events for the buttons."""
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                # Adjust mouse position to be relative to this module's surface
                adjusted_pos = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
                
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(adjusted_pos):
                        self.selected_button = i
                        self.select_module()
                        break # Stop checking once a button is clicked

    def handle_resume(self):
        self.parent.pypboy.header.headline = "HOME"
        self.parent.pypboy.header.title = [f"USER: {config.PLAYERNAME}"]
        super(Module, self).handle_resume()
