import os
import shutil
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
env_example_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env.example")

if not os.path.exists(env_path) and os.path.exists(env_example_path):
    shutil.copy(env_example_path, env_path)

load_dotenv(env_path)

ENV_MODEL_FILE = os.environ.get("SNAKE_MODEL_FILE", "model.txt")
ENV_ITERATIONS = int(os.environ.get("SNAKE_ITERATIONS", "1000"))
ENV_POPULATION = int(os.environ.get("SNAKE_POPULATION", "400"))
ENV_SELECTION = int(os.environ.get("SNAKE_SELECTION", "50"))
ENV_CROSSOVER = float(os.environ.get("SNAKE_CROSSOVER", "0.8"))
ENV_MUTATION = float(os.environ.get("SNAKE_MUTATION", "2.0"))
ENV_GRID_SIZE = int(os.environ.get("SNAKE_GRID_SIZE", "10"))
ENV_NB_GAMES = int(os.environ.get("SNAKE_NB_GAMES", "10"))
ENV_FPS = int(os.environ.get("SNAKE_FPS", "20"))
ENV_HIDDEN_LAYER = int(os.environ.get("SNAKE_HIDDEN_LAYER", "24"))
ENV_MODE = os.environ.get("SNAKE_MODE", "train")

def get_train_config():
    return {
        "mode": "train",
        "model_file": ENV_MODEL_FILE,
        "iterations": ENV_ITERATIONS,
        "population": ENV_POPULATION,
        "selection": ENV_SELECTION,
        "crossover": ENV_CROSSOVER,
        "mutation": ENV_MUTATION,
        "grid_size": ENV_GRID_SIZE,
        "nb_games": ENV_NB_GAMES,
        "hidden_layer": ENV_HIDDEN_LAYER
    }

def get_play_config():
    return {
        "mode": "play",
        "model_file": ENV_MODEL_FILE,
        "fps": ENV_FPS,
        "grid_size": ENV_GRID_SIZE
    }

def get_default_config(mode="train"):
    if mode == "train":
        return get_train_config()
    return get_play_config()
