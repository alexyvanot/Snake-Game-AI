"""Utilitaires pour la gestion des entrées clavier et souris"""
import pygame

# Mapping des touches de navigation
KEY_DIRECTIONS = {
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_HOME: "home",
    pygame.K_END: "end",
}

# Touches modificatrices à ignorer
MODIFIER_KEYS = (
    pygame.K_LSHIFT, pygame.K_RSHIFT,
    pygame.K_LCTRL, pygame.K_RCTRL,
    pygame.K_LALT, pygame.K_RALT
)


def get_cursor_position_from_click(font, text, click_x):
    """Calcule la position du curseur en fonction du clic"""
    for i in range(len(text) + 1):
        text_width = font.size(text[:i])[0]
        if text_width >= click_x:
            if i > 0:
                prev_width = font.size(text[:i-1])[0]
                return i - 1 if click_x - prev_width < text_width - click_x else i
            return 0
    return len(text)


def delete_char_before(text, cursor_pos):
    """Supprime le caractère avant le curseur (backspace)"""
    if cursor_pos > 0:
        return text[:cursor_pos-1] + text[cursor_pos:], cursor_pos - 1
    return text, cursor_pos


def delete_char_after(text, cursor_pos):
    """Supprime le caractère après le curseur (delete)"""
    if cursor_pos < len(text):
        return text[:cursor_pos] + text[cursor_pos+1:], cursor_pos
    return text, cursor_pos


def insert_char(text, cursor_pos, char):
    """Insère un caractère à la position du curseur"""
    return text[:cursor_pos] + char + text[cursor_pos:], cursor_pos + 1


def move_cursor(cursor_pos, direction, text_length):
    """Déplace le curseur (left/right/home/end)"""
    if direction == "left":
        return max(0, cursor_pos - 1)
    elif direction == "right":
        return min(text_length, cursor_pos + 1)
    elif direction == "home":
        return 0
    elif direction == "end":
        return text_length
    return cursor_pos
