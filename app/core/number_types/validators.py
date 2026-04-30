from fractions import Fraction
from sympy import isprime as sympy_isprime

def is_prime(n: int) -> bool:
    return n > 1 and sympy_isprime(n)

def is_composite(n: int) -> bool:
    return n > 1 and not sympy_isprime(n)

def is_whole(n) -> bool:
    return isinstance(n, int) and n >= 0

def is_natural(n) -> bool:
    return isinstance(n, int) and n >= 1

def is_proper_fraction(f: Fraction) -> bool:
    """Pecahan biasa: 0 < f < 1"""
    return 0 < f < 1

def is_mixed_fraction(f: Fraction) -> bool:
    """Pecahan campuran: f > 1 dan bukan integer"""
    return f > 1 and f.denominator != 1

def classify_number(n) -> list[str]:
    """
    Mengklasifikasikan satu angka ke semua NumberType yang berlaku.
    Returns: list label yang berlaku, misal: ["natural", "whole", "integer_pos", "prime"]
    """
    labels = []
    if isinstance(n, int):
        if n > 0:
            labels += ["natural", "whole", "integer", "integer_pos"]
            if is_prime(n):    labels.append("prime")
            if is_composite(n): labels.append("composite")
        elif n == 0:
            labels += ["whole", "integer"]
        else:
            labels += ["integer", "integer_neg"]
    elif isinstance(n, Fraction):
        if is_proper_fraction(n):  labels.append("fraction")
        if is_mixed_fraction(n):   labels.append("mixed_fraction")
    elif isinstance(n, float):
        labels.append("decimal")
    labels.append("real")  # Semua bilangan adalah real
    return labels
