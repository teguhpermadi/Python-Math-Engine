from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.statistics.calculators import generate_statistics_problem

async def generate_statistics_question(seed: int, level: int):
    ctx = SeedContext(seed=seed, operation="statistics", level=level, number_type="natural")
    rng = SeedManager(ctx).rng
    config = get_level_config(level)
    
    data = generate_statistics_problem(rng, config)
    
    expression = f"Diberikan data: {data['dataset']}. Hitung Mean, Median, dan Modus."

    return {
        "meta": {"seed": seed, "level": level, "type": "statistics"},
        "data": {
            "expression": expression,
            "dataset": data["dataset"],
            "results": {
                "mean": data["mean"],
                "median": data["median"],
                "mode": data["mode"]
            }
        }
    }
