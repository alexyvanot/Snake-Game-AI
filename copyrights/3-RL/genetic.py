import numpy
from NN_numpy import *
import concurrent.futures
from snake import *
import random
import pygame
from vue import SnakeVue

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

    vue = SnakeVue(gameParams["height"], gameParams["width"], 64)
    fps = pygame.time.Clock()
    gameSpeed = 500

    try:
        for it in range(nbIterations):
            # sort par score 
            population.sort(key=lambda x: x.score, reverse=True)

            # on prend les meilleurs
            elites = population[:tailleSelection]

            # generation des nouveaux individus par crossover + mutation
            nouveaux = []
            while len(elites) + len(nouveaux) < taillePopulation:
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

                if len(elites) + len(nouveaux) < taillePopulation:
                    eval(child2, gameParams)
                    nouveaux.append(child2)

            population = elites + nouveaux

            best = max(population, key=lambda x: x.score)
            print(f"Iteration {it+1}/{nbIterations} - Best score = {best.score:.4f}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt

            demo_game = Game(gameParams["height"], gameParams["width"])
            while demo_game.enCours:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise KeyboardInterrupt
                features = demo_game.getFeatures()
                action = int(numpy.argmax(best.nn.compute(features)))
                demo_game.direction = action
                demo_game.refresh()
                if demo_game.enCours:
                    vue.displayGame(demo_game)
                    pygame.display.set_caption(f'Score = {len(demo_game.serpent)} | Gen {it+1}/{nbIterations} (Learning...)')
                    fps.tick(gameSpeed)
    except KeyboardInterrupt:
        print("\nEntrainement interrompu (Ctrl-C)")

    # on recup le meilleur individu
    population.sort(key=lambda x: x.score, reverse=True)
    best = population[0]
    print(f"Meilleur score final : {best.score:.4f}")

    # on créé un nn avec les poids du meilleur individu
    original_init = NeuralNet.__init__

    def init_with_best(self, layerSizes):
        original_init(self, layerSizes)
        # copie des poids et biais du meilleur individu
        for idx, layer in enumerate(self.layers[1:]):
            layer.bias = best.nn.layers[idx + 1].bias.copy()
            layer.weights = best.nn.layers[idx + 1].weights.copy()

    NeuralNet.__init__ = init_with_best
    
    return NeuralNet(arch)
