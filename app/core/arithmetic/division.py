import random
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result, get_result_type

def generate_division(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    result_type: NumberType | None = None
) -> dict:
    """
    Menghasilkan soal pembagian dengan hasil yang selalu bersih.
    Strategy: Backward Compute (Quotient * Divisor = Dividend)
    """
    # 1. Pilih pembagi (divisor)
    divisor = generate_number(number_type, level_config, rng)
    # Divisor tidak boleh 0
    while divisor == 0:
        divisor = generate_number(number_type, level_config, rng)

    # 2. Pilih hasil (quotient)
    target_type = result_type or number_type
    quotient = generate_number(target_type, level_config, rng)

    # 3. Hitung dividend
    dividend = quotient * divisor

    dividend_str = format_result(dividend)
    divisor_str = format_result(divisor)
    expression = f"{dividend_str} ÷ {divisor_str}"
    
    return {
        "operands": [dividend_str, divisor_str],
        "operation": "division",
        "expression": expression,
        "result": format_result(quotient),
        "result_type": get_result_type(quotient),
        "steps": [f"{expression} = {format_result(quotient)}"]
    }
