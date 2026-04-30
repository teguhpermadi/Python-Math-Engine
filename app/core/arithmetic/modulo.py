import random
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result, get_result_type

def generate_modulo(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType
) -> dict:
    """
    Menghasilkan soal sisa bagi: dividend % divisor.
    """
    # Modulo biasanya untuk bilangan bulat
    if number_type not in [NumberType.NATURAL, NumberType.WHOLE, NumberType.INTEGER, NumberType.INTEGER_POS]:
        number_type = NumberType.NATURAL

    divisor = rng.randint(2, level_config.level * 5 + 3)
    dividend = generate_number(number_type, level_config, rng)
    
    # Pastikan dividend > divisor agar ada sisa atau kelipatan yang menarik
    if dividend < divisor:
        dividend += divisor * rng.randint(1, 5)

    result = dividend % divisor
    quotient = dividend // divisor
    
    dividend_str = format_result(dividend)
    divisor_str = format_result(divisor)
    expression = f"{dividend_str} mod {divisor_str}"
    
    return {
        "operands": [dividend_str, divisor_str],
        "operation": "modulo",
        "expression": expression,
        "result": str(result),
        "result_type": "whole",
        "steps": [
            f"{dividend_str} ÷ {divisor_str} = {quotient} sisa {result}",
            f"Jadi {dividend_str} mod {divisor_str} = {result}"
        ]
    }
