import sympy
from fractions import Fraction
from ..number_types.registry import NumberType
from ..number_types.validators import classify_number

def format_result(val, number_type: NumberType | None = None) -> str:
    """Mengubah nilai (int, float, Fraction) menjadi string yang ramah UI."""
    if isinstance(val, Fraction):
        if val.denominator == 1:
            return str(val.numerator)
        
        # Jika diminta mixed_fraction atau jika nilai > 1 dan kita ingin otomatis (opsional)
        if number_type == NumberType.MIXED_FRACTION:
            whole = abs(val.numerator) // val.denominator
            remain = abs(val.numerator) % val.denominator
            sign = "-" if val.numerator < 0 else ""
            if whole == 0:
                return f"{sign}{remain}/{val.denominator}"
            if remain == 0:
                return f"{sign}{whole}"
            return f"{sign}{whole} {remain}/{val.denominator}"
            
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
    
    # 0. Handle mixed fractions "2 2/3" -> "2 \frac{2}{3}"
    # Cocokkan "angka spasi angka/angka" atau "-angka spasi angka/angka"
    mixed_pattern = r"(-?\d+)\s+(\d+)/(\d+)"
    if re.search(mixed_pattern, expression):
        expression = re.sub(mixed_pattern, r"\1 \\frac{\2}{\3}", expression)

    # 0.1 Handle simple fractions like "1/2" directly to avoid SymPy evaluate=False quirks
    if re.match(r"^-?\d+/\d+$", expression.strip()):
        parts = expression.strip().split("/")
        return f"\\frac{{{parts[0]}}}{{{parts[1]}}}"
    
    # 1. Bersihkan expression dari simbol non-standar SymPy
    # × -> *, ÷ -> /, √ -> sqrt()
    # Pastikan kita tidak merusak \frac yang mungkin sudah kita buat di atas
    expr_clean = expression.replace("×", " * ").replace("÷", " / ")
    
    # Handle √x -> sqrt(x)
    expr_clean = re.sub(r"√(\d+)", r"sqrt(\1)", expr_clean)
    if "sqrt" in expr_clean and "(" not in expr_clean:
         expr_clean = expr_clean.replace("sqrt", "sqrt(") + ")"
    
    try:
        # Jika ekspresi mengandung \frac, SymPy mungkin akan error jika disympify langsung.
        # Jadi jika kita sudah melakukan manual conversion untuk mixed, kita kembalikan saja.
        if "\\" in expression:
            return expression

        # 2. Gunakan SymPy sympify dengan evaluate=False
        parsed_expr = sympy.sympify(expr_clean, evaluate=False)
        
        # 3. Convert ke LaTeX
        latex_str = sympy.latex(parsed_expr, mul_symbol='times')
        
        # 4. Cleanup
        latex_str = re.sub(r"(?<!\d)1 \\times ", "", latex_str)
        
        return latex_str
    except Exception:
        expr = expression.replace(" / ", " \\div ")
        expr = expr.replace(" * ", " \\times ")
        expr = expr.replace(" x ", " \\times ")
        return expr
