import random
from fractions import Fraction
from dataclasses import dataclass
from typing import Literal, Any, cast
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

@dataclass
class MixedNode:
    value: Any
    op: OperationName | None = None
    left: 'MixedNode | None' = None
    right: 'MixedNode | None' = None
    is_leaf: bool = True

def generate_mixed_operations(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    operation_count: int | None = None,
    with_parentheses: bool | None = None,
    allowed_operations: list[str] | None = None
) -> dict:
    """
    Menghasilkan soal operasi campuran multi-step (sampai 5 operasi) menggunakan Tree-based generation.
    Menjamin BODMAS dan hasil bersih di setiap step.
    """
    # 1. Tentukan jumlah operasi
    max_ops_level = level_config.max_operations
    if operation_count is None or operation_count < 1:
        # Default 2-3 ops jika level memungkinkan
        operation_count = rng.randint(min(2, max_ops_level), min(5, max(2, max_ops_level)))
    else:
        operation_count = min(5, operation_count)

    # 2. Tentukan kolam operasi
    valid_ops_all: list[OperationName] = ["addition", "subtraction", "multiplication", "division", "power", "root", "modulo"]
    if allowed_operations:
        ops_pool = [cast(OperationName, op) for op in allowed_operations if op in valid_ops_all]
        if not ops_pool: ops_pool = ["addition", "subtraction"]
    else:
        ops_pool = ["addition", "subtraction"]
        if level_config.level >= 2:
            ops_pool += ["multiplication", "division", "power", "root"]
        if level_config.level >= 3:
            ops_pool += ["modulo"]

    # 3. Build Tree (Backward Strategy)
    # Mulai dengan hasil akhir (root)
    root_val = generate_number(number_type, level_config, rng)
    root = MixedNode(value=root_val)
    
    nodes_to_split = [root]
    current_ops = 0
    
    while current_ops < operation_count and nodes_to_split:
        # Bias: Pilih node secara acak, tapi jika ingin lebih banyak tanda kurung
        # kita bisa memilih node yang "dalam" atau "seimbang".
        # Untuk sekarang, acak saja sudah cukup menghasilkan berbagai struktur.
        idx = rng.randrange(len(nodes_to_split))
        node = nodes_to_split.pop(idx)
        
        # Pilih operasi. Untuk level tinggi, beri bobot lebih ke perkalian/pembagian
        # agar memicu kurung pada penjumlahan di bawahnya.
        op = rng.choice(ops_pool)
        
        # Split node.value menjadi left_val [op] right_val
        left_val, right_val = _split_value(node.value, op, number_type, level_config, rng)
        
        node.op = op
        node.is_leaf = False
        node.left = MixedNode(value=left_val)
        node.right = MixedNode(value=right_val)
        
        nodes_to_split.append(node.left)
        nodes_to_split.append(node.right)
        current_ops += 1

    # 4. Generate Expression & Steps
    leaves = []
    _get_leaves(root, leaves)
    variables = []
    for i, leaf in enumerate(leaves):
        var_id = f"v{i+1}"
        leaf.var_id = var_id
        variables.append({"id": var_id, "value": format_result(leaf.value)})

    # Generate Expression string
    expression = _build_expression_string(root)
    expression_latex = _build_latex_string(root)
    
    # Generate Steps (Post-order traversal)
    steps = []
    _generate_steps(root, steps)

    return {
        "variables": variables,
        "operation": "mixed",
        "expression": expression,
        "expression_latex": expression_latex,
        "result": format_result(root.value),
        "result_type": get_result_type(root.value),
        "steps": steps
    }

def _split_value(target, op, number_type, level_config, rng):
    """Membagi target menjadi dua nilai berdasarkan operasi."""
    if op == "addition":
        # target = a + b
        b = generate_number(number_type, level_config, rng)
        a = target - b
        return a, b
    elif op == "subtraction":
        # target = a - b -> a = target + b
        b = generate_number(number_type, level_config, rng)
        a = target + b
        return a, b
    elif op == "multiplication":
        # target = a * b
        if isinstance(target, int) and target != 0:
            divisors = [d for d in range(1, abs(target) + 1) if target % d == 0]
            if not divisors:
                # Jika target=1 atau -1, fallback
                b = rng.choice([1, -1])
                a = target // b
            else:
                a = rng.choice(divisors)
                if rng.random() > 0.5: a = -a
                b = target // a
            return a, b
        else:
            b = generate_number(number_type, level_config, rng)
            if b == 0: b = 1
            a = target / b
            return a, b
    elif op == "division":
        # target = a / b -> a = target * b
        # Pastikan b tidak terlalu besar agar a tetap dalam range level
        b = rng.randint(1, 10) if isinstance(target, int) else generate_number(number_type, level_config, rng)
        if b == 0: b = 1
        a = target * b
        return a, b
    elif op == "power":
        # target = a ^ b. Kita cari b dulu, lalu a = target^(1/b)
        # Atau lebih mudah: b random [2, 3], a = target^(1/b) jika bulat
        # Untuk simplifikasi backward: kita batasi target harus positif
        if isinstance(target, int) and target > 1:
            possible_b = []
            for b in range(2, 6):
                a = round(target**(1/b), 8)
                if a.is_integer() and a > 1:
                    possible_b.append(b)
            if possible_b:
                b = rng.choice(possible_b)
                a = int(round(target**(1/b)))
                return a, b
        # Fallback: target = target^1 (tidak seru) atau pakai multiplication
        return target, 1
    elif op == "root":
        # target = b-th root of a -> a = target ^ b
        b = rng.choice(level_config.allowed_roots) if level_config.allowed_roots else 2
        a = target ** b
        return b, a
    elif op == "modulo":
        # target = a % b -> a = k*b + target
        b = rng.randint(target + 1, target + 10)
        k = rng.randint(1, 5)
        a = k * b + target
        return a, b
    return target, 0

def _get_leaves(node, leaves):
    if node.is_leaf:
        leaves.append(node)
    else:
        _get_leaves(node.left, leaves)
        _get_leaves(node.right, leaves)

def _build_expression_string(node):
    if node.is_leaf:
        return format_result(node.value)
    
    left_str = _build_expression_string(node.left)
    right_str = _build_expression_string(node.right)
    
    # Tambahkan kurung jika prioritas anak lebih rendah
    if not node.left.is_leaf and priority(node.left.op) < priority(node.op):
        left_str = f"({left_str})"
    
    # Case khusus untuk pengurangan dan pembagian di sebelah kanan
    # a - (b + c) -> kurung wajib
    # a / (b * c) -> kurung wajib
    if not node.right.is_leaf:
        if priority(node.right.op) < priority(node.op):
            right_str = f"({right_str})"
        elif priority(node.right.op) == priority(node.op) and node.op in ["subtraction", "division"]:
            right_str = f"({right_str})"

    return f"{left_str} {get_sym(node.op)} {right_str}"

def _build_latex_string(node):
    if node.is_leaf:
        val = node.value
        if isinstance(val, Fraction):
            if val.denominator == 1:
                return str(val.numerator)
            return f"\\frac{{{val.numerator}}}{{{val.denominator}}}"
        return format_result(val)
    
    left_str = _build_latex_string(node.left)
    right_str = _build_latex_string(node.right)
    
    if node.op == "power":
        return f"{{{left_str}}}^{{{right_str}}}"
    
    if node.op == "root":
        # left is degree, right is radicand
        degree = left_str
        radicand = right_str
        if degree == "2":
            return f"\\sqrt{{{radicand}}}"
        return f"\\sqrt[{degree}]{{{radicand}}}"
    
    if node.op == "division":
        # Render division as fraction in LaTeX for better visuals
        return f"\\frac{{{left_str}}}{{{right_str}}}"

    # Priority handling for other operators
    if not node.left.is_leaf and priority(node.left.op) < priority(node.op):
        left_str = f"\\left({left_str}\\right)"
    
    if not node.right.is_leaf:
        if priority(node.right.op) < priority(node.op):
            right_str = f"\\left({right_str}\\right)"
        elif priority(node.right.op) == priority(node.op) and node.op in ["subtraction", "division"]:
            right_str = f"\\left({right_str}\\right)"

    latex_ops = {
        "addition": "+",
        "subtraction": "-",
        "multiplication": "\\times",
        "modulo": "\\pmod"
    }
    
    op_sym = latex_ops.get(node.op, get_sym(node.op))
    return f"{left_str} {op_sym} {right_str}"

def _generate_steps(node, steps):
    if node.is_leaf:
        return node.var_id # Mengembalikan ID variabel atau ID step
    
    left_ref = _generate_steps(node.left, steps)
    right_ref = _generate_steps(node.right, steps)
    
    step_id = f"s{len(steps) + 1}"
    
    # Untuk nilai di expression step, gunakan hasil evaluasi real-nya
    left_val_s = format_result(node.left.value)
    right_val_s = format_result(node.right.value)
    
    steps.append({
        "step_id": step_id,
        "operation": node.op,
        "inputs": [left_ref, right_ref],
        "expression": f"{left_val_s} {get_sym(node.op)} {right_val_s}",
        "result": format_result(node.value)
    })
    
    node.step_ref = step_id
    return step_id

def eval_op(op, a, b):
    if op == "addition": return a + b
    if op == "subtraction": return a - b
    if op == "multiplication": return a * b
    if op == "division": return a // b
    if op == "power": return a ** b
    if op == "root": return a ** (1/b)
    if op == "modulo": return a % b
    return a

def get_sym(op):
    return {
        "addition": "+", "subtraction": "-", "multiplication": "×", "division": "÷",
        "power": "^", "root": "√", "modulo": "mod"
    }[op]

def priority(op):
    if op in ["power", "root"]: return 3
    if op in ["multiplication", "division", "modulo"]: return 2
    return 1
