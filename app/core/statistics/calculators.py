import random
import statistics
from ..levels.config import LevelConfig

def generate_statistics_problem(rng: random.Random, level_config: LevelConfig):
    # Generate a list of numbers
    size = rng.randint(5, 10 + level_config.level)
    data = [rng.randint(1, level_config.level * 10) for _ in range(size)]
    
    mean = statistics.mean(data)
    median = statistics.median(data)
    try:
        mode = statistics.mode(data)
    except statistics.StatisticsError:
        mode = "Multiple/None"
        
    return {
        "dataset": data,
        "mean": round(mean, 2),
        "median": median,
        "mode": mode
    }
