import os
import pygame
from src.ai.metadata import ModelMetadata


def scan_models(base_path="."):
    models = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.venv', 'venv']]
        for file in files:
            if file.endswith(".txt"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r") as f:
                        first_line = f.readline().strip()
                        parts = first_line.split()
                        if len(parts) >= 2 and all(p.isdigit() for p in parts):
                            rel_path = os.path.relpath(filepath, base_path)
                            metadata = ModelMetadata.load(filepath)
                            models.append({
                                "path": filepath,
                                "name": rel_path,
                                "metadata": metadata
                            })
                except (IOError, UnicodeDecodeError):
                    pass
    return models


class ModelSelector:
    def __init__(self, x, y, width, height, font, small_font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.small_font = small_font
        self.models = []
        self.selected_index = -1
        self.scroll_offset = 0
        self.item_height = 35
        self.hovered_index = -1
        self.refresh_models()
    
    def refresh_models(self):
        self.models = scan_models(".")
        if self.models and self.selected_index == -1:
            self.selected_index = 0
    
    def get_selected_model(self):
        if 0 <= self.selected_index < len(self.models):
            return self.models[self.selected_index]
        return None
    
    def draw(self, screen):
        pygame.draw.rect(screen, (40, 40, 40), self.rect, border_radius=5)
        pygame.draw.rect(screen, (80, 80, 80), self.rect, 2, border_radius=5)
        
        if not self.models:
            no_model = self.font.render("Aucun modèle trouvé", True, (150, 150, 150))
            no_rect = no_model.get_rect(center=self.rect.center)
            screen.blit(no_model, no_rect)
            return
        
        clip_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4)
        screen.set_clip(clip_rect)
        
        visible_items = self.rect.height // self.item_height
        max_scroll = max(0, len(self.models) - visible_items)
        self.scroll_offset = min(self.scroll_offset, max_scroll)
        
        for i, model in enumerate(self.models):
            if i < self.scroll_offset:
                continue
            
            item_y = self.rect.y + (i - self.scroll_offset) * self.item_height
            if item_y > self.rect.y + self.rect.height:
                break
            
            item_rect = pygame.Rect(self.rect.x + 2, item_y, self.rect.width - 4, self.item_height - 2)
            
            if i == self.selected_index:
                pygame.draw.rect(screen, (60, 100, 60), item_rect, border_radius=3)
            elif i == self.hovered_index:
                pygame.draw.rect(screen, (50, 50, 50), item_rect, border_radius=3)
            
            name_surf = self.small_font.render(model["name"], True, (220, 220, 220))
            screen.blit(name_surf, (item_rect.x + 10, item_rect.y + 5))
            
            meta = model["metadata"]
            if meta.created_at:
                info = f"{meta.grid_size}x{meta.grid_size} | {meta.iterations} iter"
            else:
                info = "Pas de métadonnées"
            info_surf = self.small_font.render(info, True, (140, 140, 140))
            screen.blit(info_surf, (item_rect.x + 10, item_rect.y + 18))
        
        screen.set_clip(None)
        
        if len(self.models) > visible_items:
            scrollbar_height = max(20, self.rect.height * visible_items // len(self.models))
            scrollbar_y = self.rect.y + (self.rect.height - scrollbar_height) * self.scroll_offset // max_scroll if max_scroll > 0 else self.rect.y
            scrollbar_rect = pygame.Rect(self.rect.x + self.rect.width - 8, scrollbar_y, 6, scrollbar_height)
            pygame.draw.rect(screen, (80, 80, 80), scrollbar_rect, border_radius=3)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.button == 1:
                    rel_y = event.pos[1] - self.rect.y
                    clicked_index = self.scroll_offset + rel_y // self.item_height
                    if 0 <= clicked_index < len(self.models):
                        self.selected_index = clicked_index
                elif event.button == 4:
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif event.button == 5:
                    visible_items = self.rect.height // self.item_height
                    max_scroll = max(0, len(self.models) - visible_items)
                    self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
    
    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            rel_y = pos[1] - self.rect.y
            self.hovered_index = self.scroll_offset + rel_y // self.item_height
            if self.hovered_index >= len(self.models):
                self.hovered_index = -1
        else:
            self.hovered_index = -1


class ModelInfoPanel:
    def __init__(self, x, y, width, height, font, small_font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.small_font = small_font
    
    def draw(self, screen, model):
        pygame.draw.rect(screen, (35, 35, 35), self.rect, border_radius=5)
        pygame.draw.rect(screen, (70, 70, 70), self.rect, 1, border_radius=5)
        
        if not model:
            no_sel = self.small_font.render("Sélectionnez un modèle", True, (120, 120, 120))
            no_rect = no_sel.get_rect(center=self.rect.center)
            screen.blit(no_sel, no_rect)
            return
        
        meta = model["metadata"]
        y = self.rect.y + 10
        x = self.rect.x + 10
        line_h = 18
        
        title = self.font.render("Informations", True, (100, 180, 100))
        screen.blit(title, (x, y))
        y += 28
        
        if meta.created_at:
            date_str = meta.created_at[:10] if meta.created_at else "?"
            lines = [
                f"Date: {date_str}",
                f"Grille: {meta.grid_size}x{meta.grid_size}",
                f"Itérations: {meta.iterations}",
                f"Population: {meta.population}",
                f"Sélection: {meta.selection}",
                f"Crossover: {meta.crossover}",
                f"Mutation: {meta.mutation}",
                f"Parties/éval: {meta.nb_games}",
                f"Neurones: {meta.hidden_layer}",
                f"Performance: {meta.best_score:.4f}",
                f"Temps: {meta.training_time}s",
            ]
        else:
            lines = [
                "Aucune métadonnée",
                "Modèle ancien ou",
                "créé manuellement"
            ]
        
        for line in lines:
            text = self.small_font.render(line, True, (180, 180, 180))
            screen.blit(text, (x, y))
            y += line_h
