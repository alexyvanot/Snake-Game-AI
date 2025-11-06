import numpy as np
import sys

from Dataset import *
from Kmeans import *

if __name__=='__main__':
    if len(sys.argv)!=2:
        print(f"Usage : python {sys.argv[0]} pathToData")
        sys.exit(0)

    dataset = Dataset(sys.argv[1])
    dataset.trace()
    kmeans = Kmeans(5)
    kmeans.fit(dataset.X, nbTries=30)
    print(kmeans.inertia)
    dataset.trace(labels=kmeans.labels)