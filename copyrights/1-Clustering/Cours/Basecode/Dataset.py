import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Dataset:
    def __init__(self, filename):
        X = []
        with open(filename, "r") as fichier:
            lignes = fichier.readlines()
            for ligne in lignes:
                X.append([float(ligne.split(" ")[0]), float(ligne.split(" ")[1])])
        self.X = np.array(X)
        self.X = (self.X - np.tile(self.X.mean(axis=0), (len(self.X), 1)))/(np.tile(self.X.std(axis=0), (len(self.X), 1)))
        print(self.X.mean(axis=0))
        print(self.X.std(axis=0))

    def trace(self, labels=None):
        x,y = self.X[:,0], self.X[:,1]
        if labels is None:
            plt.scatter(x, y)
        else:
            palette = list(mcolors.TABLEAU_COLORS.keys())
            colors = [palette[i] if i<len(palette) else palette[0] for i in labels]
            plt.scatter(x, y, c=colors)
        plt.show()
