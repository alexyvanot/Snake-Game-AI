import pygame
from src.utils.input import (
    KEY_DIRECTIONS, MODIFIER_KEYS,
    get_cursor_position_from_click, delete_char_before,
    delete_char_after, insert_char, move_cursor
)


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
        
        if stats.model_metadata and stats.model_metadata.created_at:
            lines.append("")
            lines.append("--- Modèle ---")
            lines.append(f"Grille: {stats.model_metadata.grid_size}x{stats.model_metadata.grid_size}")
            lines.append(f"Itérations: {stats.model_metadata.iterations}")
            lines.append(f"Population: {stats.model_metadata.population}")
            lines.append(f"Perf: {stats.model_metadata.best_score:.4f}")
        
        self.draw(screen, lines)


class InputField:
    def __init__(self, x, y, width, height, font, default_value="", validator=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.value = str(default_value)
        self.active = False
        self.cursor_pos = len(self.value)
        self.cursor_visible = True
        self.cursor_timer = 0
        self.validator = validator
    
    def is_valid(self):
        if self.validator:
            return self.validator(self.value)
        return bool(self.value.strip())
    
    def draw(self, screen):
        valid = self.is_valid()
        bg_color = (100, 100, 100) if self.active else (60, 60, 60)
        border_color = (150, 150, 150) if self.active else (80, 80, 80)
        if not valid:
            bg_color = (100, 50, 50) if self.active else (80, 40, 40)
            border_color = (200, 80, 80) if self.active else (150, 60, 60)
        
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=3)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=3)
        
        text_surf = self.font.render(self.value, True, (255, 255, 255))
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 8))
        
        if self.active:
            self.cursor_timer = (self.cursor_timer + 1) % 60
            if self.cursor_timer == 0:
                self.cursor_visible = not self.cursor_visible
            if self.cursor_visible:
                cursor_x = self.rect.x + 10 + self.font.size(self.value[:self.cursor_pos])[0]
                pygame.draw.line(screen, (255, 255, 255), 
                               (cursor_x, self.rect.y + 8), 
                               (cursor_x, self.rect.y + 28), 2)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            was_active = self.active
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                if not was_active:
                    self.cursor_pos = len(self.value)
                    self.cursor_visible = True
                    self.cursor_timer = 0
                else:
                    self.cursor_pos = get_cursor_position_from_click(
                        self.font, self.value, event.pos[0] - self.rect.x - 10)
        elif event.type == pygame.KEYDOWN and self.active:
            self._handle_keydown(event)
    
    def _handle_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.value, self.cursor_pos = delete_char_before(self.value, self.cursor_pos)
        elif event.key == pygame.K_DELETE:
            self.value, self.cursor_pos = delete_char_after(self.value, self.cursor_pos)
        elif event.key in KEY_DIRECTIONS:
            self.cursor_pos = move_cursor(self.cursor_pos, KEY_DIRECTIONS[event.key], len(self.value))
        elif event.key == pygame.K_RETURN:
            self.active = False
        elif event.key not in MODIFIER_KEYS and event.unicode and event.unicode.isprintable():
            self.value, self.cursor_pos = insert_char(self.value, self.cursor_pos, event.unicode)


class Checkbox:
    """Case à cocher simple"""
    
    def __init__(self, x, y, size, font, label="", checked=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.font = font
        self.label = label
        self.checked = checked
        self.hovered = False
        self.size = size
    
    def draw(self, screen):
        # Couleur selon état
        bg_color = (60, 80, 60) if self.checked else (50, 50, 50)
        border_color = (100, 150, 100) if self.checked else (100, 100, 100)
        if self.hovered:
            bg_color = (70, 90, 70) if self.checked else (70, 70, 70)
        
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=3)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=3)
        
        # Coche si checked
        if self.checked:
            cx, cy = self.rect.centerx, self.rect.centery
            points = [
                (cx - 6, cy),
                (cx - 2, cy + 5),
                (cx + 6, cy - 5)
            ]
            pygame.draw.lines(screen, (150, 255, 150), False, points, 3)
        
        # Label à droite
        if self.label:
            label_surf = self.font.render(self.label, True, (200, 200, 200))
            screen.blit(label_surf, (self.rect.x + self.size + 8, self.rect.y + (self.size - label_surf.get_height()) // 2))
    
    def check_hover(self, pos):
        # Zone cliquable inclut le label
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
