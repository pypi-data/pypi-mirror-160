import numpy as np
import json


def load_lib(path):
    with open(path, "rb") as f:
        brands = np.load(f)
        return brands

def load_json_lib(path):
    with open(path, 'r') as f:
        return json.load(f)