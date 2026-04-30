import random
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result, get_result_type

def generate_subtraction(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    allow_negative_result: bool | None = None
) -> dict:
    """
    Menghasilkan soal pengurangan.
    """
    if allow_negative_result is None:
        # Level < 4 biasanya tidak menggunakan bilangan negatif
        allow_negative_result = level_config.level >= 4

    op1 = generate_number(number_type, level_config, rng)
    op2 = generate_number(number_type, level_config, rng)

    # Constraint: Hasil tidak negatif untuk level rendah
    if not allow_negative_result:
        if op1 < op2:
            op1, op2 = op2, op1 # Swap agar hasil positif

    result = op1 - op2
    
    op1_str = format_result(op1)
    op2_str = format_result(op2)
    expression = f"{op1_str} - {op2_str}"
    
    return {
        "operands": [op1_str, op2_str],
        "operation": "subtraction",
        "expression": expression,
        "result": format_result(result),
        "result_type": get_result_type(result),
        "steps": [f"{expression} = {format_result(result)}"]
    }
