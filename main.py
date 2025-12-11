import sys
from src.gui.menu import ConfigMenu
from src.config.env import get_default_config, ENV_MODE
from src.config.runner import run

if __name__ == "__main__":
    if "--nogui" in sys.argv:
        config = get_default_config(ENV_MODE)
    else:
        menu = ConfigMenu()
        config = menu.run()
    
    if config:
        run(config)

