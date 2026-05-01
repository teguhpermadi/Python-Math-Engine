from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.measurement.generator import generate_conversion_problem
from app.services.ai_storyteller import ai_storyteller

async def generate_measurement_question(seed: int, level: int, with_story: bool = False):
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
        
    return {
        "meta": {"seed": seed, "level": level, "type": "measurement"},
        "data": {
            "expression": data["expression"],
            "story": story,
            "correct_answer": data["result"],
            "details": data
        }
    }
