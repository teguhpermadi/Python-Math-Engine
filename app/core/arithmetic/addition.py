import random
from fractions import Fraction
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result, get_result_type

def generate_addition(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    operand_count: int = 2
) -> dict:
    """
    Menghasilkan soal penjumlahan.
    """
    # Batasi operand_count
    max_ops = level_config.max_operations + 1
    operand_count = min(max(2, operand_count), max_ops)

    operands = []
    for _ in range(operand_count):
        operands.append(generate_number(number_type, level_config, rng))

    result = sum(operands)
    
    # Format operands for expression
    operand_strs = [format_result(o, number_type) for o in operands]
    expression = " + ".join(operand_strs)
    
    # Generate steps (simple for single operation)
    if operand_count == 2:
        steps = [f"{operand_strs[0]} + {operand_strs[1]} = {format_result(result, number_type)}"]
    else:
        steps = [f"Jumlahkan semua angka: {expression} = {format_result(result, number_type)}"]

    return {
        "operands": operand_strs,
        "operation": "addition",
        "expression": expression,
        "result": format_result(result, number_type),
        "result_type": get_result_type(result),
        "steps": steps
    }
