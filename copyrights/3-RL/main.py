from snake import *
from vue import *
import genetic 

#les paramètres d'évaluation : les grilles sont en 10 par 10, et on joue 10 parties
gameParams={"nbGames":10, "height":10, "width":10}

#on procède à l'optimisation
nn = genetic.optimize(taillePopulation=400, tailleSelection=50, pc=0.8, mr=2.0, arch=[nbFeatures, 24, nbActions], gameParams=gameParams, nbIterations=1000)
#on enregistre le modèle obtenu, on pourra le recharger dans un autre code pour l'utiliser en inférence
nn.save("model.txt")

#on initialise l'interface graphique -> on va pouvoir observer les performances de notre réseau de neurones en direct
vue = SnakeVue(gameParams["height"], gameParams["width"], 64)
fps = pygame.time.Clock()
gameSpeed = 20

#Tant que l'on ne fait pas à Ctrl-C
while True:
    #On créé une partie avec les mêmes dimensions que lors de l'apprentissage
    game = Game(gameParams["height"], gameParams["width"])
    #Tant que la partie n'est pas finie, on joue (enfin pas nous, le réseau de neurones)
    while game.enCours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pred = np.argmax(nn.compute(game.getFeatures())) #on extrait les features de la partie, et on demande au réseau quelle direction choisir
        game.direction = pred #on joue la direction choisie par le réseau
        game.refresh()
        if not game.enCours: break
        vue.displayGame(game)
        fps.tick(gameSpeed)

