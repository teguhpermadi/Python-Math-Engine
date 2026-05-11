import random
import math
from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.geometry.shapes import (
    generate_cube, generate_block, generate_sphere, 
    generate_pyramid, generate_prism,
    generate_square, generate_rectangle, generate_circle, generate_triangle,
    generate_right_triangle, generate_equilateral_triangle,
    generate_isosceles_triangle, generate_scalene_triangle,
    generate_acute_triangle, generate_obtuse_triangle,
    generate_parallelogram, generate_right_trapezoid,
    generate_isosceles_trapezoid, generate_kite, generate_rhombus,
    generate_ellipse, generate_pentagon, generate_hexagon, generate_octagon,
)
from app.core.geometry.mesh import (
    generate_cube_mesh, generate_block_mesh,
    generate_pyramid_mesh, generate_prism_mesh,
    generate_rectangle_2d_mesh, generate_polygon_2d_mesh,
    generate_right_triangle_2d_mesh, generate_equilateral_triangle_mesh,
    generate_isosceles_triangle_mesh, generate_scalene_triangle_mesh,
    generate_parallelogram_mesh, generate_trapezoid_mesh,
    generate_kite_mesh, generate_rhombus_mesh, generate_ellipse_mesh,
)
from app.services.ai_storyteller import ai_storyteller

def get_available_shapes():
    """
    Mengembalikan daftar semua bangun datar (2D) dan bangun ruang (3D) yang didukung.
    """
    return {
        "2D": [
            "square", "rectangle", "circle", "ellipse",
            "triangle", "right_triangle", "equilateral_triangle",
            "isosceles_triangle", "scalene_triangle",
            "acute_triangle", "obtuse_triangle",
            "parallelogram", "right_trapezoid", "isosceles_trapezoid",
            "kite", "rhombus",
            "pentagon", "hexagon", "octagon",
        ],
        "3D": ["cube", "block", "pyramid", "prism", "sphere"]
    }

async def generate_geometry_question(
    seed: int, 
    level: int, 
    shape_type: str | None = None, 
    with_story: bool = False,
    sides: int | None = None,
    dimension: str = "3D"
):
    ctx = SeedContext(seed=seed, operation="geometry", level=level, number_type="natural")
    rng = SeedManager(ctx).rng
    config = get_level_config(level)
    
    # 1. Pilih Bangun Berdasarkan Dimensi
    if dimension.upper() == "2D":
        shapes = [
            "square", "rectangle", "triangle", "right_triangle",
            "equilateral_triangle", "isosceles_triangle", "scalene_triangle",
            "parallelogram", "right_trapezoid", "isosceles_trapezoid",
            "kite", "rhombus",
        ]
        if level >= 3:
            shapes += ["circle", "ellipse", "pentagon", "hexagon", "octagon"]
        if level >= 4:
            shapes += ["acute_triangle", "obtuse_triangle"]
    else:
        shapes = ["cube", "block"]
        if level >= 3: shapes += ["pyramid", "prism"]
        if level >= 5: shapes.append("sphere")
    
    target_shape = shape_type or rng.choice(shapes)
    
    # 2. Generate Dimensi & Hasil
    if target_shape == "square":
        res = generate_square(rng, config)
        mesh = generate_rectangle_2d_mesh(res.dimensions["side"], res.dimensions["side"])
        expression = f"Hitung luas persegi dengan sisi {res.dimensions['side']}"
        correct_answer = str(res.area)
        
    elif target_shape == "rectangle":
        res = generate_rectangle(rng, config)
        mesh = generate_rectangle_2d_mesh(res.dimensions["length"], res.dimensions["width"])
        expression = f"Hitung luas persegi panjang (p={res.dimensions['length']}, l={res.dimensions['width']})"
        correct_answer = str(res.area)
        
    elif target_shape == "triangle":
        res = generate_triangle(rng, config)
        # Mesh segitiga siku-siku sederhana
        vertices = [[0,0,0], [res.dimensions["base"],0,0], [0,res.dimensions["height"],0]]
        mesh = {"vertices": vertices, "faces": [[0,1,2]]}
        expression = f"Hitung luas segitiga (alas={res.dimensions['base']}, tinggi={res.dimensions['height']})"
        correct_answer = f"{res.area:.1f}" if not res.area.is_integer() else str(int(res.area))

    elif target_shape == "circle":
        res = generate_circle(rng, config)
        mesh = generate_polygon_2d_mesh(32, res.dimensions["radius"])
        expression = f"Hitung luas lingkaran dengan jari-jari {res.dimensions['radius']}"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "ellipse":
        res = generate_ellipse(rng, config)
        mesh = generate_ellipse_mesh(res.dimensions["semi_major"], res.dimensions["semi_minor"])
        expression = f"Hitung luas elips (a={res.dimensions['semi_major']}, b={res.dimensions['semi_minor']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "right_triangle":
        res = generate_right_triangle(rng, config)
        d = res.dimensions
        mesh = generate_right_triangle_2d_mesh(d["base"], d["height"])
        expression = f"Hitung luas segitiga siku-siku (alas={d['base']}, tinggi={d['height']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "equilateral_triangle":
        res = generate_equilateral_triangle(rng, config)
        mesh = generate_equilateral_triangle_mesh(res.dimensions["side"])
        expression = f"Hitung luas segitiga sama sisi (sisi={res.dimensions['side']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "isosceles_triangle":
        res = generate_isosceles_triangle(rng, config)
        d = res.dimensions
        mesh = generate_isosceles_triangle_mesh(d["base"], d["height"])
        expression = f"Hitung luas segitiga sama kaki (alas={d['base']}, kaki={d['leg']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "scalene_triangle":
        res = generate_scalene_triangle(rng, config)
        d = res.dimensions
        mesh = generate_scalene_triangle_mesh(d["side_a"], d["side_b"], d["side_c"])
        expression = f"Hitung luas segitiga sembarang (sisi={d['side_a']}, {d['side_b']}, {d['side_c']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "acute_triangle":
        res = generate_acute_triangle(rng, config)
        d = res.dimensions
        mesh = generate_scalene_triangle_mesh(d["side_a"], d["side_b"], d["side_c"])
        expression = f"Hitung luas segitiga lancip (sisi={d['side_a']}, {d['side_b']}, {d['side_c']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "obtuse_triangle":
        res = generate_obtuse_triangle(rng, config)
        d = res.dimensions
        mesh = generate_scalene_triangle_mesh(d["side_a"], d["side_b"], d["side_c"])
        expression = f"Hitung luas segitiga tumpul (sisi={d['side_a']}, {d['side_b']}, {d['side_c']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "parallelogram":
        res = generate_parallelogram(rng, config)
        d = res.dimensions
        mesh = generate_parallelogram_mesh(d["base"], d["side"], d["height"])
        expression = f"Hitung luas jajargenjang (alas={d['base']}, tinggi={d['height']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "right_trapezoid":
        res = generate_right_trapezoid(rng, config)
        d = res.dimensions
        mesh = generate_trapezoid_mesh(d["base_a"], d["base_b"], d["height"], is_isosceles=False)
        expression = f"Hitung luas trapesium siku-siku (a={d['base_a']}, b={d['base_b']}, t={d['height']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "isosceles_trapezoid":
        res = generate_isosceles_trapezoid(rng, config)
        d = res.dimensions
        mesh = generate_trapezoid_mesh(d["base_a"], d["base_b"], d["height"])
        expression = f"Hitung luas trapesium sama kaki (a={d['base_a']}, b={d['base_b']}, t={d['height']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "kite":
        res = generate_kite(rng, config)
        d = res.dimensions
        mesh = generate_kite_mesh(d["diagonal_1"], d["diagonal_2"], d["diagonal_1"] / 2)
        expression = f"Hitung luas layang-layang (d1={d['diagonal_1']}, d2={d['diagonal_2']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "rhombus":
        res = generate_rhombus(rng, config)
        d = res.dimensions
        mesh = generate_rhombus_mesh(d["diagonal_1"], d["diagonal_2"])
        expression = f"Hitung luas belah ketupat (d1={d['diagonal_1']}, d2={d['diagonal_2']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "pentagon":
        res = generate_pentagon(rng, config)
        mesh = generate_polygon_2d_mesh(5, res.dimensions["side"] / (2 * math.sin(math.pi / 5)))
        expression = f"Hitung luas segi lima beraturan (sisi={res.dimensions['side']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "hexagon":
        res = generate_hexagon(rng, config)
        mesh = generate_polygon_2d_mesh(6, res.dimensions["side"] / (2 * math.sin(math.pi / 6)))
        expression = f"Hitung luas segi enam beraturan (sisi={res.dimensions['side']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "octagon":
        res = generate_octagon(rng, config)
        mesh = generate_polygon_2d_mesh(8, res.dimensions["side"] / (2 * math.sin(math.pi / 8)))
        expression = f"Hitung luas segi delapan beraturan (sisi={res.dimensions['side']})"
        correct_answer = f"{res.area:.2f}"

    elif target_shape == "cube":
        res = generate_cube(rng, config)
        mesh = generate_cube_mesh(res.dimensions["side"])
        expression = f"Hitung volume kubus dengan sisi {res.dimensions['side']}"
        correct_answer = str(res.volume)
    
    elif target_shape == "block":
        res = generate_block(rng, config)
        mesh = generate_block_mesh(res.dimensions["length"], res.dimensions["width"], res.dimensions["height"])
        expression = f"Hitung volume balok (p={res.dimensions['length']}, l={res.dimensions['width']}, t={res.dimensions['height']})"
        correct_answer = str(res.volume)
    
    elif target_shape == "pyramid":
        if sides is None: sides = rng.randint(3, 8)
        res = generate_pyramid(rng, config, sides=sides)
        mesh = generate_pyramid_mesh(sides, res.dimensions["side_length"], res.dimensions["height"])
        expression = f"Hitung volume limas segi-{sides} (s={res.dimensions['side_length']}, t={res.dimensions['height']})"
        correct_answer = f"{res.volume:.1f}" if not res.volume.is_integer() else str(int(res.volume))
    
    elif target_shape == "prism":
        if sides is None: sides = rng.randint(3, 8)
        res = generate_prism(rng, config, sides=sides)
        mesh = generate_prism_mesh(sides, res.dimensions["side_length"], res.dimensions["height"])
        expression = f"Hitung volume prisma segi-{sides} (s={res.dimensions['side_length']}, t={res.dimensions['height']})"
        correct_answer = f"{res.volume:.1f}" if not res.volume.is_integer() else str(int(res.volume))
    
    else: # Sphere
        res = generate_sphere(rng, config)
        mesh = {"type": "sphere", "radius": res.dimensions["radius"]}
        expression = f"Hitung volume bola dengan jari-jari {res.dimensions['radius']}"
        correct_answer = f"{res.volume:.2f}"

    # 3. AI Story (Optional)
    story = None
    if with_story:
        story = await ai_storyteller.generate_story(expression, str(correct_answer), "geometry", "sekolah", rng)

    return {
        "meta": {"seed": seed, "level": level, "shape": target_shape, "dimension": dimension.upper()},
        "data": {
            "expression": expression,
            "story": story,
            "mesh": mesh,
            "dimensions": res.dimensions,
            "correct_answer": str(correct_answer)
        }
    }
