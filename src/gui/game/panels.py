import pygame
from src.gui.shared.panel import Panel
from src.gui.shared.checkbox import Checkbox


class StatsPanel(Panel):
    def __init__(self, x, y, width, font, small_font):
        super().__init__(x, y, width, font, small_font)
        self.target_height = 0
        self.current_height = 0
        self.expanded = False
        self.animation_speed = 15
    
    def toggle(self, expanded):
        self.expanded = expanded
        
    def update(self, lines):
        self.lines = lines
        self.target_height = len(lines) * 22 + 20 if self.expanded else 0
        
        if self.current_height < self.target_height:
            self.current_height = min(self.current_height + self.animation_speed, self.target_height)
        elif self.current_height > self.target_height:
            self.current_height = max(self.current_height - self.animation_speed, self.target_height)
    
    def draw(self, screen):
        if self.current_height <= 0:
            return
            
        panel_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, int(self.current_height))
        
        pygame.draw.rect(screen, (40, 40, 40, 200), panel_rect, border_radius=5)
        pygame.draw.rect(screen, (80, 80, 80), panel_rect, 2, border_radius=5)
        
        if self.current_height >= self.target_height and self.lines:
            y = self.rect.y + 10
            for line in self.lines:
                text = self.small_font.render(line, True, (200, 200, 200))
                screen.blit(text, (self.rect.x + 10, y))
                y += 22


class AutoCloseCheckbox(Checkbox):
    def __init__(self, x, y, font):
        super().__init__(x, y, "Sauvegarder et fermer à la fin", font)
