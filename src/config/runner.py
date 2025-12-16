import pygame
import time

def train_model(config):
    from src.core.snake import nbFeatures, nbActions, Game
    from src.gui.vue import SnakeVue
    from src.gui.events import BackToMenuException
    from src.gui.end_training import EndTrainingScreen
    from src.ai import genetic
    from src.ai.metadata import ModelMetadata
    
    gameParams = {"nbGames": config["nb_games"], "height": config["grid_size"], "width": config["grid_size"]}
    arch = [nbFeatures, config["hidden_layer"], nbActions]
    
    start_time = time.time()
    
    try:
        nn, best_score, auto_close = genetic.optimize(
            taillePopulation=config["population"],
            tailleSelection=config["selection"],
            pc=config["crossover"],
            mr=config["mutation"],
            arch=arch,
            gameParams=gameParams,
            nbIterations=config["iterations"]
        )
        
        training_time = int(time.time() - start_time)
        
        metadata = ModelMetadata()
        metadata.set_training_params(config)
        metadata.set_performance(best_score, training_time)
        
        pygame.quit()
        
        # Si auto_close, sauvegarder et quitter directement
        if auto_close:
            model_file = config["model_file"]
            if not model_file.endswith('.txt'):
                model_file += '.txt'
            nn.save(model_file)
            metadata.save(model_file)
            print(f"\nModèle sauvegardé automatiquement: {model_file}")
            return False  # Quitter l'application
        
        end_screen = EndTrainingScreen(nn, config["grid_size"], config["model_file"], metadata)
        result = end_screen.run()
        
        if result is None or result["action"] == "quit":
            return False
        elif result["action"] == "menu":
            return True
        elif result["action"] == "preview":
            preview_config = {
                "mode": "play",
                "model_file": result["model_file"],
                "grid_size": result["grid_size"],
                "fps": 15
            }
            return play_model(preview_config)
        
        return False
    except BackToMenuException:
        pygame.quit()
        return True

def play_model(config):
    from src.core.snake import Game
    from src.gui.vue import SnakeVue
    from src.gui.events import BackToMenuException
    from src.ai.NN_numpy import NeuralNet
    import numpy as np
    
    nn = NeuralNet([8, 24, 4])
    nn.load(config["model_file"])
    
    vue = SnakeVue(config["grid_size"], config["grid_size"], 64, config["model_file"])
    fps = pygame.time.Clock()
    
    try:
        while True:
            game = Game(config["grid_size"], config["grid_size"])
            vue.new_game()
            while game.enCours:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return False
                    vue.handle_back_button(event)
                pred = np.argmax(nn.compute(game.getFeatures()))
                game.direction = pred
                game.refresh()
                if not game.enCours:
                    break
                vue.displayGame(game)
                fps.tick(config["fps"])
    except BackToMenuException:
        pygame.quit()
        return True
    except KeyboardInterrupt:
        pygame.quit()
        return False

def run(config):
    if config["mode"] == "train":
        return train_model(config)
    else:
        return play_model(config)
