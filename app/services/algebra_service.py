from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.algebra.linear import generate_linear_equation

async def generate_algebra_question(seed: int, level: int):
    ctx = SeedContext(seed=seed, operation="algebra", level=level, number_type="natural")
    rng = SeedManager(ctx).rng
    config = get_level_config(level)
    
    data = generate_linear_equation(rng, config)
    
    # Simple blueprint for algebra
    blueprint = [
        {"step": 1, "desc": f"Kurangi kedua ruas dengan {data['b']}", "expr": f"{data['a']}x = {data['c']} - {data['b']}"},
        {"step": 2, "desc": f"Bagi kedua ruas dengan {data['a']}", "expr": f"x = {data['result']}"}
    ]
    if data['b'] == 0:
        blueprint = [{"step": 1, "desc": f"Bagi kedua ruas dengan {data['a']}", "expr": f"x = {data['result']}"}]

    return {
        "meta": {"seed": seed, "level": level, "type": "algebra"},
        "data": {
            "expression": data["expression"],
            "correct_answer": data["result"],
            "blueprint": blueprint
        }
    }
