import pygame

def train_model(config):
    from src.core.snake import nbFeatures, nbActions, Game
    from src.gui.vue import SnakeVue
    from src.ai import genetic
    
    gameParams = {"nbGames": config["nb_games"], "height": config["grid_size"], "width": config["grid_size"]}
    arch = [nbFeatures, config["hidden_layer"], nbActions]
    
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

def play_model(config):
    from src.core.snake import Game
    from src.gui.vue import SnakeVue
    from src.ai.NN_numpy import NeuralNet
    import numpy as np
    
    nn = NeuralNet([8, 24, 4])
    nn.load(config["model_file"])
    
    vue = SnakeVue(config["grid_size"], config["grid_size"], 64)
    fps = pygame.time.Clock()
    
    try:
        while True:
            game = Game(config["grid_size"], config["grid_size"])
            while game.enCours:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                pred = np.argmax(nn.compute(game.getFeatures()))
                game.direction = pred
                game.refresh()
                if not game.enCours:
                    break
                vue.displayGame(game)
                fps.tick(config["fps"])
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()

def run(config):
    if config["mode"] == "train":
        train_model(config)
    else:
        play_model(config)
