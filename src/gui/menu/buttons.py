import pygame


class MenuButton:
    
    def __init__(self, x, y, width, height, text, font, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
        self.base_color = color
        
    def draw(self, screen):
        if self.base_color:
            r, g, b = self.base_color
            color = (min(r + 30, 255), min(g + 30, 255), min(b + 30, 255)) if self.hovered else self.base_color
            border = (min(r + 50, 255), min(g + 50, 255), min(b + 50, 255))
        else:
            color = (80, 80, 80) if self.hovered else (50, 50, 50)
            border = (100, 100, 100)
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, border, self.rect, 2, border_radius=5)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def is_clicked(self, pos, click):
        return click and self.rect.collidepoint(pos)
