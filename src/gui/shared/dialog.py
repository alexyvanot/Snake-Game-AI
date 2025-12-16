import pygame
from src.gui.shared.button import Button


class ConfirmDialog:
    
    def __init__(self, screen_width, screen_height, font, small_font, 
                 title="Confirmation", message="", 
                 confirm_text="Confirmer", cancel_text="Annuler",
                 confirm_color=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.small_font = small_font
        self.visible = False
        self.title = title
        self.message = message
        
        dialog_w, dialog_h = 350, 160
        self.rect = pygame.Rect(
            (screen_width - dialog_w) // 2, 
            (screen_height - dialog_h) // 2, 
            dialog_w, dialog_h
        )
        
        btn_w, btn_h = 100, 35
        btn_y = self.rect.y + self.rect.height - 50
        
        if confirm_color:
            confirm_colors = {"normal": confirm_color, "hover": tuple(min(c + 30, 255) for c in confirm_color)}
            confirm_borders = {"normal": tuple(min(c + 30, 255) for c in confirm_color), 
                             "hover": tuple(min(c + 50, 255) for c in confirm_color)}
        else:
            confirm_colors = {"normal": (120, 50, 50), "hover": (150, 70, 70)}
            confirm_borders = {"normal": (180, 80, 80), "hover": (200, 100, 100)}
        
        self.confirm_btn = Button(
            self.rect.x + 40, btn_y, btn_w, btn_h, font, confirm_text,
            confirm_colors, confirm_borders
        )
        self.cancel_btn = Button(
            self.rect.x + self.rect.width - btn_w - 40, btn_y, btn_w, btn_h, font, cancel_text
        )
    
    def show(self, message=None):
        self.visible = True
        if message:
            self.message = message
    
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
        
        title_surf = self.font.render(self.title, True, (255, 180, 100))
        title_rect = title_surf.get_rect(center=(self.rect.centerx, self.rect.y + 30))
        screen.blit(title_surf, title_rect)
        
        msg_surf = self.small_font.render(self.message, True, (200, 200, 200))
        msg_rect = msg_surf.get_rect(center=(self.rect.centerx, self.rect.y + 70))
        screen.blit(msg_surf, msg_rect)
        
        self.confirm_btn.check_hover(mouse_pos)
        self.cancel_btn.check_hover(mouse_pos)
        self.confirm_btn.draw(screen)
        self.cancel_btn.draw(screen)
    
    def handle_click(self, pos):
        if not self.visible:
            return None
        if self.confirm_btn.rect.collidepoint(pos):
            return "confirm"
        if self.cancel_btn.rect.collidepoint(pos):
            return "cancel"
        return None
