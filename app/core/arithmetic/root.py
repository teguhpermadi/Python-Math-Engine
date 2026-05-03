import random
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
from .utils import format_result, get_result_type

def generate_root(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    root_degree: int | None = None
) -> dict:
    """
    Menghasilkan soal penarikan akar.
    Strategy: Backward Compute (Result^Degree = Radicand)
    """
    if root_degree is None:
        if not level_config.allowed_roots:
            root_degree = 2 # Default kuadrat
        else:
            root_degree = rng.choice(level_config.allowed_roots)

    # 1. Pilih hasil (result) yang bersih (integer)
    # Batasi result agar radicand tidak meledak
    max_res = int(level_config.max_value ** (1/root_degree))
    if max_res < 2: max_res = 10
    
    res_val = rng.randint(2, max_res)
    
    # 2. Hitung radicand
    radicand = res_val ** root_degree
    
    symbol = "√" if root_degree == 2 else f"{root_degree}√"
    expression = f"{symbol}{radicand}"
    
    if root_degree == 2:
        expression_latex = f"\\sqrt{{{radicand}}}"
    else:
        expression_latex = f"\\sqrt[{root_degree}]{{{radicand}}}"
    
    return {
        "radicand": str(radicand),
        "root_degree": root_degree,
        "operation": "root",
        "expression": expression,
        "expression_latex": expression_latex,
        "result": str(res_val),
        "result_type": "natural",
        "steps": [f"{expression} = {res_val}"]
    }
