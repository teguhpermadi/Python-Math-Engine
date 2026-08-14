from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.statistics.calculators import generate_statistics_problem
from app.services.distractor import generate_distractors

async def generate_statistics_question(
    seed: int,
    level: int,
    with_distractors: bool = True,
    distractor_count: int = 3,
):
    ctx = SeedContext(seed=seed, operation="statistics", level=level, number_type="natural")
    rng = SeedManager(ctx).rng
    config = get_level_config(level)
    
    data = generate_statistics_problem(rng, config)
    
    # Pick one measure as the question target
    measures = ["mean", "median", "mode"]
    target_measure = rng.choice(measures)
    correct_answer = str(data[target_measure])

    expression = f"Diberikan data: {data['dataset']}. Tentukan nilai {target_measure.capitalize()} dari data tersebut."

    # Distractors: use other measures + off-by-one
    context = {"results": {"mean": str(data["mean"]), "median": str(data["median"]), "mode": str(data["mode"])}}
    answer_choices = [correct_answer]
    if with_distractors:
        dists = generate_distractors(correct_answer, target_measure, "natural", distractor_count, rng, "statistics", context)
        answer_choices.extend(dists)
    rng.shuffle(answer_choices)

    return {
        "status": "success",
        "meta": {"seed": seed, "level": level, "operation": "statistics", "type": "statistics"},
        "context": {"story": None, "theme": "general"},
        "data": {
            "expression": expression,
            "expression_latex": expression,
            "answer_choices": answer_choices,
            "answer_choices_latex": answer_choices,
            "correct_answer": correct_answer,
            "correct_answer_latex": correct_answer,
            "dataset": data["dataset"],
            "results": {
                "mean": data["mean"],
                "median": data["median"],
                "mode": data["mode"]
            }
        }
    }
