import pygame
from src.utils.input import (
    KEY_DIRECTIONS, MODIFIER_KEYS,
    get_cursor_position_from_click, delete_char_before,
    delete_char_after, insert_char, move_cursor
)


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
    
    def get_colors(self):
        valid = self.is_valid()
        if not valid:
            bg = (100, 50, 50) if self.active else (80, 40, 40)
            border = (200, 80, 80) if self.active else (150, 60, 60)
        else:
            bg = (100, 100, 100) if self.active else (60, 60, 60)
            border = (150, 150, 150) if self.active else (80, 80, 80)
        return bg, border, (255, 255, 255)
    
    def draw(self, screen):
        bg_color, border_color, text_color = self.get_colors()
        
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=3)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=3)
        
        text_surf = self.font.render(self.value, True, text_color)
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
