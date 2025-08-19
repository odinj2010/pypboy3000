import game
import pygame
import config

class Module(game.Entity):
    def draw(self, surface):
        pass
    def handle_event(self, event):
        pass
    def move(self, x, y):
        self.position = (x, y)
        # If the superclass has a move method, call it
        if hasattr(super(Module, self), 'move'):
            super(Module, self).move(x, y)
    def __init__(self, pypboy, *args, **kwargs):
        self.pypboy = pypboy
        self.position = (0, 0)
        super(Module, self).__init__((config.WIDTH, config.HEIGHT - 80), *args, **kwargs)
        self.submodules = []

    def handle_action(self, action):
        if action.startswith("knob_"):
            self.switch_submodule(int(action[-1]) - 1)

    def switch_submodule(self, module_index):
        if module_index < len(self.submodules):
            for module in self.submodules:
                # --- MODIFICATION: Changed back to self.groups() ---
                if module in self.groups():
                    # --- MODIFICATION: Changed back to self.groups() ---
                    self.groups()[0].remove(module)
            groups = self.groups()
            if groups:
                self.submodules[module_index].add(groups[0])
            else:
                # Optionally log or handle the case where no groups are available
                pass
            self.submodules[module_index].handle_resume()

class SubModule(game.Entity):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.pypboy = parent.pypboy
        super(SubModule, self).__init__((config.WIDTH, config.HEIGHT - 80), *args, **kwargs)

    def handle_action(self, action):
        pass

    def handle_resume(self):
        print(f"Resuming {self.__class__.__name__}")

    def handle_pause(self):
        print(f"Pausing {self.__class__.__name__}")
