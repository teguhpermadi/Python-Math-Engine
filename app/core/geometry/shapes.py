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
    hypotenuse = math.sqrt(base**2 + height**2)
    return GeometricResult(
        shape="triangle",
        dimensions={"base": base, "height": height},
        area=0.5 * base * height,
        perimeter=base + height + hypotenuse
    )
