class GameStats:
    """Statistiques de jeu en temps reel"""
    
    def __init__(self):
        self.reset()
        self.model_metadata = None
        # Données d'entraînement (mode training)
        self.training_data = None
    
    def reset(self):
        self.games_played = 0
        self.total_apples = 0
        self.best_score = 0
        self.current_score = 0
        self.total_steps = 0
        self.current_game_apples = 0
    
    def load_model_metadata(self, model_filename):
        """Charge les metadonnées d'un modele"""
        from src.ai.metadata import ModelMetadata
        self.model_metadata = ModelMetadata.load(model_filename)
    
    def set_training_data(self, generation, total_generations, best_algo_score, population_size, selection_size, elapsed_time=None, remaining_time=None):
        """Update les données d'entrainement"""
        self.training_data = {
            "generation": generation,
            "total_generations": total_generations,
            "best_algo_score": best_algo_score,
            "population": population_size,
            "selection": selection_size,
            "elapsed_time": elapsed_time,
            "remaining_time": remaining_time
        }
    
    def new_game(self):
        self.games_played += 1
        self.current_score = 0
        self.current_game_apples = 0
    
    def update(self, game):
        score = len(game.serpent)
        apples = score - 4
        
        if apples > self.current_game_apples:
            new_apples = apples - self.current_game_apples
            self.total_apples += new_apples
            self.current_game_apples = apples
        
        self.current_score = score
        self.total_steps += 1
        
        if score > self.best_score:
            self.best_score = score
    
    def get_avg_apples(self):
        if self.games_played == 0:
            return 0.0
        return self.total_apples / self.games_played
    
    def get_stats_lines(self):
        """Retourne les lignes de stats à afficher selon le mode"""
        lines = [
            f"Parties: {self.games_played}",
            f"Score: {self.current_score}",
            f"Pommes: {self.current_game_apples}",
            f"Meilleur: {self.best_score}",
            f"Moy pommes: {self.get_avg_apples():.1f}",
        ]
        
        # Mode training : afficher les infos d'apprentissage
        if self.training_data:
            from src.utils.time_estimator import TimeEstimator
            lines.append("")
            lines.append("--- Apprentissage ---")
            lines.append(f"Gen: {self.training_data['generation']}/{self.training_data['total_generations']}")
            lines.append(f"Best score: {self.training_data['best_algo_score']:.4f}")
            lines.append(f"Pop: {self.training_data['population']} | Sel: {self.training_data['selection']}")
            elapsed = TimeEstimator.format_duration(self.training_data.get('elapsed_time'))
            remaining = TimeEstimator.format_duration(self.training_data.get('remaining_time'))
            lines.append(f"Ecoulé: {elapsed}")
            lines.append(f"Restant: {remaining}")
        
        elif self.model_metadata and self.model_metadata.created_at:
            lines.append("")
            lines.append("--- Modèle ---")
            lines.append(f"Grille: {self.model_metadata.grid_size}x{self.model_metadata.grid_size}")
            lines.append(f"Iter: {self.model_metadata.iterations}")
            lines.append(f"Pop: {self.model_metadata.population}")
            lines.append(f"Perf: {self.model_metadata.best_score:.4f}")
            if self.model_metadata.training_time:
                lines.append(f"Temps: {self.model_metadata.training_time}s")
        
        return lines
