import random
import math
from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.geometry.shapes import (
    generate_cube, generate_block, generate_sphere, 
    generate_pyramid, generate_prism,
    generate_square, generate_rectangle, generate_circle, generate_triangle
)
from app.core.geometry.mesh import (
    generate_cube_mesh, generate_block_mesh,
    generate_pyramid_mesh, generate_prism_mesh,
    generate_rectangle_2d_mesh, generate_polygon_2d_mesh
)
from app.services.ai_storyteller import ai_storyteller

def get_available_shapes():
    """
    Mengembalikan daftar semua bangun datar (2D) dan bangun ruang (3D) yang didukung.
    """
    return {
        "2D": ["square", "rectangle", "triangle", "circle"],
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
        shapes = ["square", "rectangle", "triangle"]
        if level >= 3: shapes.append("circle")
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
