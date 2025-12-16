import os
import pygame
from src.gui.shared.input_field import InputField
from src.utils.input import (
    KEY_DIRECTIONS, MODIFIER_KEYS,
    get_cursor_position_from_click, delete_char_before,
    delete_char_after, insert_char, move_cursor
)


def is_valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_valid_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_field(value, field_type):
    if not value.strip():
        return False
    if field_type == "int":
        return is_valid_int(value)
    elif field_type == "float":
        return is_valid_float(value)
    return True


class MenuInputField:
    
    def __init__(self, x, y, width, height, label, default_value, font, tooltip="", field_type="text"):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.value = str(default_value)
        self.font = font
        self.active = False
        self.tooltip = tooltip
        self.label_rect = None
        self.cursor_pos = len(self.value)
        self.cursor_visible = True
        self.cursor_timer = 0
        self.field_type = field_type
        
    def is_valid(self):
        return validate_field(self.value, self.field_type)
    
    def get_colors(self):
        valid = self.is_valid()
        if not valid:
            bg = (100, 50, 50) if self.active else (80, 40, 40)
            border = (200, 80, 80) if self.active else (150, 60, 60)
        else:
            bg = (100, 100, 100) if self.active else (60, 60, 60)
            border = (150, 150, 150) if self.active else (80, 80, 80)
        return bg, border, (255, 255, 255)
        
    def draw(self, screen, label_x):
        label_surf = self.font.render(self.label, True, (200, 200, 200))
        self.label_rect = pygame.Rect(label_x, self.rect.y + 5, label_surf.get_width(), label_surf.get_height())
        screen.blit(label_surf, (label_x, self.rect.y + 5))
        
        bg_color, border_color, text_color = self.get_colors()
        
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=3)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=3)
        
        screen.blit(self.font.render(self.value, True, text_color), (self.rect.x + 10, self.rect.y + 5))
        
        if self.active:
            self.cursor_timer = (self.cursor_timer + 1) % 60
            if self.cursor_timer == 0:
                self.cursor_visible = not self.cursor_visible
            if self.cursor_visible:
                cursor_x = self.rect.x + 10 + self.font.size(self.value[:self.cursor_pos])[0]
                pygame.draw.line(screen, (255, 255, 255), (cursor_x, self.rect.y + 5), (cursor_x, self.rect.y + 25), 2)
    
    def is_label_hovered(self, pos):
        return self.label_rect and self.label_rect.collidepoint(pos)
        
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
                    self.cursor_pos = get_cursor_position_from_click(self.font, self.value, event.pos[0] - self.rect.x - 10)
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


class ModelFileField(MenuInputField):
    def is_valid(self):
        value = self.value.strip()
        if not value:
            return False
        if '.' in value:
            return value.endswith('.txt')
        return True
    
    def file_exists(self):
        if not self.value.strip():
            return False
        path = self.value if self.value.endswith('.txt') else self.value + '.txt'
        return os.path.exists(path)
    
    def get_colors(self):
        valid = self.is_valid()
        if not valid:
            bg = (100, 50, 50) if self.active else (80, 40, 40)
            border = (200, 80, 80) if self.active else (150, 60, 60)
            text = (255, 255, 255)
        elif self.file_exists():
            bg = (100, 90, 40) if self.active else (80, 70, 30)
            border = (200, 180, 60) if self.active else (150, 130, 40)
            text = (255, 220, 100)
        else:
            bg = (100, 100, 100) if self.active else (60, 60, 60)
            border = (150, 150, 150) if self.active else (80, 80, 80)
            text = (255, 255, 255)
        return bg, border, text
    
    def draw(self, screen, label_x):
        super().draw(screen, label_x)
        if self.file_exists() and self.is_valid():
            warning = self.font.render("!", True, (255, 200, 50))
            screen.blit(warning, (self.rect.x + self.rect.width + 5, self.rect.y + 5))
