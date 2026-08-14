from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.algebra.linear import generate_linear_equation
from app.services.distractor import generate_distractors

async def generate_algebra_question(
    seed: int,
    level: int,
    with_distractors: bool = True,
    distractor_count: int = 3,
):
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

    correct_answer = str(data["result"])

    # Distractors
    answer_choices = [correct_answer]
    if with_distractors:
        dists = generate_distractors(correct_answer, "algebra", "natural", distractor_count, rng, "algebra", {"a": data.get("a")})
        answer_choices.extend(dists)
    rng.shuffle(answer_choices)

    expression = data["expression"]

    return {
        "status": "success",
        "meta": {"seed": seed, "level": level, "operation": "algebra", "type": "algebra"},
        "context": {"story": None, "theme": "general"},
        "data": {
            "expression": expression,
            "expression_latex": expression,
            "answer_choices": answer_choices,
            "answer_choices_latex": answer_choices,
            "correct_answer": correct_answer,
            "correct_answer_latex": correct_answer,
            "blueprint": blueprint
        }
    }
