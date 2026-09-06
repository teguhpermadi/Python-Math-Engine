import random
from sympy import gcd, lcm, factorint
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result

def generate_gcd_problem(
    rng: random.Random,
    level_config: LevelConfig
) -> dict:
    """
    Menghasilkan soal FPB (Faktor Persekutuan Terbesar).
    """
    # Strategi: pilih GCD target dulu
    gcd_target = rng.randint(2, level_config.level * 4)
    
    # Pilih multiplier yang saling prima (coprime) agar GCD tidak berubah
    m1 = rng.randint(1, 10)
    m2 = rng.randint(1, 10)
    while gcd(m1, m2) != 1 or m1 == m2:
        m2 = rng.randint(1, 10)
        
    op1 = gcd_target * m1
    op2 = gcd_target * m2
    
    # Sort agar manis
    nums = sorted([op1, op2])
    
    return {
        "operands": [str(n) for n in nums],
        "operation": "gcd",
        "expression": f"FPB dari {nums[0]} dan {nums[1]}",
        "result": str(gcd_target),
        "result_type": "natural",
        "steps": [
            f"Faktor dari {nums[0]} dan {nums[1]}",
            f"FPB = {gcd_target}"
        ]
    }

def generate_lcm_problem(
    rng: random.Random,
    level_config: LevelConfig
) -> dict:
    """
    Menghasilkan soal KPK (Kelipatan Persekutuan Terkecil).
    """
    # Pilih dua angka kecil
    op1 = rng.randint(2, level_config.level * 5)
    op2 = rng.randint(2, level_config.level * 5)
    while op1 == op2:
        op2 = rng.randint(2, level_config.level * 5)
        
    res = lcm(op1, op2)
    
    nums = sorted([op1, op2])
    
    return {
        "operands": [str(n) for n in nums],
        "operation": "lcm",
        "expression": f"KPK dari {nums[0]} dan {nums[1]}",
        "result": str(res),
        "result_type": "natural",
        "steps": [
            f"Kelipatan dari {nums[0]} dan {nums[1]}",
            f"KPK = {res}"
        ]
    }

def generate_factorization_problem(
    rng: random.Random,
    level_config: LevelConfig
) -> dict:
    """
    Menghasilkan soal faktorisasi prima.
    """
    num = rng.randint(10, level_config.max_value)
    factors = factorint(num)
    
    # Format: 2^2 * 3
    parts = []
    for p, e in sorted(factors.items()):
        if e > 1:
            parts.append(f"{p}^{e}")
        else:
            parts.append(str(p))
    
    result = " x ".join(parts)
    
    return {
        "operand": str(num),
        "operation": "factorization",
        "expression": f"Faktorisasi prima dari {num}",
        "result": result,
        "result_type": "expression",
        "steps": [f"Pohon faktor dari {num} menghasilkan {result}"]
    }
