# pypboy/modules/stats/special.py

from game.core import Entity
import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

    label = "S.P.E.C.I.A.L."

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

        self.stat = Stat('images/special_strength.png')
        self.stat.rect.topleft = (100, 0)
        self.add(self.stat)

        self.menu = pypboy.ui.Menu(240, [
            "Strength               4", 
            "Perception             7", 
            "Endurance              5", 
            "Charisma               6", 
            "Intelligence           9", 
            "Agility                4", 
            "Luck                   6"], [self.show_str, self.show_per, self.show_end, self.show_cha, self.show_int, self.show_agi, self.show_luc], 0)
        self.menu.rect[0] = 4
        self.menu.rect[1] = 60
        self.add(self.menu)

    def changeStat(self, imageUrl):
        self.stat.image = pygame.image.load(imageUrl).convert_alpha()
        self.stat.image.fill((config.TINTCOLOUR), None, pygame.BLEND_RGB_MULT)
        self.stat.rect = self.stat.image.get_rect()
        self.stat.rect.topleft = (100, 0)

    def show_str(self):
        self.changeStat('images/special_strength.png')

    def show_per(self):
        self.changeStat('images/special_perception.png')

    def show_end(self):
        self.changeStat('images/special_endurance.png')

    def show_cha(self):
        self.changeStat('images/special_charisma.png')

    def show_int(self):
        self.changeStat('images/special_intelligence.png')

    def show_agi(self):
        self.changeStat('images/special_agility.png')

    def show_luc(self):
        self.changeStat('images/special_luck.png')

class Stat(game.Entity):
    def __init__(self, imageUrl):
        # --- FIX: Properly initialize the Entity ---
        # 1. Load the image first to get its dimensions.
        image_surface = pygame.image.load(imageUrl).convert_alpha()
        
        # 2. Call the parent __init__ with the correct dimensions.
        super(Stat, self).__init__(image_surface.get_size())
        
        # 3. Now, assign the loaded surface to self.image and apply tint.
        self.image = image_surface
        self.image.fill(config.TINTCOLOUR, None, pygame.BLEND_RGB_MULT)