import random
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result, get_result_type

def generate_multiplication(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    operand_count: int = 2
) -> dict:
    """
    Menghasilkan soal perkalian.
    """
    max_ops = level_config.max_operations + 1
    operand_count = min(max(2, operand_count), max_ops)

    operands = []
    # Untuk perkalian, kita mungkin ingin angka yang lebih kecil agar hasil tidak meledak
    # Namun untuk sekarang kita ikuti generator standar
    for _ in range(operand_count):
        operands.append(generate_number(number_type, level_config, rng))

    result = 1
    for o in operands:
        result *= o

    operand_strs = [format_result(o, number_type) for o in operands]
    expression = " × ".join(operand_strs) # Menggunakan simbol kali yang cantik
    
    return {
        "operands": operand_strs,
        "operation": "multiplication",
        "expression": expression,
        "result": format_result(result, number_type),
        "result_type": get_result_type(result),
        "steps": [f"{expression} = {format_result(result, number_type)}"]
    }
