import pygame
from src.gui.shared.button import Button


class BackButton(Button):
    
    def __init__(self, x, y, width, height, font):
        colors = {"normal": (70, 40, 40), "hover": (100, 60, 60)}
        border_colors = {"normal": (150, 80, 80), "hover": (150, 80, 80)}
        super().__init__(x, y, width, height, font, "< Retour", colors, border_colors)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class StatsButton(Button):
    
    def __init__(self, x, y, size, font):
        colors = {"normal": (50, 70, 50), "hover": (60, 90, 60), "active": (80, 120, 80)}
        border_colors = {"normal": (80, 120, 80), "hover": (80, 120, 80), "active": (100, 180, 100)}
        super().__init__(x, y, size, size, font, "", colors, border_colors)
        self.expanded = False
    
    def draw(self, screen, active=None):
        if active is None:
            active = self.expanded
        
        if active:
            color = self.colors["active"]
            border_color = self.border_colors["active"]
        else:
            state = "hover" if self.hovered else "normal"
            color = self.colors[state]
            border_color = self.border_colors[state]
        
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=5)
        
        cx, cy = self.rect.centerx, self.rect.centery
        bar_width = 4
        pygame.draw.rect(screen, (255, 255, 255), (cx - 8, cy + 2, bar_width, 8))
        pygame.draw.rect(screen, (255, 255, 255), (cx - 2, cy - 4, bar_width, 14))
        pygame.draw.rect(screen, (255, 255, 255), (cx + 4, cy - 8, bar_width, 18))
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def toggle(self):
        self.expanded = not self.expanded
        return self.expanded
