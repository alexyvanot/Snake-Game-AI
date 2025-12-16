import sys
from src.gui.menu import ConfigMenu
from src.config.env import get_default_config, ENV_MODE
from src.config.runner import run

if __name__ == "__main__":
    if "--nogui" in sys.argv:
        config = get_default_config(ENV_MODE)
        if config:
            run(config)
    else:
        # Boucle principale avec retour au menu
        while True:
            menu = ConfigMenu()
            config = menu.run()
            
            if not config:
                break  # Quitter si le menu est fermé
            
            back_to_menu = run(config)
            if not back_to_menu:
                break  # Quitter si on ne veut pas retourner au menu

