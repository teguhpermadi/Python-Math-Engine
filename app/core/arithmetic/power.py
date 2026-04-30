import random
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result, get_result_type

def generate_power(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    exponent: int | None = None
) -> dict:
    """
    Menghasilkan soal perpangkatan.
    """
    if exponent is None:
        max_exp = level_config.max_exponent
        # Pangkat 0 hanya level 5+
        min_exp = 0 if level_config.level >= 5 else 1
        exponent = rng.randint(min_exp, max_exp)

    base = generate_number(number_type, level_config, rng)
    
    # Batasan agar hasil tidak terlalu besar untuk UI
    # Jika hasil > max_value * 100, kita coba generate ulang base
    result = base ** exponent
    
    # Simple check for very large numbers
    max_safe = level_config.max_value * 1000
    if isinstance(result, (int, float)) and result > max_safe:
        # Perkecil base jika terlalu besar
        base = rng.randint(1, 10)
        result = base ** exponent

    base_str = format_result(base)
    # Gunakan simbol superscript untuk exponent jika kecil
    superscripts = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
    exp_str = "".join(superscripts.get(c, c) for c in str(exponent))
    
    expression = f"{base_str}{exp_str}"
    
    return {
        "base": base_str,
        "exponent": str(exponent),
        "operation": "power",
        "expression": expression,
        "result": format_result(result),
        "result_type": get_result_type(result),
        "steps": [f"{base_str}^{exponent} = {format_result(result)}"]
    }
