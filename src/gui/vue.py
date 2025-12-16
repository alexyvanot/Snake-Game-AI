import pygame
import os
from src.gui.components import BackButton, StatsButton, StatsPanel, Checkbox
from src.gui.stats import GameStats
from src.gui.events import BackToMenuException, GameEventHandler


class SnakeVue:
    def __init__(self, width, height, scale, model_file=None, is_training=False):
        self.width, self.height, self.scale = width, height, scale
        self.is_training = is_training
        self.auto_close = False  # Fermer automatiquement après entraînement
        
        pygame.init()
        pygame.display.set_caption('Snake')
        self.game_window = pygame.display.set_mode((width*scale, height*scale))
        asset_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "snake.png")
        self.sheet = pygame.image.load(asset_path).convert()
        self.extractSprites()
        
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.back_button = BackButton(10, 10, 90, 30, self.font)
        
        self.stats = GameStats()
        if model_file:
            self.stats.load_model_metadata(model_file)
        self.stats_button = StatsButton(width * scale - 40, 10, 30, self.font)
        self.stats_panel = StatsPanel(width * scale - 170, 50, 160, self.font)
        
        # Checkbox auto-close (uniquement en mode training)
        if is_training:
            self.auto_close_checkbox = Checkbox(
                110, 12, 20, self.small_font, 
                "Fermer auto.", checked=False
            )
        else:
            self.auto_close_checkbox = None
        
        self.event_handler = GameEventHandler(self)

    def extractSprites(self):
        self.images_body = []
        self.images_head = []
        self.images_queue = []
        for idx, pos in enumerate([(1,0), (0, 0), (0,1), (0,2), (1,2), (2,2)]):
            rect = pygame.Rect(64*pos[1], 64*pos[0], 64, 64)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sheet, (0, 0), rect)
            self.images_body.append(image)
        for idx, pos in enumerate([(0,3), (1, 4), (1,3), (0,4)]):
            rect = pygame.Rect(64*pos[1], 64*pos[0], 64, 64)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sheet, (0, 0), rect)
            self.images_head.append(image)
        for idx, pos in enumerate([(2,3), (3, 4), (3,3), (2,4)]):
            rect = pygame.Rect(64*pos[1], 64*pos[0], 64, 64)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sheet, (0, 0), rect)
            self.images_queue.append(image)
        rect = pygame.Rect(0, 64*3, 64, 64)
        self.image_fruit = pygame.Surface(rect.size).convert()
        self.image_fruit.blit(self.sheet, (0, 0), rect)
        colorkey = self.image_fruit.get_at((0,0))
        self.image_fruit.set_colorkey(colorkey, pygame.RLEACCEL)

    def displayGame(self, game):
        color = pygame.Color(0,0,0)
        pygame.draw.rect(self.game_window, color, pygame.Rect(0, 0, self.width*self.scale, self.height*self.scale))
        self.game_window.blit(self.image_fruit, (game.fruit[0]*self.scale, game.fruit[1]*self.scale))
        for idx, body in enumerate(game.serpent):
            coord = (body[0]*self.scale, body[1]*self.scale)
            if idx==0:
                self.game_window.blit(self.images_head[game.direction], coord)
                continue
            if idx==len(game.serpent)-1:
                if game.serpent[-2][0]==body[0]-1:
                    self.game_window.blit(self.images_queue[2], coord)
                elif game.serpent[-2][0]==body[0]+1:
                    self.game_window.blit(self.images_queue[3], coord)
                elif game.serpent[-2][1]==body[1]-1:
                    self.game_window.blit(self.images_queue[0], coord)
                else:
                    self.game_window.blit(self.images_queue[1], coord)
                continue
            if (game.serpent[idx+1][0]==game.serpent[idx][0]+1 and game.serpent[idx-1][1]==game.serpent[idx][1]-1) or (game.serpent[idx-1][0]==game.serpent[idx][0]+1 and game.serpent[idx+1][1]==game.serpent[idx][1]-1):
                self.game_window.blit(self.images_body[0], coord)
            elif (game.serpent[idx+1][1]==game.serpent[idx][1]+1 and game.serpent[idx-1][0]==game.serpent[idx][0]+1) or (game.serpent[idx-1][1]==game.serpent[idx][1]+1 and game.serpent[idx+1][0]==game.serpent[idx][0]+1):
                self.game_window.blit(self.images_body[1], coord)
            elif (game.serpent[idx+1][1]==game.serpent[idx][1]+1 and game.serpent[idx-1][0]==game.serpent[idx][0]-1) or (game.serpent[idx-1][1]==game.serpent[idx][1]+1 and game.serpent[idx+1][0]==game.serpent[idx][0]-1):
                self.game_window.blit(self.images_body[3], coord)
            elif (game.serpent[idx+1][0]==game.serpent[idx][0]-1 and game.serpent[idx-1][1]==game.serpent[idx][1]-1) or (game.serpent[idx-1][0]==game.serpent[idx][0]-1 and game.serpent[idx+1][1]==game.serpent[idx][1]-1):
                self.game_window.blit(self.images_body[5], coord)
            elif (game.serpent[idx+1][0]==game.serpent[idx][0]-1) or (game.serpent[idx-1][0]==game.serpent[idx][0]-1):
                self.game_window.blit(self.images_body[2], coord)
            else:
                self.game_window.blit(self.images_body[4], coord)
        pygame.display.set_caption(f'Score = {len(game.serpent)}')
        
        self.stats.update(game)
        
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(self.game_window)
        
        # Checkbox auto-close (uniquement en mode training)
        if self.auto_close_checkbox:
            self.auto_close_checkbox.check_hover(mouse_pos)
            self.auto_close_checkbox.draw(self.game_window)
            self.auto_close = self.auto_close_checkbox.checked
        
        self.stats_button.check_hover(mouse_pos)
        self.stats_button.draw(self.game_window, self.stats_panel.visible)
        self.stats_panel.draw_stats(self.game_window, self.stats)
        
        pygame.display.update()
    
    def draw_ui_only(self, status_text=""):
        """Dessine uniquement l'interface (sans le jeu) pendant les calculs"""
        # Fond noir
        self.game_window.fill((0, 0, 0))
        
        # Message de statut au centre
        if status_text:
            text_surf = self.font.render(status_text, True, (150, 150, 150))
            text_rect = text_surf.get_rect(center=(self.width * self.scale // 2, self.height * self.scale // 2))
            self.game_window.blit(text_surf, text_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Bouton retour
        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(self.game_window)
        
        # Checkbox auto-close
        if self.auto_close_checkbox:
            self.auto_close_checkbox.check_hover(mouse_pos)
            self.auto_close_checkbox.draw(self.game_window)
            self.auto_close = self.auto_close_checkbox.checked
        
        # Bouton stats
        self.stats_button.check_hover(mouse_pos)
        self.stats_button.draw(self.game_window, self.stats_panel.visible)
        self.stats_panel.draw_stats(self.game_window, self.stats)
        
        pygame.display.update()
    
    def handle_events(self, event):
        # Gérer la checkbox en premier
        if self.auto_close_checkbox:
            self.auto_close_checkbox.handle_event(event)
        self.event_handler.handle(event)
    
    def handle_back_button(self, event):
        self.handle_events(event)
    
    def new_game(self):
        self.stats.new_game()