import sympy
from fractions import Fraction
from ..number_types.registry import NumberType
from ..number_types.validators import classify_number

def format_result(val) -> str:
    """Mengubah nilai (int, float, Fraction) menjadi string yang ramah UI."""
    if isinstance(val, Fraction):
        if val.denominator == 1:
            return str(val.numerator)
        return f"{val.numerator}/{val.denominator}"
    if isinstance(val, float):
        # Hilangkan .0 jika itu integer
        if val.is_integer():
            return str(int(val))
        return str(val)
    return str(val)

def get_result_type(val) -> str:
    """Mengambil tipe bilangan yang paling spesifik untuk hasil."""
    labels = classify_number(val)
    # Urutan prioritas label: 
    # prime > composite > natural > whole > integer > fraction > mixed_fraction > decimal > real
    priority = [
        "prime", "composite", "natural", "whole", "integer_pos", "integer_neg", 
        "integer", "fraction", "mixed_fraction", "decimal", "real"
    ]
    for p in priority:
        if p in labels:
            return p
    return "real"

def simplify_fraction(f: Fraction) -> Fraction:
    """Memastikan pecahan disederhanakan (otomatis oleh Fraction sebenarnya)."""
    return f

def to_latex(expression: str) -> str:
    """Konversi sederhana ke LaTeX menggunakan SymPy."""
    if not expression:
        return ""
    
    import re
    
    # 0. Handle simple fractions like "1/2" directly to avoid SymPy evaluate=False quirks
    # (SymPy evaluate=False often turns 1/2 into 1 * \frac{1}{2})
    if re.match(r"^-?\d+/\d+$", expression.strip()):
        parts = expression.strip().split("/")
        return f"\\frac{{{parts[0]}}}{{{parts[1]}}}"
    
    # 1. Bersihkan expression dari simbol non-standar SymPy
    # × -> *, ÷ -> /, √ -> sqrt()
    expr_clean = expression.replace("×", " * ").replace("÷", " / ")
    
    # Handle √x -> sqrt(x). Ini sederhana, hanya untuk satu angka setelah √
    expr_clean = re.sub(r"√(\d+)", r"sqrt(\1)", expr_clean)
    # Jika sudah ada sqrt, pastikan ada kurung
    if "sqrt" in expr_clean and "(" not in expr_clean:
         expr_clean = expr_clean.replace("sqrt", "sqrt(") + ")"
    
    try:
        # 2. Gunakan SymPy sympify dengan evaluate=False agar struktur soal tetap terjaga
        parsed_expr = sympy.sympify(expr_clean, evaluate=False)
        
        # 3. Convert ke LaTeX dengan mul_symbol='times' agar 2*3 jadi 2 \times 3
        latex_str = sympy.latex(parsed_expr, mul_symbol='times')
        
        # 4. Cleanup: hapus "1 \times " yang sering muncul akibat evaluate=False pada pecahan
        latex_str = latex_str.replace("1 \\times ", "")
        
        return latex_str
    except Exception:
        # Fallback jika parsing gagal
        expr = expression.replace(" / ", " \\div ")
        expr = expr.replace(" * ", " \\times ")
        expr = expr.replace(" x ", " \\times ")
        return expr
