from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.measurement.generator import generate_conversion_problem
from app.services.ai_storyteller import ai_storyteller
from app.services.distractor import generate_distractors

async def generate_measurement_question(
    seed: int,
    level: int,
    with_story: bool = False,
    with_distractors: bool = True,
    distractor_count: int = 3,
):
    ctx = SeedContext(seed=seed, operation="measurement", level=level, number_type="natural")
    rng = SeedManager(ctx).rng
    config = get_level_config(level)
    
    data = generate_conversion_problem(rng, config)
    
    story = None
    if with_story:
        story = await ai_storyteller.generate_story(
            data["expression"], 
            data["result"], 
            "measurement", 
            "sehari-hari", 
            rng
        )

    correct_answer = str(data["result"])

    # Distractors
    answer_choices = [correct_answer]
    if with_distractors:
        dists = generate_distractors(correct_answer, "measurement", "natural", distractor_count, rng, "measurement", {"value": data.get("value")})
        answer_choices.extend(dists)
    rng.shuffle(answer_choices)

    return {
        "status": "success",
        "meta": {"seed": seed, "level": level, "operation": "measurement", "type": "measurement"},
        "context": {"story": story, "theme": "sehari-hari"},
        "data": {
            "expression": data["expression"],
            "expression_latex": data["expression"],
            "answer_choices": answer_choices,
            "answer_choices_latex": answer_choices,
            "correct_answer": correct_answer,
            "correct_answer_latex": correct_answer,
            "story": story,
            "details": data
        }
    }
