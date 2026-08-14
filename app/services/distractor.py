import random
import math
from typing import List, Optional


def generate_distractors(
    correct_answer: str,
    operation: str,
    number_type: str = "natural",
    count: int = 3,
    rng: random.Random = None,
    domain: str = "arithmetic",
    context: dict = None,
) -> List[str]:
    """
    Menghasilkan pilihan jawaban salah yang masuk akal berdasarkan domain.

    Args:
        correct_answer: Jawaban benar (string)
        operation: Operasi atau tipe soal (e.g. addition, cube, complementary)
        number_type: Tipe bilangan (natural, integer, etc.)
        count: Jumlah distractor yang diinginkan
        rng: Random generator deterministic
        domain: Domain soal (arithmetic, geometry, algebra, angles, measurement, statistics)
        context: Konteks tambahan (dimensi, satuan, dll)
    """
    if rng is None:
        rng = random.Random()
    if context is None:
        context = {}

    distractors = set()

    try:
        val = _parse_number(correct_answer)

        if domain == "geometry":
            distractors.update(_geometry_distractors(val, operation, context, rng))
        elif domain == "algebra":
            distractors.update(_algebra_distractors(val, operation, context, rng))
        elif domain == "angles":
            distractors.update(_angle_distractors(val, operation, context, rng))
        elif domain == "measurement":
            distractors.update(_measurement_distractors(val, operation, context, rng))
        elif domain == "statistics":
            distractors.update(_statistics_distractors(val, operation, context, rng))
        else:
            distractors.update(_arithmetic_distractors(val, operation, correct_answer, rng))
    except Exception:
        pass

    # Ensure correct answer is not in distractors
    distractors.discard(correct_answer)

    # Fill remaining with generic random values if needed
    while len(distractors) < count:
        if val is not None:
            offset = rng.randint(1, max(10, int(abs(val)) + 10))
            candidate = str(int(val) + offset if val == int(val) else round(val + offset * 0.1, 2))
            distractors.add(candidate)
        else:
            distractors.add(str(rng.randint(1, 100)))

    final_list = list(distractors)[:count]
    rng.shuffle(final_list)
    return final_list


def _parse_number(s: str) -> Optional[float]:
    """Parse a numeric string, return None if not parseable."""
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _arithmetic_distractors(val, operation, correct_answer, rng) -> set:
    """Original arithmetic distractor logic."""
    d = set()
    if val is not None:
        if val == int(val):
            v = int(val)
            d.add(str(v + 1))
            d.add(str(v - 1))
        else:
            d.add(str(round(val + 0.1, 2)))
            d.add(str(round(val - 0.1, 2)))

        if operation == "multiplication":
            d.add(str(int(val) + 10))

    if '/' in correct_answer:
        parts = correct_answer.split('/')
        if len(parts) == 2:
            num, den = int(parts[0]), int(parts[1])
            d.add(f"{num + 1}/{den}")
            d.add(f"{num}/{den + 1}")
            d.add(f"{num + 1}/{den + 1}")

    return d


def _geometry_distractors(val, shape, context, rng) -> set:
    """
    Geometry distractors: wrong formula, radius↔diameter confusion,
    forget 1/3 for pyramids/cones, wrong exponent.
    """
    d = set()
    if val is None:
        return d

    v = val

    # Wrong formula: use perimeter instead of area, area instead of volume
    # For area problems, a common mistake is to forget the formula
    # e.g., triangle: forget 1/2, circle: forget pi, etc.
    if shape in ("triangle", "right_triangle", "equilateral_triangle",
                 "isosceles_triangle", "scalene_triangle",
                 "acute_triangle", "obtuse_triangle"):
        # Mistake: base * height (forget /2)
        d.add(str(round(v * 2, 2)))
    elif shape in ("circle", "ellipse"):
        # Mistake: use diameter instead of radius (×4 for area, ×8 for volume)
        d.add(str(round(v * 4, 2)))
    elif shape in ("pyramid", "cone", "rectangular_pyramid", "right_triangular_pyramid"):
        # Mistake: forget 1/3 multiplier (treat as prism)
        d.add(str(round(v * 3, 2)))
    elif shape in ("hemisphere",):
        # Mistake: use full sphere formula instead of half
        d.add(str(round(v * 2, 2)))

    # Off-by-one in value
    if v == int(v):
        iv = int(v)
        d.add(str(iv + 1))
        d.add(str(iv - 1))
    else:
        d.add(str(round(v * 0.9, 2)))
        d.add(str(round(v * 1.1, 2)))

    # Confuse radius vs diameter
    d.add(str(round(v * 2, 2)))

    # Wrong exponent (squared vs cubed confusion)
    d.add(str(round(v * 1.5, 2)))

    return d


def _algebra_distractors(val, operation, context, rng) -> set:
    """
    Algebra distractors: wrong sign, off-by-one, divide by wrong coefficient.
    """
    d = set()
    if val is None:
        return d

    v = val

    # Off-by-one in solution
    if v == int(v):
        iv = int(v)
        d.add(str(iv + 1))
        d.add(str(iv - 1))
    else:
        d.add(str(round(v + 1, 2)))
        d.add(str(round(v - 1, 2)))

    # Wrong sign
    d.add(str(round(-v, 2)))

    # Partial solving: intermediate value
    a = context.get("a", None)
    if a and a != 0:
        d.add(str(round(v * a, 2)))  # Forgot to divide by a

    return d


def _angle_distractors(val, angle_type, context, rng) -> set:
    """
    Angle distractors: complement↔supplement swap, off-by-5/10 degrees.
    """
    d = set()
    if val is None:
        return d

    v = val

    # Complement ↔ supplement swap
    if angle_type == "complementary":
        d.add(str(180 - v))  # Mistook for supplementary
    elif angle_type == "supplementary":
        d.add(str(90 - v))   # Mistook for complementary
    else:
        d.add(str(90 - v))
        d.add(str(180 - v))

    # Off-by-5 and off-by-10
    d.add(str(int(v + 5)))
    d.add(str(int(v - 5)))
    d.add(str(int(v + 10)))
    d.add(str(int(v - 10)))

    # Same angle (no calculation)
    d.add(str(int(v)))

    return d


def _measurement_distractors(val, operation, context, rng) -> set:
    """
    Measurement distractors: inverse conversion, off-by-factor-of-10, identity.
    """
    d = set()
    if val is None:
        return d

    v = val

    # Inverse: multiply instead of divide (or vice versa)
    d.add(str(round(v * 10, 2)))
    d.add(str(round(v / 10, 2)))

    # Off by factor of 10 (common metric unit error)
    d.add(str(round(v * 100, 2)))
    d.add(str(round(v / 100, 2)))

    # Identity: value unchanged (no conversion applied)
    original = context.get("value", None)
    if original is not None:
        d.add(str(original))

    # Off-by-one
    if v == int(v):
        iv = int(v)
        d.add(str(iv + 1))
        d.add(str(iv - 1))

    return d


def _statistics_distractors(val, measure_type, context, rng) -> set:
    """
    Statistics distractors: swap mean↔median/mode, off-by-one rounding.
    """
    d = set()
    if val is None:
        return d

    v = val

    # Off-by-one rounding
    if isinstance(v, float):
        d.add(str(round(v + 0.1, 2)))
        d.add(str(round(v - 0.1, 2)))
        d.add(str(round(v + 1, 2)))
        d.add(str(round(v - 1, 2)))
    else:
        d.add(str(int(v) + 1))
        d.add(str(int(v) - 1))

    # Swap with other measures if available
    results = context.get("results", {})
    for other_measure, other_val in results.items():
        if other_measure != measure_type and other_val is not None:
            d.add(str(other_val))

    # Common wrong calculation
    d.add(str(round(v * 1.5, 2)))
    d.add(str(round(v * 0.5, 2)))

    return d
