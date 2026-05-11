import math
import random
from dataclasses import dataclass
from ..levels.config import LevelConfig

@dataclass
class GeometricResult:
    shape: str
    dimensions: dict
    area: float | None = None
    volume: float | None = None
    perimeter: float | None = None

def generate_cube(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    side = rng.randint(1, level_config.level * 5)
    return GeometricResult(
        shape="cube",
        dimensions={"side": side},
        volume=side ** 3,
        area=6 * (side ** 2)
    )

def generate_block(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    l = rng.randint(2, level_config.level * 5)
    w = rng.randint(1, l - 1)
    h = rng.randint(1, level_config.level * 4)
    return GeometricResult(
        shape="block",
        dimensions={"length": l, "width": w, "height": h},
        volume=l * w * h,
        area=2 * (l*w + l*h + w*h)
    )

def generate_sphere(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    radius = rng.randint(1, level_config.level * 3)
    return GeometricResult(
        shape="sphere",
        dimensions={"radius": radius},
        volume=(4/3) * math.pi * (radius ** 3),
        area=4 * math.pi * (radius ** 2)
    )

def _get_polygon_area(n: int, side: float) -> float:
    """Menghitung luas poligon beraturan dengan n sisi."""
    return (n * side**2) / (4 * math.tan(math.pi / n))

def generate_pyramid(rng: random.Random, level_config: LevelConfig, sides: int = 4) -> GeometricResult:
    side_length = rng.randint(2, level_config.level * 4)
    height = rng.randint(2, level_config.level * 5)
    base_area = _get_polygon_area(sides, side_length)
    return GeometricResult(
        shape="pyramid",
        dimensions={"sides": sides, "side_length": side_length, "height": height},
        volume=(1/3) * base_area * height,
        area=base_area + (sides * 0.5 * side_length * height) # Estimasi luas selimut sederhana
    )

def generate_prism(rng: random.Random, level_config: LevelConfig, sides: int = 3) -> GeometricResult:
    side_length = rng.randint(2, level_config.level * 4)
    height = rng.randint(2, level_config.level * 5)
    base_area = _get_polygon_area(sides, side_length)
    return GeometricResult(
        shape="prism",
        dimensions={"sides": sides, "side_length": side_length, "height": height},
        volume=base_area * height,
        area=(2 * base_area) + (sides * side_length * height)
    )

# ── 2D SHAPES ───────────────────────────────────────────────────────────────

def generate_square(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    side = rng.randint(2, level_config.level * 10)
    return GeometricResult(
        shape="square",
        dimensions={"side": side},
        area=side ** 2,
        perimeter=4 * side
    )

def generate_rectangle(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    l = rng.randint(3, level_config.level * 10)
    w = rng.randint(2, l - 1)
    return GeometricResult(
        shape="rectangle",
        dimensions={"length": l, "width": w},
        area=l * w,
        perimeter=2 * (l + w)
    )

def generate_circle(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    radius = rng.randint(1, level_config.level * 7)
    return GeometricResult(
        shape="circle",
        dimensions={"radius": radius},
        area=math.pi * (radius ** 2),
        perimeter=2 * math.pi * radius
    )

def generate_triangle(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    # Segitiga siku-siku sederhana
    base = rng.randint(2, level_config.level * 8)
    height = rng.randint(2, level_config.level * 8)
    hypotenuse = round(math.sqrt(base**2 + height**2), 2)
    return GeometricResult(
        shape="triangle",
        dimensions={"base": base, "height": height},
        area=0.5 * base * height,
        perimeter=round(base + height + hypotenuse, 2)
    )


# ── NEW 2D SHAPES ──────────────────────────────────────────────────────────

def generate_right_triangle(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    base = rng.randint(2, level_config.level * 8)
    height = rng.randint(2, level_config.level * 8)
    hypotenuse = round(math.sqrt(base**2 + height**2), 2)
    return GeometricResult(
        shape="right_triangle",
        dimensions={"base": base, "height": height, "hypotenuse": hypotenuse},
        area=round(0.5 * base * height, 2),
        perimeter=round(base + height + hypotenuse, 2)
    )


def generate_equilateral_triangle(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    side = rng.randint(2, level_config.level * 8)
    height = round((math.sqrt(3) / 2) * side, 2)
    area = round((math.sqrt(3) / 4) * side**2, 2)
    return GeometricResult(
        shape="equilateral_triangle",
        dimensions={"side": side, "height": height},
        area=area,
        perimeter=round(3 * side, 2)
    )


def generate_isosceles_triangle(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    base = rng.randint(2, level_config.level * 8)
    min_leg = base // 2 + 1
    leg = rng.randint(min_leg, level_config.level * 8)
    height = round(math.sqrt(leg**2 - (base / 2)**2), 2)
    area = round(0.5 * base * height, 2)
    return GeometricResult(
        shape="isosceles_triangle",
        dimensions={"base": base, "leg": leg, "height": height},
        area=area,
        perimeter=round(2 * leg + base, 2)
    )


def generate_scalene_triangle(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    max_val = level_config.level * 8
    while True:
        a = rng.randint(2, max_val)
        b = rng.randint(2, max_val)
        c = rng.randint(2, max_val)
        sides = sorted([a, b, c])
        if sides[0] + sides[1] > sides[2] and len({a, b, c}) == 3:
            break
    s = (a + b + c) / 2
    area = round(math.sqrt(s * (s - a) * (s - b) * (s - c)), 2)
    return GeometricResult(
        shape="scalene_triangle",
        dimensions={"side_a": a, "side_b": b, "side_c": c},
        area=area,
        perimeter=round(a + b + c, 2)
    )


def _classify_triangle_by_sides(a: int, b: int, c: int) -> str:
    sides = sorted([a, b, c])
    a2, b2, c2 = sides[0]**2, sides[1]**2, sides[2]**2
    if a2 + b2 == c2:
        return "right"
    elif a2 + b2 > c2:
        return "acute"
    else:
        return "obtuse"


def _generate_triangle_by_type(rng: random.Random, level_config: LevelConfig, target_type: str):
    max_val = level_config.level * 8
    for _ in range(200):
        a = rng.randint(2, max_val)
        b = rng.randint(2, max_val)
        c = rng.randint(2, max_val)
        sides = sorted([a, b, c])
        if sides[0] + sides[1] <= sides[2]:
            continue
        if _classify_triangle_by_sides(a, b, c) == target_type:
            return a, b, c
    return None


def generate_acute_triangle(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    result = _generate_triangle_by_type(rng, level_config, "acute")
    if result is None:
        side = level_config.level * 3
        a = b = c = side
    else:
        a, b, c = result
    s = (a + b + c) / 2
    area = round(math.sqrt(s * (s - a) * (s - b) * (s - c)), 2)
    return GeometricResult(
        shape="acute_triangle",
        dimensions={"side_a": a, "side_b": b, "side_c": c},
        area=area,
        perimeter=round(a + b + c, 2)
    )


def generate_obtuse_triangle(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    result = _generate_triangle_by_type(rng, level_config, "obtuse")
    if result is None:
        a = b = level_config.level * 2
        c = level_config.level * 5
    else:
        a, b, c = result
    s = (a + b + c) / 2
    area = round(math.sqrt(s * (s - a) * (s - b) * (s - c)), 2)
    return GeometricResult(
        shape="obtuse_triangle",
        dimensions={"side_a": a, "side_b": b, "side_c": c},
        area=area,
        perimeter=round(a + b + c, 2)
    )


def generate_parallelogram(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    base = rng.randint(3, level_config.level * 8)
    side = rng.randint(2, level_config.level * 6)
    max_h = min(side, level_config.level * 6)
    height = rng.randint(2, max_h)
    return GeometricResult(
        shape="parallelogram",
        dimensions={"base": base, "side": side, "height": height},
        area=round(base * height, 2),
        perimeter=round(2 * (base + side), 2)
    )


def generate_right_trapezoid(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    a = rng.randint(2, level_config.level * 5)
    b = rng.randint(a + 1, a + level_config.level * 5)
    height = rng.randint(2, level_config.level * 6)
    slant = round(math.sqrt(height**2 + (b - a)**2), 2)
    return GeometricResult(
        shape="right_trapezoid",
        dimensions={"base_a": a, "base_b": b, "height": height, "slant": slant},
        area=round(0.5 * (a + b) * height, 2),
        perimeter=round(a + b + height + slant, 2)
    )


def generate_isosceles_trapezoid(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    a = rng.randint(2, level_config.level * 5)
    b = rng.randint(a + 2, a + level_config.level * 6)
    min_leg = (b - a) // 2 + 1
    leg = rng.randint(min_leg, level_config.level * 6)
    diff = (b - a) / 2
    height = round(math.sqrt(leg**2 - diff**2), 2)
    return GeometricResult(
        shape="isosceles_trapezoid",
        dimensions={"base_a": a, "base_b": b, "leg": leg, "height": height},
        area=round(0.5 * (a + b) * height, 2),
        perimeter=round(a + b + 2 * leg, 2)
    )


def generate_kite(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    d1 = rng.randint(4, level_config.level * 8)
    p = rng.randint(2, d1 - 2)
    t = rng.randint(2, level_config.level * 6)
    d2 = 2 * t
    side1 = round(math.sqrt(p**2 + t**2), 2)
    side2 = round(math.sqrt((d1 - p)**2 + t**2), 2)
    return GeometricResult(
        shape="kite",
        dimensions={"diagonal_1": d1, "diagonal_2": d2},
        area=round(0.5 * d1 * d2, 2),
        perimeter=round(2 * (side1 + side2), 2)
    )


def generate_rhombus(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    d1 = rng.randint(4, level_config.level * 8)
    d2 = rng.randint(4, level_config.level * 8)
    side = round(math.sqrt((d1 / 2)**2 + (d2 / 2)**2), 2)
    return GeometricResult(
        shape="rhombus",
        dimensions={"diagonal_1": d1, "diagonal_2": d2, "side": side},
        area=round(0.5 * d1 * d2, 2),
        perimeter=round(4 * side, 2)
    )


def generate_ellipse(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    a = rng.randint(3, level_config.level * 7)
    b = rng.randint(2, a)
    perimeter_approx = round(math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b))), 2)
    return GeometricResult(
        shape="ellipse",
        dimensions={"semi_major": a, "semi_minor": b},
        area=round(math.pi * a * b, 2),
        perimeter=perimeter_approx
    )


def generate_pentagon(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    side = rng.randint(2, level_config.level * 6)
    area = round((1 / 4) * math.sqrt(5 * (5 + 2 * math.sqrt(5))) * side**2, 2)
    return GeometricResult(
        shape="pentagon",
        dimensions={"side": side},
        area=area,
        perimeter=round(5 * side, 2)
    )


def generate_hexagon(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    side = rng.randint(2, level_config.level * 6)
    area = round((3 * math.sqrt(3) / 2) * side**2, 2)
    return GeometricResult(
        shape="hexagon",
        dimensions={"side": side},
        area=area,
        perimeter=round(6 * side, 2)
    )


def generate_octagon(rng: random.Random, level_config: LevelConfig) -> GeometricResult:
    side = rng.randint(2, level_config.level * 5)
    area = round(2 * (1 + math.sqrt(2)) * side**2, 2)
    return GeometricResult(
        shape="octagon",
        dimensions={"side": side},
        area=area,
        perimeter=round(8 * side, 2)
    )
