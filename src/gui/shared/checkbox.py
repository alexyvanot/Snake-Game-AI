import pygame


class Checkbox:
    def __init__(self, x, y, size, font, label="", checked=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.font = font
        self.label = label
        self.checked = checked
        self.hovered = False
        self.size = size
    
    def draw(self, screen):
        bg_color = (60, 80, 60) if self.checked else (50, 50, 50)
        border_color = (100, 150, 100) if self.checked else (100, 100, 100)
        if self.hovered:
            bg_color = (70, 90, 70) if self.checked else (70, 70, 70)
        
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=3)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=3)
        
        if self.checked:
            cx, cy = self.rect.centerx, self.rect.centery
            points = [
                (cx - 6, cy),
                (cx - 2, cy + 5),
                (cx + 6, cy - 5)
            ]
            pygame.draw.lines(screen, (150, 255, 150), False, points, 3)
        
        if self.label:
            label_surf = self.font.render(self.label, True, (200, 200, 200))
            screen.blit(label_surf, (self.rect.x + self.size + 8, self.rect.y + (self.size - label_surf.get_height()) // 2))
    
    def check_hover(self, pos):
        label_width = self.font.size(self.label)[0] if self.label else 0
        clickable = pygame.Rect(self.rect.x, self.rect.y, self.size + 8 + label_width, self.size)
        self.hovered = clickable.collidepoint(pos)
        return self.hovered
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            label_width = self.font.size(self.label)[0] if self.label else 0
            clickable = pygame.Rect(self.rect.x, self.rect.y, self.size + 8 + label_width, self.size)
            if clickable.collidepoint(event.pos):
                self.checked = not self.checked
                return True
        return False
    
    def handle_click(self, pos):
        if pos is None:
            return False
        label_width = self.font.size(self.label)[0] if self.label else 0
        clickable = pygame.Rect(self.rect.x, self.rect.y, self.size + 8 + label_width, self.size)
        if clickable.collidepoint(pos):
            self.checked = not self.checked
            return True
        return False
