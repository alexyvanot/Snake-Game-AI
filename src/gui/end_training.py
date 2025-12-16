import pygame
from src.gui.components import Button, InputField


def validate_model_filename(value):
    return value.strip().endswith(".txt") and len(value.strip()) > 4


class SaveButton(Button):
    def __init__(self, x, y, width, height, font):
        colors = {"normal": (50, 100, 50), "hover": (70, 130, 70)}
        border_colors = {"normal": (80, 150, 80), "hover": (100, 180, 100)}
        super().__init__(x, y, width, height, font, "Sauvegarder", colors, border_colors)


class PreviewButton(Button):
    def __init__(self, x, y, width, height, font):
        colors = {"normal": (50, 80, 120), "hover": (70, 100, 150)}
        border_colors = {"normal": (80, 120, 180), "hover": (100, 150, 200)}
        super().__init__(x, y, width, height, font, "Tester le modèle", colors, border_colors)


class MenuButton(Button):
    def __init__(self, x, y, width, height, font):
        colors = {"normal": (70, 40, 40), "hover": (100, 60, 60)}
        border_colors = {"normal": (150, 80, 80), "hover": (150, 80, 80)}
        super().__init__(x, y, width, height, font, "Retour au menu", colors, border_colors)


class EndTrainingScreen:
    def __init__(self, nn, grid_size, default_filename="model.txt"):
        pygame.init()
        self.width, self.height = 500, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Entraînement terminé")
        
        self.nn = nn
        self.grid_size = grid_size
        self.saved = False
        self.saved_filename = None
        
        self.title_font = pygame.font.Font(None, 42)
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        self.file_input = InputField(150, 120, 200, 35, self.font, default_filename, validate_model_filename)
        self.save_btn = SaveButton(175, 170, 150, 40, self.font)
        self.preview_btn = PreviewButton(125, 280, 250, 45, self.font)
        self.menu_btn = MenuButton(175, 340, 150, 40, self.font)
        
        self.running = True
        self.result = None
    
    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.result = {"action": "quit"}
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                
                self.file_input.handle_event(event)
            
            if not self.running:
                break
            
            self.save_btn.check_hover(mouse_pos)
            self.preview_btn.check_hover(mouse_pos)
            self.menu_btn.check_hover(mouse_pos)
            
            if self.save_btn.is_clicked(event) and click and self.file_input.is_valid() and not self.saved:
                self.nn.save(self.file_input.value)
                self.saved = True
                self.saved_filename = self.file_input.value
            
            if self.preview_btn.is_clicked(event) and click and self.saved:
                self.running = False
                self.result = {
                    "action": "preview",
                    "model_file": self.saved_filename,
                    "grid_size": self.grid_size
                }
            
            if self.menu_btn.is_clicked(event) and click:
                self.running = False
                self.result = {"action": "menu"}
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        return self.result
    
    def draw(self):
        self.screen.fill((30, 30, 30))
        
        title = self.title_font.render("Entraînement terminé !", True, (50, 205, 50))
        title_rect = title.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("Félicitations, votre modèle est prêt.", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 80))
        self.screen.blit(subtitle, subtitle_rect)
        
        label = self.small_font.render("Nom du fichier:", True, (180, 180, 180))
        self.screen.blit(label, (150, 100))
        
        self.file_input.draw(self.screen)
        
        if not self.file_input.is_valid():
            error = self.small_font.render("Le nom doit se terminer par .txt", True, (255, 100, 100))
            self.screen.blit(error, (150, 158))
        
        if not self.saved:
            self.save_btn.draw(self.screen)
        else:
            saved_text = self.font.render(f"Sauvegardé: {self.saved_filename}", True, (100, 200, 100))
            saved_rect = saved_text.get_rect(center=(self.width // 2, 190))
            self.screen.blit(saved_text, saved_rect)
        
        pygame.draw.line(self.screen, (60, 60, 60), (50, 230), (450, 230), 1)
        
        warning_lines = [
            "Le modèle a été entraîné sur une grille " + str(self.grid_size) + "x" + str(self.grid_size) + ".",
            "Ses performances peuvent varier sur d'autres tailles."
        ]
        for i, line in enumerate(warning_lines):
            warn = self.small_font.render(line, True, (255, 200, 100))
            warn_rect = warn.get_rect(center=(self.width // 2, 248 + i * 18))
            self.screen.blit(warn, warn_rect)
        
        if self.saved:
            self.preview_btn.draw(self.screen)
        else:
            disabled_surf = pygame.Surface((250, 45), pygame.SRCALPHA)
            disabled_surf.fill((40, 40, 40, 200))
            pygame.draw.rect(disabled_surf, (60, 60, 60), (0, 0, 250, 45), 2, border_radius=5)
            text = self.font.render("Tester le modèle", True, (100, 100, 100))
            text_rect = text.get_rect(center=(125, 22))
            disabled_surf.blit(text, text_rect)
            self.screen.blit(disabled_surf, (125, 280))
        
        self.menu_btn.draw(self.screen)
        
        pygame.display.flip()
