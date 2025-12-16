import numpy
from src.ai.NN_numpy import *
import concurrent.futures
from src.core.snake import *
import random
import pygame
from src.gui.game import SnakeVue, BackToMenuException, SaveAndExitException
from src.utils.time_estimator import TimeEstimator


def process_events(vue, status_text=""):
    """Traite les événements pygame et rafraîchit l'UI pendant les calculs"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise KeyboardInterrupt
        vue.handle_events(event)
    # refrshuui
    vue.draw_ui_only(status_text)


def eval(sol, gameParams):
    sol.score = 0.0
    
    nbGames = gameParams["nbGames"]
    H = gameParams["height"]
    W = gameParams["width"]

    total = 0.0

    for _ in range(nbGames):
        # nouvelle partie
        game = Game(H, W)

        # jusquau gameover
        while game.enCours:
            features = game.getFeatures() # vec8 features
            outputs = sol.nn.compute(features) #prediction
            action = int(numpy.argmax(outputs)) # direction choisi
            game.direction = action
            game.refresh()

        # partie fini on calc le score
        pommes = game.score - 4 # taille 4 au debut
        not_since_last_pomme = game.steps # step
        total += 1000 * pommes + not_since_last_pomme

    # normalisation entre 0 et 1
    sol.score = total / (nbGames * H * W * 1000.0)
    
    return (sol.id,sol.score)

class Individu:
    def __init__(self, nn, id):
        self.nn = nn
        self.id = id
        self.score = 0

    def clone(self, copie):
        for idx, layer in enumerate(copie.nn.layers[1:]):
            layer.bias = self.nn.layers[idx+1].bias.copy()
            layer.weights = self.nn.layers[idx+1].weights.copy()


def optimize(taillePopulation, tailleSelection, pc, mr, arch, gameParams, nbIterations):

    def crossover(parent1, parent2, pc):
        """Crossover entre deux individus selon le taux pc"""
        child1 = Individu(NeuralNet(arch), -1)
        child2 = Individu(NeuralNet(arch), -1)

        # check si clone
        if random.random() > pc:
            parent1.clone(child1)
            parent2.clone(child2)
            return child1, child2

        # crossover dans chaque couche
        for idx in range(1, len(parent1.nn.layers)):
            layer_p1 = parent1.nn.layers[idx]
            layer_p2 = parent2.nn.layers[idx]
            layer_c1 = child1.nn.layers[idx]
            layer_c2 = child2.nn.layers[idx]

            alpha = random.random()

            # poids
            layer_c1.weights = (
                alpha * layer_p1.weights + (1.0 - alpha) * layer_p2.weights
            )
            layer_c2.weights = (
                1.0 - alpha
            ) * layer_p1.weights + alpha * layer_p2.weights

            # biais
            layer_c1.bias = alpha * layer_p1.bias + (1.0 - alpha) * layer_p2.bias
            layer_c2.bias = (1.0 - alpha) * layer_p1.bias + alpha * layer_p2.bias

        return child1, child2

    def mutate(individu, mr):
        """Mutation de l'individu selon le taux mr"""
        nn = individu.nn
        for idx in range(1, len(nn.layers)):
            layer = nn.layers[idx]
            prev_layer = nn.layers[idx - 1]

            layerSize = layer.size
            previousLayerSize = prev_layer.size

            pm_bias = mr / float(layerSize)
            pm_weights = mr / float(previousLayerSize)

            # biais
            for j in range(layerSize):
                if random.random() < pm_bias:
                    layer.bias[j] += numpy.random.randn()

            # poids
            for j in range(layerSize):
                for i in range(previousLayerSize):
                    if random.random() < pm_weights:
                        layer.weights[j, i] += numpy.random.randn()

    # init population
    population = []
    next_id = 0
    for _ in range(taillePopulation):
        nn = NeuralNet(arch)
        indiv = Individu(nn, next_id)
        next_id += 1
        eval(indiv, gameParams)
        population.append(indiv)

    vue = SnakeVue(gameParams["height"], gameParams["width"], 64, is_training=True)
    fps = pygame.time.Clock()
    gameSpeed = 500
    
    # Estimateur de temps
    time_estimator = TimeEstimator(nbIterations)
    time_estimator.start()

    try:
        for it in range(nbIterations):
            status = f"Generation {it+1}/{nbIterations} - Calcul..."
                
            # event realtime
            process_events(vue, status)
            
            # sort par score 
            population.sort(key=lambda x: x.score, reverse=True)
            
            # update affichage stats avec temps estimé
            best_current = population[0].score if population else 0
            elapsed = time_estimator.get_elapsed()
            remaining = time_estimator.get_remaining_time()
            vue.update_training_stats(it + 1, nbIterations, best_current, taillePopulation, tailleSelection, elapsed, remaining)

            # on prend les meilleurs
            elites = population[:tailleSelection]

            # generation des nouveaux individus par crossover + mutation
            nouveaux = []
            nb_to_create = taillePopulation - tailleSelection
            while len(nouveaux) < nb_to_create:
                # event real time
                progress = len(nouveaux) * 100 // nb_to_create
                status = f"Gen {it+1}/{nbIterations} - Evaluation {progress}%"
                process_events(vue, status)
                
                parent1, parent2 = random.sample(elites, 2)

                child1, child2 = crossover(parent1, parent2, pc)
                mutate(child1, mr)
                mutate(child2, mr)

                child1.id = next_id
                next_id += 1
                child2.id = next_id
                next_id += 1

                eval(child1, gameParams)
                nouveaux.append(child1)

                if len(nouveaux) < nb_to_create:
                    eval(child2, gameParams)
                    nouveaux.append(child2)

            population = elites + nouveaux

            best = max(population, key=lambda x: x.score)
            
            # Mettre à jour l'estimateur de temps
            time_estimator.step(it + 1)
            
            # Afficher avec temps restant
            remaining_str = TimeEstimator.format_duration(time_estimator.get_remaining_time())
            print(f"Iteration {it+1}/{nbIterations} - Best score = {best.score:.4f} - Restant: {remaining_str}")

            # event demo
            process_events(vue, "Lancement demo...")

            demo_game = Game(gameParams["height"], gameParams["width"])
            vue.new_game()
            while demo_game.enCours:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise KeyboardInterrupt
                    vue.handle_events(event)
                features = demo_game.getFeatures()
                action = int(numpy.argmax(best.nn.compute(features)))
                demo_game.direction = action
                demo_game.refresh()
                if demo_game.enCours:
                    vue.displayGame(demo_game)
                    pygame.display.set_caption(f'Score = {len(demo_game.serpent)} | Gen {it+1}/{nbIterations} (Learning...)')
                    fps.tick(gameSpeed)
    except (KeyboardInterrupt, BackToMenuException):
        print("\nEntrainement interrompu")
    except SaveAndExitException:
        print("\nEntrainement interrompu - sauvegarde demandée")

    # recup auto_close avant de fermer
    auto_close = vue.auto_close

    # on recup le meilleur individu
    try:
        population.sort(key=lambda x: x.score, reverse=True)
        best = population[0]
        print(f"Meilleur score final : {best.score:.4f}")
    except (KeyboardInterrupt, IndexError):
        print("Interruption finale - retour d'un modèle par défaut")
        return NeuralNet(arch), 0.0, auto_close

    # on créé un nn avec les poids du meilleur individu
    try:
        original_init = NeuralNet.__init__

        def init_with_best(self, layerSizes):
            original_init(self, layerSizes)
            # copie des poids et biais du meilleur individu
            for idx, layer in enumerate(self.layers[1:]):
                layer.bias = best.nn.layers[idx + 1].bias.copy()
                layer.weights = best.nn.layers[idx + 1].weights.copy()

        NeuralNet.__init__ = init_with_best
        
        return NeuralNet(arch), best.score, auto_close
    except KeyboardInterrupt:
        print("Interruption lors de la création du modèle final")
        return NeuralNet(arch), best.score, auto_close
