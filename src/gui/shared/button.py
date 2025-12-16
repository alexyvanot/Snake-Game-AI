import pygame


class Button:
    def __init__(self, x, y, width, height, font, text="", colors=None, border_colors=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = text
        self.hovered = False
        self.colors = colors or {"normal": (50, 50, 50), "hover": (80, 80, 80)}
        self.border_colors = border_colors or {"normal": (100, 100, 100), "hover": (100, 100, 100)}
    
    def draw(self, screen):
        state = "hover" if self.hovered else "normal"
        pygame.draw.rect(screen, self.colors[state], self.rect, border_radius=5)
        pygame.draw.rect(screen, self.border_colors[state], self.rect, 2, border_radius=5)
        if self.text:
            text_surf = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False
