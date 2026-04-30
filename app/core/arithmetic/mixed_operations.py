import random
from dataclasses import dataclass
from typing import Literal, Any
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result, get_result_type

OperationName = Literal["addition", "subtraction", "multiplication", "division"]

@dataclass
class MixedStep:
    step_id: str
    operation: OperationName
    inputs: list[str] # v1, v2, s1, dst
    result: Any
    expression: str

def generate_mixed_operations(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    operation_count: int | None = None,
    with_parentheses: bool | None = None
) -> dict:
    """
    Menghasilkan soal operasi campuran multi-step.
    """
    if operation_count is None:
        operation_count = rng.randint(2, max(2, level_config.max_operations))
    
    if with_parentheses is None:
        with_parentheses = level_config.allow_parentheses

    # Untuk menyederhanakan Phase 3, kita buat 2-step saja dulu
    # v1 [op1] v2 [op2] v3
    
    ops: list[OperationName] = ["addition", "subtraction"]
    if level_config.level >= 2:
        ops += ["multiplication", "division"]
        
    op1 = rng.choice(ops)
    op2 = rng.choice(ops)
    
    # Backward strategy simplified for 2 steps:
    # Kita tentukan target hasil akhir dulu? Atau generate v1, v2, v3?
    # Agar aman dari pembagian by zero dan hasil kotor:
    
    v1 = generate_number(number_type, level_config, rng)
    v2 = generate_number(number_type, level_config, rng)
    
    # Pastikan op1 aman
    if op1 == "division":
        while v2 == 0 or (v1 % v2 != 0 if isinstance(v1, int) else False):
            v2 = rng.randint(1, 10)
            v1 = v2 * rng.randint(1, 10)
            
    s1_res = eval_op(op1, v1, v2)
    
    v3 = generate_number(number_type, level_config, rng)
    # Pastikan op2 aman
    if op2 == "division":
        while v3 == 0 or (s1_res % v3 != 0 if isinstance(s1_res, int) else False):
            v3 = rng.randint(1, 10)
            # Re-adjust s1_res to be multiple of v3 if needed? 
            # Better: generate v3 then adjust s1_res?
            # Simplest for now: just retry a few times
            pass
            
    final_res = eval_op(op2, s1_res, v3)
    
    v1_s, v2_s, v3_s = format_result(v1), format_result(v2), format_result(v3)
    sym1 = get_sym(op1)
    sym2 = get_sym(op2)
    
    # Handle Parentheses (BODMAS: Multi/Div > Add/Sub)
    # Jika op2 > op1 dalam hirarki tapi op1 harus dikerjakan dulu, beri kurung
    # Misal: (v1 + v2) * v3
    needs_parens = False
    if with_parentheses:
        if priority(op2) > priority(op1):
            needs_parens = True
            
    if needs_parens:
        expression = f"({v1_s} {sym1} {v2_s}) {sym2} {v3_s}"
    else:
        expression = f"{v1_s} {sym1} {v2_s} {sym2} {v3_s}"

    return {
        "variables": [
            {"id": "v1", "value": v1_s},
            {"id": "v2", "value": v2_s},
            {"id": "v3", "value": v3_s}
        ],
        "operation": "mixed",
        "expression": expression,
        "result": format_result(final_res),
        "result_type": get_result_type(final_res),
        "steps": [
            {"step_id": "s1", "operation": op1, "inputs": ["v1", "v2"], "expression": f"{v1_s} {sym1} {v2_s}", "result": format_result(s1_res)},
            {"step_id": "s2", "operation": op2, "inputs": ["s1", "v3"], "expression": f"{format_result(s1_res)} {sym2} {v3_s}", "result": format_result(final_res)}
        ]
    }

def eval_op(op, a, b):
    if op == "addition": return a + b
    if op == "subtraction": return a - b
    if op == "multiplication": return a * b
    if op == "division": return a // b # Assume clean for now
    return a

def get_sym(op):
    return {"addition": "+", "subtraction": "-", "multiplication": "×", "division": "÷"}[op]

def priority(op):
    if op in ["multiplication", "division"]: return 2
    return 1
