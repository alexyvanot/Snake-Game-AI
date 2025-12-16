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


class BackButton(Button):
    def __init__(self, x, y, width, height, font):
        colors = {"normal": (70, 40, 40), "hover": (100, 60, 60)}
        border_colors = {"normal": (150, 80, 80), "hover": (150, 80, 80)}
        super().__init__(x, y, width, height, font, "< Retour", colors, border_colors)


class StatsButton(Button):
    def __init__(self, x, y, size, font):
        colors = {"normal": (50, 70, 50), "hover": (60, 90, 60), "active": (80, 120, 80)}
        border_colors = {"normal": (80, 120, 80), "hover": (80, 120, 80), "active": (100, 180, 100)}
        super().__init__(x, y, size, size, font, "", colors, border_colors)
    
    def draw(self, screen, active=False):
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


class Panel:
    def __init__(self, x, y, width, font, line_height=22):
        self.x = x
        self.y = y
        self.width = width
        self.font = font
        self.visible = False
        self.line_height = line_height
        self.bg_color = (30, 30, 30, 220)
        self.border_color = (80, 120, 80)
        self.text_color = (220, 220, 220)
    
    def toggle(self):
        self.visible = not self.visible
    
    def draw(self, screen, lines):
        if not self.visible:
            return
        
        padding = 10
        height = len(lines) * self.line_height + padding * 2
        
        panel_surface = pygame.Surface((self.width, height), pygame.SRCALPHA)
        panel_surface.fill(self.bg_color)
        pygame.draw.rect(panel_surface, self.border_color, (0, 0, self.width, height), 2, border_radius=5)
        
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, self.text_color)
            panel_surface.blit(text_surf, (padding, padding + i * self.line_height))
        
        screen.blit(panel_surface, (self.x, self.y))


class StatsPanel(Panel):
    def __init__(self, x, y, width, font):
        super().__init__(x, y, width, font)
    
    def draw_stats(self, screen, stats):
        lines = [
            f"Parties: {stats.games_played}",
            f"Score actuel: {stats.current_score}",
            f"Meilleur: {stats.best_score}",
            f"Pommes total: {stats.total_apples}",
            f"Moy. pommes: {stats.get_avg_apples():.1f}",
            f"Steps total: {stats.total_steps}",
        ]
        self.draw(screen, lines)
