# pypboy/core.py

import pygame
import config
import game
import pypboy.ui
import os
from math import atan2, pi, degrees

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    print("WARNING: llama-cpp-python is not installed. AI functionality will be disabled.")

from pypboy.modules import data
from pypboy.modules import items
from pypboy.modules import stats
from pypboy.modules import home
from pypboy.modules import ai
from pypboy.modules import gpio


if config.GPIO_AVAILABLE:
    import RPi.GPIO as GPIO


class Pypboy(game.core.Engine):

    currentModule = 0

    def __init__(self, *args, **kwargs):
        if hasattr(config, 'OUTPUT_WIDTH') and hasattr(config, 'OUTPUT_HEIGHT'):
            self.rescale = True
        super(Pypboy, self).__init__(*args, **kwargs)
        
        self.llm = None
        self.load_llm()
        
        self.init_children()
        self.init_modules()
        
        self.gpio_actions = {}
        if config.GPIO_AVAILABLE:
            self.init_gpio_controls()

    def load_llm(self):
        """Loads the AI model for V.I.N.C.E."""
        if not LLAMA_CPP_AVAILABLE:
            print("Cannot load LLM: llama_cpp library not available.")
            return
            
        model_name = "Phi-3-mini-4k-instruct-q4.gguf"
        model_path = os.path.join(config.MODELS_DIR, model_name)
        
        if os.path.exists(model_path):
            print(f"Loading AI model from: {model_path}")
            try:
                self.llm = Llama(
                    model_path=model_path,
                    n_gpu_layers=0,
                    n_ctx=4096,
                    verbose=False
                )
                print("AI model loaded successfully.")
            except Exception as e:
                print(f"FATAL: Failed to load AI model: {e}")
                self.llm = None
        else:
            print(f"WARNING: AI model not found at '{model_path}'. AI will be offline.")
            self.llm = None

    def init_children(self):
        self.background = pygame.image.load('images/overlay.png').convert_alpha()
        self.background.fill(config.TINTCOLOUR, None, pygame.BLEND_RGB_MULT)

        scanlines = pypboy.ui.Scanlines(config.WIDTH, config.HEIGHT, 3, 1, [(0, 13, 3, 50), (6, 42, 22, 100), (0, 13, 3, 50)],)
        self.root_children.add(scanlines)
        scanlines2 = pypboy.ui.Scanlines(config.WIDTH, config.HEIGHT, 8, 40, [(0, 10, 1, 0), (21, 62, 42, 90), (61, 122, 82, 100), (21, 62, 42, 90)] + [(0, 10, 1, 0) for x in range(50)], True)
        self.root_children.add(scanlines2)
        self.header = pypboy.ui.Header()
        self.root_children.add(self.header)

    def init_modules(self):
        self.modules = {
            "home": home.Module(self),
            "data": data.Module(self),
            "items": items.Module(self),
            "stats": stats.Module(self),
            "ai": ai.Module(self),
            "gpio": gpio.Module(self)
        }
        for module in self.modules.values():
            module.move(4, 40)
        self.switch_module("home")

    def init_gpio_controls(self):
        for pin in config.GPIO_ACTIONS.keys():
            print("Intialising pin %s as action '%s'" % (pin, config.GPIO_ACTIONS[pin]))
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.gpio_actions[pin] = config.GPIO_ACTIONS[pin]

    def check_gpio_input(self):
        for pin in self.gpio_actions.keys():
            if GPIO.input(pin) == False:
                self.handle_action(self.gpio_actions[pin])

    def update(self):
        if hasattr(self, 'active'):
            self.active.update()
        super(Pypboy, self).update()

    # --- THIS IS THE FIX ---
    def render(self):
        # First, draw the background to clear the screen from the last frame
        self.screen.blit(self.background, (0, 0))

        # Now, continue with the original rendering logic
        interval = super(Pypboy, self).render()
        if hasattr(self, 'active'):
            self.active.render(interval)

    def switch_module(self, module):
        if module in self.modules:
            if hasattr(self, 'active'):
                self.active.handle_action("pause")
                self.remove(self.active)
            self.active = self.modules[module]
            self.active.parent = self
            self.active.handle_action("resume")
            self.add(self.active)
        else:
            print("Module '%s' not implemented." % module)

    def handle_swipe(self, swipe):
        if swipe == -1: return
        total_modules = len(config.MODULES)
        if swipe == 4: #UP
            self.currentModule = (self.currentModule + 1) % total_modules
            self.switch_module(config.MODULES[self.currentModule])
        elif swipe == 3: #DOWN
            self.currentModule = (self.currentModule - 1 + total_modules) % total_modules
            self.switch_module(config.MODULES[self.currentModule])
        else:
            self.active.handle_swipe(swipe)

    def handle_action(self, action):
        if action.startswith('module_'):
            self.switch_module(action[7:])
        else:
            if hasattr(self, 'active'):
                self.active.handle_action(action)

    def handle_event(self, event):
        if hasattr(self, 'active'):
            self.active.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE):
                self.running = False
            else:
                if event.key in config.ACTIONS:
                    self.handle_action(config.ACTIONS[event.key])
        elif event.type == pygame.QUIT:
            self.running = False
        elif event.type == config.EVENTS['SONG_END']:
            if config.SOUND_ENABLED:
                if hasattr(config, 'radio'):
                    config.radio.handle_event(event)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            swipe = 4
            self.handle_swipe(swipe)

    def run(self):
        self.running = True
        while self.running:
            if config.GPIO_AVAILABLE:
                self.check_gpio_input()
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.render()
            pygame.time.wait(1)

        try:
            pygame.mixer.quit()
        except Exception as e:
            print(e)
            pass