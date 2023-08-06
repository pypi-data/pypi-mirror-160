import numpy as np
import json
import os

dir = os.path.dirname(__file__)

def build_path(path):
    return os.path.join(dir, path)

def load_lib(path):
    path = build_path(path)

    with open(path, "rb") as f:
        brands = np.load(f)
        return brands

def load_json_lib(path):
    path = build_path(path)
    with open(path, 'r') as f:
        return json.load(f)