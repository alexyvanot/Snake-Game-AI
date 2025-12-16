import sys
import pygame
from src.config.env import (
    ENV_MODEL_FILE, ENV_ITERATIONS, ENV_POPULATION, ENV_SELECTION,
    ENV_CROSSOVER, ENV_MUTATION, ENV_GRID_SIZE, ENV_NB_GAMES,
    ENV_FPS, ENV_HIDDEN_LAYER
)
from src.utils.input import (
    KEY_DIRECTIONS, MODIFIER_KEYS,
    get_cursor_position_from_click, delete_char_before,
    delete_char_after, insert_char, move_cursor
)
from src.gui.model_selector import ModelSelector, ModelInfoPanel

TOOLTIPS = {
    "model_file": "Nom du fichier .txt où sauvegarder/charger le modèle",
    "iterations": "Nombre de générations d'entraînement",
    "population": "Nombre d'individus par génération",
    "selection": "Nombre des meilleurs individus gardés",
    "crossover": "Probabilité de mélanger deux parents (0-1)",
    "mutation": "Intensité des mutations aléatoires",
    "grid_size": "Dimensions de la grille de jeu (NxN)",
    "nb_games": "Nombre de parties pour évaluer chaque individu",
    "hidden_layer": "Nombre de neurones dans la couche cachée",
    "fps": "Vitesse d'affichage (images par seconde)",
}

# assert func
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


class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
        
    def draw(self, screen):
        color = (80, 80, 80) if self.hovered else (50, 50, 50)
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2, border_radius=5)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def is_clicked(self, pos, click):
        return click and self.rect.collidepoint(pos)

class InputField:
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
        
    def draw(self, screen, label_x):
        # Label
        label_surf = self.font.render(self.label, True, (200, 200, 200))
        self.label_rect = pygame.Rect(label_x, self.rect.y + 5, label_surf.get_width(), label_surf.get_height())
        screen.blit(label_surf, (label_x, self.rect.y + 5))
        
        # Couleurs selon validité
        valid = self.is_valid()
        bg_color = (100, 50, 50) if not valid and self.active else (80, 40, 40) if not valid else (100, 100, 100) if self.active else (60, 60, 60)
        border_color = (200, 80, 80) if not valid and self.active else (150, 60, 60) if not valid else (150, 150, 150) if self.active else (80, 80, 80)
        
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=3)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=3)
        
        # txt
        screen.blit(self.font.render(self.value, True, (255, 255, 255)), (self.rect.x + 10, self.rect.y + 5))
        
        # crrseur
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

class ConfigMenu:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake AI - Configuration")
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.tooltip_font = pygame.font.Font(None, 20)
        
        self.mode = "train"
        self.running = True
        self.result = None
        self.current_tooltip = None
        
        self.train_btn = Button(50, 100, 240, 50, "Entraîner un modèle", self.font)
        self.play_btn = Button(310, 100, 240, 50, "Jouer avec modèle", self.font)
        self.launch_btn = Button(200, 640, 200, 50, "LANCER", self.font)
        
        self.create_fields()
        self.create_model_selector()
        
    def create_model_selector(self):
        self.model_selector = ModelSelector(50, 180, 300, 250, self.font, self.small_font)
        self.model_info_panel = ModelInfoPanel(370, 180, 180, 250, self.font, self.small_font)
        
    def create_fields(self):
        y_start = 180
        spacing = 45
        field_x = 300
        field_w = 250
        
        self.train_fields = [
            InputField(field_x, y_start, field_w, 35, "Fichier modèle:", ENV_MODEL_FILE, self.small_font, TOOLTIPS["model_file"], "text"),
            InputField(field_x, y_start + spacing, field_w, 35, "Itérations:", ENV_ITERATIONS, self.small_font, TOOLTIPS["iterations"], "int"),
            InputField(field_x, y_start + spacing*2, field_w, 35, "Population:", ENV_POPULATION, self.small_font, TOOLTIPS["population"], "int"),
            InputField(field_x, y_start + spacing*3, field_w, 35, "Sélection:", ENV_SELECTION, self.small_font, TOOLTIPS["selection"], "int"),
            InputField(field_x, y_start + spacing*4, field_w, 35, "Taux crossover:", ENV_CROSSOVER, self.small_font, TOOLTIPS["crossover"], "float"),
            InputField(field_x, y_start + spacing*5, field_w, 35, "Taux mutation:", ENV_MUTATION, self.small_font, TOOLTIPS["mutation"], "float"),
            InputField(field_x, y_start + spacing*6, field_w, 35, "Taille grille:", ENV_GRID_SIZE, self.small_font, TOOLTIPS["grid_size"], "int"),
            InputField(field_x, y_start + spacing*7, field_w, 35, "Parties par éval:", ENV_NB_GAMES, self.small_font, TOOLTIPS["nb_games"], "int"),
            InputField(field_x, y_start + spacing*8, field_w, 35, "Neurones cachés:", ENV_HIDDEN_LAYER, self.small_font, TOOLTIPS["hidden_layer"], "int"),
        ]
        
        self.play_fields = [
            InputField(field_x, y_start + 280, field_w, 35, "FPS:", ENV_FPS, self.small_font, TOOLTIPS["fps"], "int"),
            InputField(field_x, y_start + 280 + spacing, field_w, 35, "Taille grille:", ENV_GRID_SIZE, self.small_font, TOOLTIPS["grid_size"], "int"),
        ]
    
    def all_fields_valid(self):
        if self.mode == "train":
            return all(field.is_valid() for field in self.train_fields)
        else:
            has_model = self.model_selector.get_selected_model() is not None
            fields_valid = all(field.is_valid() for field in self.play_fields)
            return has_model and fields_valid
        
    def run(self):
        clock = pygame.time.Clock()
        
        try:
            while self.running:
                mouse_pos = pygame.mouse.get_pos()
                click = False
                self.current_tooltip = None
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.result = None
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        click = True
                    
                    if self.mode == "train":
                        for field in self.train_fields:
                            field.handle_event(event)
                    else:
                        self.model_selector.handle_event(event)
                        for field in self.play_fields:
                            field.handle_event(event)
                
                if not self.running:
                    break
                
                if self.mode == "train":
                    for field in self.train_fields:
                        if field.is_label_hovered(mouse_pos):
                            self.current_tooltip = field.tooltip
                            break
                else:
                    self.model_selector.check_hover(mouse_pos)
                    for field in self.play_fields:
                        if field.is_label_hovered(mouse_pos):
                            self.current_tooltip = field.tooltip
                            break
                        
                self.train_btn.check_hover(mouse_pos)
                self.play_btn.check_hover(mouse_pos)
                self.launch_btn.check_hover(mouse_pos)
                
                if self.train_btn.is_clicked(mouse_pos, click):
                    self.mode = "train"
                elif self.play_btn.is_clicked(mouse_pos, click):
                    self.mode = "play"
                    self.model_selector.refresh_models()
                elif self.launch_btn.is_clicked(mouse_pos, click) and self.all_fields_valid():
                    self.running = False
                    self.build_result()
                    
                self.draw(mouse_pos)
                clock.tick(60)
        except KeyboardInterrupt:
            self.result = None
            
        pygame.quit()
        return self.result
        
    def build_result(self):
        if self.mode == "train":
            self.result = {
                "mode": "train",
                "model_file": self.train_fields[0].value,
                "iterations": int(self.train_fields[1].value),
                "population": int(self.train_fields[2].value),
                "selection": int(self.train_fields[3].value),
                "crossover": float(self.train_fields[4].value),
                "mutation": float(self.train_fields[5].value),
                "grid_size": int(self.train_fields[6].value),
                "nb_games": int(self.train_fields[7].value),
                "hidden_layer": int(self.train_fields[8].value),
            }
        else:
            selected = self.model_selector.get_selected_model()
            self.result = {
                "mode": "play",
                "model_file": selected["path"],
                "fps": int(self.play_fields[0].value),
                "grid_size": int(self.play_fields[1].value),
            }
            
    def draw(self, mouse_pos):
        self.screen.fill((30, 30, 30))
        
        title = self.title_font.render("Snake AI", True, (50, 205, 50))
        title_rect = title.get_rect(center=(self.width // 2, 45))
        self.screen.blit(title, title_rect)
        
        if self.mode == "train":
            pygame.draw.rect(self.screen, (50, 205, 50), self.train_btn.rect, 3, border_radius=5)
            self.train_btn.hovered = True
        else:
            pygame.draw.rect(self.screen, (50, 205, 50), self.play_btn.rect, 3, border_radius=5)
            self.play_btn.hovered = True
            
        self.train_btn.draw(self.screen)
        self.play_btn.draw(self.screen)
        
        if self.mode == "train":
            for field in self.train_fields:
                field.draw(self.screen, 50)
        else:
            label = self.small_font.render("Sélectionner un modèle:", True, (200, 200, 200))
            self.screen.blit(label, (50, 160))
            self.model_selector.draw(self.screen)
            self.model_info_panel.draw(self.screen, self.model_selector.get_selected_model())
            for field in self.play_fields:
                field.draw(self.screen, 50)
            
        self.launch_btn.draw(self.screen)
        
        if self.current_tooltip:
            self.draw_tooltip(mouse_pos, self.current_tooltip)
        
        pygame.display.flip()
    
    def draw_tooltip(self, pos, text):
        padding = 8
        text_surf = self.tooltip_font.render(text, True, (255, 255, 255))
        tooltip_w = text_surf.get_width() + padding * 2
        tooltip_h = text_surf.get_height() + padding * 2
        
        tooltip_x = pos[0] + 15
        tooltip_y = pos[1] + 15
        
        if tooltip_x + tooltip_w > self.width:
            tooltip_x = pos[0] - tooltip_w - 5
        if tooltip_y + tooltip_h > self.height:
            tooltip_y = pos[1] - tooltip_h - 5
        
        pygame.draw.rect(self.screen, (60, 60, 60), (tooltip_x, tooltip_y, tooltip_w, tooltip_h), border_radius=4)
        pygame.draw.rect(self.screen, (100, 100, 100), (tooltip_x, tooltip_y, tooltip_w, tooltip_h), 1, border_radius=4)
        self.screen.blit(text_surf, (tooltip_x + padding, tooltip_y + padding))
