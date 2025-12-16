import json
import os
from datetime import datetime

META_MARKER = "# META: "


class ModelMetadata:
    def __init__(self):
        self.created_at = None
        self.iterations = 0
        self.population = 0
        self.selection = 0
        self.crossover = 0.0
        self.mutation = 0.0
        self.grid_size = 0
        self.nb_games = 0
        self.hidden_layer = 0
        self.best_score = 0.0
        self.training_time = 0
    
    def set_training_params(self, config):
        self.created_at = datetime.now().isoformat()
        self.iterations = config.get("iterations", 0)
        self.population = config.get("population", 0)
        self.selection = config.get("selection", 0)
        self.crossover = config.get("crossover", 0.0)
        self.mutation = config.get("mutation", 0.0)
        self.grid_size = config.get("grid_size", 0)
        self.nb_games = config.get("nb_games", 0)
        self.hidden_layer = config.get("hidden_layer", 0)
    
    def set_performance(self, best_score, training_time=0):
        self.best_score = best_score
        self.training_time = training_time
    
    def to_dict(self):
        return {
            "created_at": self.created_at,
            "training": {
                "iterations": self.iterations,
                "population": self.population,
                "selection": self.selection,
                "crossover": self.crossover,
                "mutation": self.mutation,
                "nb_games": self.nb_games,
                "hidden_layer": self.hidden_layer
            },
            "environment": {
                "grid_size": self.grid_size
            },
            "performance": {
                "best_score": self.best_score,
                "training_time": self.training_time
            }
        }
    
    def from_dict(self, data):
        self.created_at = data.get("created_at")
        training = data.get("training", {})
        self.iterations = training.get("iterations", 0)
        self.population = training.get("population", 0)
        self.selection = training.get("selection", 0)
        self.crossover = training.get("crossover", 0.0)
        self.mutation = training.get("mutation", 0.0)
        self.nb_games = training.get("nb_games", 0)
        self.hidden_layer = training.get("hidden_layer", 0)
        env = data.get("environment", {})
        self.grid_size = env.get("grid_size", 0)
        perf = data.get("performance", {})
        self.best_score = perf.get("best_score", 0.0)
        self.training_time = perf.get("training_time", 0)
        return self
    
    def save(self, model_filename):
        if not os.path.exists(model_filename):
            return
        
        with open(model_filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        lines = [l for l in lines if not l.startswith(META_MARKER)]
        
        meta_json = json.dumps(self.to_dict(), separators=(',', ':'))
        lines.append(f"{META_MARKER}{meta_json}\n")
        
        with open(model_filename, "w", encoding="utf-8") as f:
            f.writelines(lines)
    
    @staticmethod
    def load(model_filename):
        metadata = ModelMetadata()
        if not os.path.exists(model_filename):
            return metadata
        
        try:
            with open(model_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(META_MARKER):
                        json_str = line[len(META_MARKER):].strip()
                        data = json.loads(json_str)
                        metadata.from_dict(data)
                        break
        except (json.JSONDecodeError, IOError):
            pass
        
        return metadata
    
    @staticmethod
    def exists(model_filename):
        if not os.path.exists(model_filename):
            return False
        try:
            with open(model_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(META_MARKER):
                        return True
        except IOError:
            pass
        return False
