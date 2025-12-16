# GUI package - Organized by screen/functionality
#
# Structure:
# - shared/    : Composants de base réutilisables (Button, InputField, Panel, Checkbox)
# - menu/      : Menu de configuration principal  
# - game/      : Vue du jeu Snake (entraînement + preview)
# - training/  : Écran de fin d'entraînement
#
# Imports principaux pour compatibilité:
from src.gui.menu import ConfigMenu
from src.gui.game import SnakeVue, BackToMenuException, GameStats
from src.gui.training import EndTrainingScreen