from src.ai.metadata import ModelMetadata


class GameStats:
    def __init__(self):
        self.reset()
        self.model_metadata = None
    
    def reset(self):
        self.games_played = 0
        self.total_apples = 0
        self.best_score = 0
        self.current_score = 0
        self.total_steps = 0
        self.current_game_apples = 0
    
    def load_model_metadata(self, model_filename):
        self.model_metadata = ModelMetadata.load(model_filename)
    
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
