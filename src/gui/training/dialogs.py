import pygame
from src.gui.shared.button import Button


class ConfirmExitDialog:
    def __init__(self, width, height, font, small_font):
        self.screen_width = width
        self.screen_height = height
        self.font = font
        self.small_font = small_font
        self.visible = False
        
        dialog_w, dialog_h = 350, 160
        self.rect = pygame.Rect((width - dialog_w) // 2, (height - dialog_h) // 2, dialog_w, dialog_h)
        
        btn_w, btn_h = 100, 35
        btn_y = self.rect.y + self.rect.height - 50
        self.quit_btn = Button(
            self.rect.x + 40, btn_y, btn_w, btn_h, font, "Quitter",
            {"normal": (120, 50, 50), "hover": (150, 70, 70)},
            {"normal": (180, 80, 80), "hover": (200, 100, 100)}
        )
        self.cancel_btn = Button(
            self.rect.x + self.rect.width - btn_w - 40, btn_y, btn_w, btn_h, font, "Annuler"
        )
    
    def show(self):
        self.visible = True
    
    def hide(self):
        self.visible = False
    
    def draw(self, screen, mouse_pos):
        if not self.visible:
            return
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(screen, (45, 45, 45), self.rect, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2, border_radius=10)
        
        title = self.font.render("Quitter sans sauvegarder ?", True, (255, 180, 100))
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.y + 30))
        screen.blit(title, title_rect)
        
        msg = self.small_font.render("Le modele entrainer sera perdu.", True, (200, 200, 200))
        msg_rect = msg.get_rect(center=(self.rect.centerx, self.rect.y + 65))
        screen.blit(msg, msg_rect)
        
        self.quit_btn.check_hover(mouse_pos)
        self.cancel_btn.check_hover(mouse_pos)
        self.quit_btn.draw(screen)
        self.cancel_btn.draw(screen)
    
    def handle_click(self, pos):
        if not self.visible:
            return None
        if self.quit_btn.rect.collidepoint(pos):
            return "quit"
        if self.cancel_btn.rect.collidepoint(pos):
            return "cancel"
        return None
