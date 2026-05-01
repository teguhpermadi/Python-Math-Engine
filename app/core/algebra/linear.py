import random
from ..levels.config import LevelConfig

def generate_linear_equation(rng: random.Random, level_config: LevelConfig):
    # ax + b = c
    # x = (c - b) / a
    
    # Generate x first for clean results
    x = rng.randint(1, level_config.level * 5)
    a = rng.randint(1, level_config.level + 2)
    b = rng.randint(0, level_config.level * 10)
    
    c = a * x + b
    
    # Choose display format
    # format 1: ax + b = c
    # format 2: ax = c - b
    expression = f"{a}x + {b} = {c}"
    if b == 0:
        expression = f"{a}x = {c}"
        
    return {
        "expression": expression,
        "variable": "x",
        "result": str(x),
        "a": a, "b": b, "c": c
    }
