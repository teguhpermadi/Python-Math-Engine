from dataclasses import dataclass, field
from ..number_types.registry import NumberType

@dataclass(frozen=True)
class LevelConfig:
    """
    Bundel konfigurasi untuk satu level.
    Bersifat immutable (frozen=True) — tidak boleh diubah saat runtime.
    """
    level: int

    # ── Rentang nilai integer ───────────────────────────────────────────────
    min_value: int            # Nilai minimum operand integer
    max_value: int            # Nilai maksimum operand integer

    # ── Konfigurasi desimal ─────────────────────────────────────────────────
    min_decimal: float        # Nilai minimum untuk bilangan desimal
    max_decimal: float        # Nilai maksimum untuk bilangan desimal
    decimal_places: int       # Jumlah digit di belakang koma

    # ── Konfigurasi pecahan ─────────────────────────────────────────────────
    allowed_denominators: list[int]  # Penyebut yang diizinkan
    max_mixed_whole: int      # Bagian bulat maks untuk pecahan campuran

    # ── Konfigurasi operasi campuran ────────────────────────────────────────
    max_operations: int       # Jumlah operasi maks dalam soal campuran
    allow_parentheses: bool   # Apakah boleh ada tanda kurung

    # ── Konfigurasi akar & pangkat ──────────────────────────────────────────
    max_exponent: int         # Eksponen maksimum (misal: x² → max_exponent=2)
    allowed_roots: list[int]  # Jenis akar yang diizinkan (misal: [2, 3] = √ dan ∛)

    # ── NumberType yang valid untuk level ini ───────────────────────────────
    allowed_number_types: list[NumberType]

    # ── Sub-tipe untuk NumberType.REAL ─────────────────────────────────────
    real_sub_types: list[NumberType] = field(default_factory=list)


LEVEL_REGISTRY: dict[int, LevelConfig] = {

    1: LevelConfig(
        level=1,
        min_value=1,            max_value=10,
        min_decimal=0.0,        max_decimal=0.0,    decimal_places=0,
        allowed_denominators=[],                    max_mixed_whole=0,
        max_operations=1,       allow_parentheses=False,
        max_exponent=1,         allowed_roots=[],
        allowed_number_types=[NumberType.NATURAL, NumberType.WHOLE],
        real_sub_types=[]
    ),

    2: LevelConfig(
        level=2,
        min_value=1,            max_value=50,
        min_decimal=0.0,        max_decimal=0.0,    decimal_places=0,
        allowed_denominators=[],                    max_mixed_whole=0,
        max_operations=1,       allow_parentheses=False,
        max_exponent=2,         allowed_roots=[2],
        allowed_number_types=[NumberType.NATURAL, NumberType.WHOLE, NumberType.PRIME],
        real_sub_types=[]
    ),

    3: LevelConfig(
        level=3,
        min_value=1,            max_value=100,
        min_decimal=0.1,        max_decimal=9.9,    decimal_places=1,
        allowed_denominators=[2, 4, 5, 10],         max_mixed_whole=5,
        max_operations=2,       allow_parentheses=False,
        max_exponent=2,         allowed_roots=[2],
        allowed_number_types=[
            NumberType.NATURAL, NumberType.WHOLE,
            NumberType.DECIMAL, NumberType.FRACTION,
        ],
        real_sub_types=[NumberType.NATURAL, NumberType.DECIMAL]
    ),

    4: LevelConfig(
        level=4,
        min_value=1,            max_value=500,
        min_decimal=0.01,       max_decimal=99.99,  decimal_places=2,
        allowed_denominators=[2, 3, 4, 5, 6, 8, 10], max_mixed_whole=10,
        max_operations=2,       allow_parentheses=True,
        max_exponent=3,         allowed_roots=[2, 3],
        allowed_number_types=[
            NumberType.NATURAL, NumberType.INTEGER, NumberType.INTEGER_NEG,
            NumberType.DECIMAL, NumberType.FRACTION, NumberType.MIXED_FRACTION,
            NumberType.PRIME, NumberType.COMPOSITE,
        ],
        real_sub_types=[NumberType.NATURAL, NumberType.DECIMAL, NumberType.FRACTION]
    ),

    5: LevelConfig(
        level=5,
        min_value=1,            max_value=1000,
        min_decimal=0.001,      max_decimal=999.999, decimal_places=3,
        allowed_denominators=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12], max_mixed_whole=20,
        max_operations=3,       allow_parentheses=True,
        max_exponent=4,         allowed_roots=[2, 3, 4],
        allowed_number_types=[
            NumberType.INTEGER, NumberType.INTEGER_NEG,
            NumberType.DECIMAL, NumberType.FRACTION, NumberType.MIXED_FRACTION,
            NumberType.PRIME, NumberType.COMPOSITE, NumberType.REAL,
        ],
        real_sub_types=[
            NumberType.INTEGER, NumberType.DECIMAL,
            NumberType.FRACTION, NumberType.MIXED_FRACTION,
        ]
    ),

    6: LevelConfig(
        level=6,
        min_value=1,            max_value=10_000,
        min_decimal=0.0001,     max_decimal=9999.9999, decimal_places=4,
        allowed_denominators=list(range(2, 21)),       max_mixed_whole=50,
        max_operations=4,       allow_parentheses=True,
        max_exponent=5,         allowed_roots=[2, 3, 4, 5],
        allowed_number_types=[NumberType.REAL, NumberType.INTEGER_NEG],
        real_sub_types=[
            NumberType.INTEGER, NumberType.INTEGER_NEG, NumberType.DECIMAL,
            NumberType.FRACTION, NumberType.MIXED_FRACTION,
        ]
    ),

    7: LevelConfig(
        level=7,
        min_value=1,            max_value=100_000,
        min_decimal=0.00001,    max_decimal=99999.99999, decimal_places=5,
        allowed_denominators=list(range(2, 51)),           max_mixed_whole=100,
        max_operations=5,       allow_parentheses=True,
        max_exponent=6,         allowed_roots=[2, 3, 4, 5, 6],
        allowed_number_types=[NumberType.REAL, NumberType.INTEGER_NEG],
        real_sub_types=[
            NumberType.INTEGER, NumberType.INTEGER_NEG, NumberType.DECIMAL,
            NumberType.FRACTION, NumberType.MIXED_FRACTION,
            NumberType.PRIME, NumberType.COMPOSITE,
        ]
    ),
}


def get_level_config(level: int) -> LevelConfig:
    """Mengambil LevelConfig dari registry. Raise error jika level tidak tersedia."""
    if level not in LEVEL_REGISTRY:
        raise ValueError(
            f"Level {level} tidak tersedia. Level yang valid: {sorted(LEVEL_REGISTRY.keys())}"
        )
    return LEVEL_REGISTRY[level]
