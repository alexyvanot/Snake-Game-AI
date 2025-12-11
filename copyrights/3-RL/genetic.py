import numpy
from NN_numpy import *
import concurrent.futures
from snake import *

def eval(sol, gameParams):
    sol.score = 0.0
    #TODO
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
    #TODO
    return NeuralNet(arch)
