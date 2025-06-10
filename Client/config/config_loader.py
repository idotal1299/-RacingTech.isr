import json
import os

def load_config():
    path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(os.path.abspath(path), "r") as f:
        return json.load(f)
