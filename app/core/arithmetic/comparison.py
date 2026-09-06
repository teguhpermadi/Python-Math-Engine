import random
from typing import Literal
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result, to_latex

def generate_comparison(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType
) -> dict:
    """
    Menghasilkan soal perbandingan dua bilangan (>, <, =).
    """
    op1 = generate_number(number_type, level_config, rng)
    op2 = generate_number(number_type, level_config, rng)
    
    # Kadang-kadang buat sama agar ada variasi "="
    if rng.random() < 0.1:
        op2 = op1

    if op1 > op2:
        result = ">"
    elif op1 < op2:
        result = "<"
    else:
        result = "="
        
    op1_str = format_result(op1)
    op2_str = format_result(op2)
    
    # In LaTeX, we can use a box or dots for the empty space
    expression_latex = f"{to_latex(op1_str)} \\; \\square \\; {to_latex(op2_str)}"
    
    return {
        "operands": [op1_str, op2_str],
        "operation": "comparison",
        "expression": f"{op1_str} ___ {op2_str}",
        "expression_latex": expression_latex,
        "result": result,
        "result_type": "symbol",
        "steps": [f"Bandingkan {op1_str} dengan {op2_str}", f"Hasil: {op1_str} {result} {op2_str}"]
    }

def generate_ordering(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    count: int = 4,
    order: Literal["ascending", "descending"] = "ascending"
) -> dict:
    """
    Menghasilkan soal mengurutkan bilangan.
    """
    nums = []
    for _ in range(count):
        n = generate_number(number_type, level_config, rng)
        while n in nums: # Hindari duplikat agar lebih menantang
            n = generate_number(number_type, level_config, rng)
        nums.append(n)
        
    if order == "ascending":
        sorted_nums = sorted(nums)
    else:
        sorted_nums = sorted(nums, reverse=True)
        
    num_strs = [format_result(n) for n in nums]
    result_strs = [format_result(n) for n in sorted_nums]
    
    expression_latex = ", ".join([to_latex(s) for s in num_strs])
    
    return {
        "operands": num_strs,
        "operation": "ordering",
        "order_type": order,
        "expression": ", ".join(num_strs),
        "expression_latex": expression_latex,
        # Result berupa string (bukan list) agar aman untuk response schema
        # (correct_answer: str) dan to_latex(). Urutan tersimpan di "ordered".
        "result": ", ".join(result_strs),
        "ordered": result_strs,
        "result_type": "sequence",
        "steps": [f"Urutkan {order}: " + ", ".join(result_strs)]
    }
