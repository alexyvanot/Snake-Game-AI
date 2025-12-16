import pygame

def train_model(config):
    from src.core.snake import nbFeatures, nbActions, Game
    from src.gui.vue import SnakeVue
    from src.gui.events import BackToMenuException
    from src.ai import genetic
    
    gameParams = {"nbGames": config["nb_games"], "height": config["grid_size"], "width": config["grid_size"]}
    arch = [nbFeatures, config["hidden_layer"], nbActions]
    
    try:
        nn = genetic.optimize(
            taillePopulation=config["population"],
            tailleSelection=config["selection"],
            pc=config["crossover"],
            mr=config["mutation"],
            arch=arch,
            gameParams=gameParams,
            nbIterations=config["iterations"]
        )
        
        nn.save(config["model_file"])
        print(f"Modèle sauvegardé dans {config['model_file']}")
        return False  # Ne pas retourner au menu
    except BackToMenuException:
        return True  # Retourner au menu

def play_model(config):
    from src.core.snake import Game
    from src.gui.vue import SnakeVue
    from src.gui.events import BackToMenuException
    from src.ai.NN_numpy import NeuralNet
    import numpy as np
    
    nn = NeuralNet([8, 24, 4])
    nn.load(config["model_file"])
    
    vue = SnakeVue(config["grid_size"], config["grid_size"], 64)
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
        return True  # Retourner au menu
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
    return False

def run(config):
    if config["mode"] == "train":
        return train_model(config)
    else:
        return play_model(config)
