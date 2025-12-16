import pygame


class Panel:
    def __init__(self, x, y, width, font, small_font=None, line_height=22):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, 0)
        self.width = width
        self.font = font
        self.small_font = small_font or font
        self.visible = False
        self.line_height = line_height
        self.bg_color = (30, 30, 30, 220)
        self.border_color = (80, 120, 80)
        self.text_color = (220, 220, 220)
        self.lines = []
    
    def toggle(self):
        self.visible = not self.visible
    
    def draw(self, screen, lines=None):
        if not self.visible:
            return
        
        if lines is None:
            lines = self.lines
        
        padding = 10
        height = len(lines) * self.line_height + padding * 2
        
        panel_surface = pygame.Surface((self.width, height), pygame.SRCALPHA)
        panel_surface.fill(self.bg_color)
        pygame.draw.rect(panel_surface, self.border_color, (0, 0, self.width, height), 2, border_radius=5)
        
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, self.text_color)
            panel_surface.blit(text_surf, (padding, padding + i * self.line_height))
        
        screen.blit(panel_surface, (self.x, self.y))
