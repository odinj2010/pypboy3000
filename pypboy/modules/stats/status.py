# pypboy/modules/stats/status.py

import pygame
import config
import pypboy.modules

class Module(pypboy.modules.SubModule):
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        
        self.image = pygame.Surface((config.WIDTH, config.HEIGHT - 80))
        self.image.fill((0, 0, 0))

        self.draw_ui()

    def draw_ui(self):
        """Draws the static UI elements for the new STATS screen."""
        # --- Left Column (Character Info & Conditions) ---
        left_panel_rect = pygame.Rect(40, 20, (config.WIDTH / 2) - 60, config.HEIGHT - 120)
        pygame.draw.rect(self.image, config.TINTCOLOUR, left_panel_rect, 1)

        # Player Info
        player_text = f"{config.PLAYERNAME} - LEVEL {config.PLAYERLEVEL}"
        # --- FIX: Use a reliable font from the FONTS list ---
        player_render = config.FONTS[18].render(player_text, True, config.TINTCOLOUR)
        self.image.blit(player_render, (left_panel_rect.x + 20, left_panel_rect.y + 20))

        # Condition Title
        condition_text = "CONDITION"
        # --- FIX: Use a reliable font from the FONTS list ---
        condition_render = config.FONTS[18].render(condition_text, True, config.TINTCOLOUR)
        condition_pos = ((left_panel_rect.centerx - condition_render.get_width() / 2), left_panel_rect.y + 100)
        self.image.blit(condition_render, condition_pos)
        
        # Health Bars (HP, AP, etc.)
        self.draw_bar("HP", 100, 100, (left_panel_rect.x + 20, left_panel_rect.y + 150))
        self.draw_bar("AP", 100, 100, (left_panel_rect.x + 20, left_panel_rect.y + 200))
        self.draw_bar("RAD", 0, 1000, (left_panel_rect.x + 20, left_panel_rect.y + 250))


        # --- Right Column (Vault Boy Image) ---
        right_panel_rect = pygame.Rect((config.WIDTH / 2) + 20, 20, (config.WIDTH / 2) - 60, config.HEIGHT - 120)
        pygame.draw.rect(self.image, config.TINTCOLOUR, right_panel_rect, 1)
        
        # Placeholder for Vault Boy
        vault_boy_text = "[VAULT BOY IMAGE AREA]"
        # --- FIX: Use a reliable font from the FONTS list ---
        vault_boy_render = config.FONTS[18].render(vault_boy_text, True, (50, 80, 50)) # Dim color
        text_rect = vault_boy_render.get_rect(center=right_panel_rect.center)
        self.image.blit(vault_boy_render, text_rect)


    def draw_bar(self, label, current, max_val, pos):
        """Helper function to draw a status bar."""
        bar_width = (config.WIDTH / 2) - 120
        bar_height = 30
        
        # Label
        # --- FIX: Use a reliable font from the FONTS list ---
        label_render = config.FONTS[14].render(label, True, config.TINTCOLOUR)
        self.image.blit(label_render, (pos[0], pos[1] + 5))
        
        # Bar Background
        bar_bg_rect = pygame.Rect(pos[0] + 80, pos[1], bar_width, bar_height)
        pygame.draw.rect(self.image, (20, 40, 20), bar_bg_rect) # Dark green background

        # Bar Fill
        if max_val > 0:
            fill_width = (current / max_val) * bar_width
        else:
            fill_width = 0
            
        if fill_width > 0:
            bar_fill_rect = pygame.Rect(pos[0] + 80, pos[1], fill_width, bar_height)
            pygame.draw.rect(self.image, config.TINTCOLOUR, bar_fill_rect)
            
        # Bar Border
        pygame.draw.rect(self.image, config.TINTCOLOUR, bar_bg_rect, 1)

    def handle_resume(self):
        self.parent.pypboy.header.headline = "STATS"
        self.parent.pypboy.header.title = ["STATUS", "SPECIAL", "SKILLS", "PERKS"]
        super(Module, self).handle_resume()