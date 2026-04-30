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
    """Konversi sederhana ke LaTeX (bisa dikembangkan)."""
    expr = expression.replace(" / ", " \\div ")
    expr = expr.replace(" * ", " \\times ")
    expr = expr.replace(" x ", " \\times ")
    # Handle fractions a/b -> \frac{a}{b}
    # This is a very basic implementation
    return expr
