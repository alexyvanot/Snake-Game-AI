import numpy as np
from Metrics import *

'''
Implémentation de l'algorithme Kmeans
'''
class Kmeans:
    '''
    On commence par enregistrer K, et déclarer les centroïdes (vides)
    '''
    def __init__(self, K):
        self.centroids = None
        self.labels = None
        self.K = K
        self.inertia = 1e9

    '''
    TODO : Procédure d'apprentissage, on cherche à générer les K centroïdes approximant le mieux les données
    '''
    def fit(self, X, nbTries=10):
        return None

    '''
    TODO : Méthode qui prend une instance non connue, et retourne l'indice du centroïde le plus proche
    '''
    def predict(self, Xi):
        return -1

