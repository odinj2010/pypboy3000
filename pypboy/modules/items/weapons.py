# pypboy/modules/items/weapons.py

import pygame
import config
import pypboy.modules

class Module(pypboy.modules.SubModule):
    def __init__(self, parent, *args, **kwargs):
        # Ensure parent.pypboy exists, else fallback to parent
        self.pypboy = getattr(parent, 'pypboy', parent)
        super(Module, self).__init__(parent, *args, **kwargs)
        self.image = pygame.Surface((config.WIDTH, config.HEIGHT - 80))
        self.image.fill((0, 0, 0))
        y_pos = 20
        for item in config.WEAPONS:
            # --- FIX: Use a reliable font from the FONTS list ---
            text_render = config.FONTS[14].render(item, True, config.TINTCOLOUR)
            self.image.blit(text_render, (20, y_pos))
            y_pos += 40

    def handle_event(self, event):
        pass

    def handle_resume(self):
        self.parent.pypboy.header.headline = "ITEMS: WEAPONS"
        super(Module, self).handle_resume()