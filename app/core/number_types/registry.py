from enum import Enum

class NumberType(str, Enum):
    """
    Semua tipe bilangan yang didukung engine.
    Nilai string digunakan langsung sebagai parameter API.
    """
    # ── Bilangan berbasis himpunan ──────────────────────────────────────────
    NATURAL        = "natural"        # Bilangan asli: {1, 2, 3, ...}
    WHOLE          = "whole"          # Bilangan cacah: {0, 1, 2, 3, ...}
    INTEGER        = "integer"        # Bilangan bulat: {..., -2, -1, 0, 1, 2, ...}
    INTEGER_POS    = "integer_pos"    # Bilangan bulat positif: {1, 2, 3, ...}
    INTEGER_NEG    = "integer_neg"    # Bilangan bulat negatif: {..., -3, -2, -1}
    REAL           = "real"           # Bilangan real (mencakup semua di bawah)

    # ── Bilangan berbasis sifat ─────────────────────────────────────────────
    PRIME          = "prime"          # Bilangan prima: {2, 3, 5, 7, 11, ...}
    COMPOSITE      = "composite"      # Bilangan komposit: {4, 6, 8, 9, 10, ...}

    # ── Bilangan berbasis representasi ─────────────────────────────────────
    DECIMAL        = "decimal"        # Desimal: 1.5, 3.14, 0.25
    FRACTION       = "fraction"       # Pecahan biasa: 1/2, 3/4, 5/6
    MIXED_FRACTION = "mixed_fraction" # Pecahan campuran: 1½, 2¾, 3⅓
