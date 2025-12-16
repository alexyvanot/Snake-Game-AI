import pygame
from src.gui.menu.buttons import MenuButton


class OverwriteDialog:
    
    def __init__(self, width, height, font, small_font):
        self.width = width
        self.height = height
        self.font = font
        self.small_font = small_font
        self.visible = False
        self.filename = ""
        
        dialog_w, dialog_h = 400, 180
        self.rect = pygame.Rect((width - dialog_w) // 2, (height - dialog_h) // 2, dialog_w, dialog_h)
        
        btn_w, btn_h = 120, 40
        btn_y = self.rect.y + self.rect.height - 60
        self.confirm_btn = MenuButton(self.rect.x + 50, btn_y, btn_w, btn_h, "Ecraser", font, color=(150, 50, 50))
        self.cancel_btn = MenuButton(self.rect.x + self.rect.width - btn_w - 50, btn_y, btn_w, btn_h, "Annuler", font)
    
    def show(self, filename):
        self.visible = True
        self.filename = filename
    
    def hide(self):
        self.visible = False
    
    def draw(self, screen, mouse_pos):
        if not self.visible:
            return
        
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(screen, (45, 45, 45), self.rect, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2, border_radius=10)
        
        warning = self.font.render("!", True, (255, 200, 50))
        screen.blit(warning, (self.rect.x + 20, self.rect.y + 20))
        
        title = self.font.render("Fichier existant", True, (255, 200, 50))
        screen.blit(title, (self.rect.x + 50, self.rect.y + 20))
        
        msg1 = self.small_font.render(f"Le fichier '{self.filename}' existe déjà.", True, (220, 220, 220))
        msg2 = self.small_font.render("Voulez-vous l'écraser ?", True, (220, 220, 220))
        screen.blit(msg1, (self.rect.x + 20, self.rect.y + 60))
        screen.blit(msg2, (self.rect.x + 20, self.rect.y + 85))
        
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
