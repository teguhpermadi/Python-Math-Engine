import random
import math
from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.geometry.shapes import (
    generate_cube, generate_block, generate_sphere, 
    generate_pyramid, generate_prism,
    generate_cylinder, generate_cone, generate_hemisphere,
    generate_frustum, generate_torus, generate_ellipsoid,
    generate_tetrahedron, generate_hollow_sphere,
    generate_octahedron, generate_dodecahedron, generate_icosahedron,
    generate_right_triangular_prism, generate_isosceles_triangular_prism,
    generate_parallelogram_prism, generate_trapezoidal_prism,
    generate_rhombus_prism, generate_kite_prism,
    generate_rectangular_pyramid, generate_right_triangular_pyramid,
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
    generate_sphere_mesh, generate_cylinder_mesh, generate_cone_mesh,
    generate_hemisphere_mesh, generate_frustum_mesh,
    generate_torus_mesh, generate_ellipsoid_mesh,
    generate_tetrahedron_mesh, generate_octahedron_mesh,
    generate_dodecahedron_mesh, generate_icosahedron_mesh,
    _extrude_mesh, _pyramidize_mesh,
    generate_rectangle_2d_mesh, generate_polygon_2d_mesh,
    generate_right_triangle_2d_mesh, generate_equilateral_triangle_mesh,
    generate_isosceles_triangle_mesh, generate_scalene_triangle_mesh,
    generate_parallelogram_mesh, generate_trapezoid_mesh,
    generate_kite_mesh, generate_rhombus_mesh, generate_ellipse_mesh,
)
from app.services.ai_storyteller import ai_storyteller

from app.core.geometry.voxel import (
    create_voxel_group_data,
    generate_voxel_group_mesh,
    generate_voxel_group_options
)


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
        "3D": [
            "cube", "block", "pyramid", "prism", "sphere",
            "cylinder", "cone", "hemisphere", "frustum",
            "torus", "ellipsoid", "tetrahedron", "hollow_sphere",
            "octahedron", "dodecahedron", "icosahedron",
            "right_triangular_prism", "isosceles_triangular_prism",
            "parallelogram_prism", "trapezoidal_prism",
            "rhombus_prism", "kite_prism",
            "rectangular_pyramid", "right_triangular_pyramid",
            "voxel_group"
        ]
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
        if level >= 3: shapes += ["pyramid", "prism", "cylinder", "cone", "tetrahedron", "right_triangular_prism", "parallelogram_prism", "rectangular_pyramid", "right_triangular_pyramid", "voxel_group"]
        if level >= 4: shapes += ["hemisphere", "frustum", "octahedron", "isosceles_triangular_prism", "trapezoidal_prism", "rhombus_prism", "kite_prism"]
        if level >= 5: shapes += ["sphere", "torus", "ellipsoid", "dodecahedron", "icosahedron", "hollow_sphere"]
    
    if shape_type:
        available = get_available_shapes()
        dim_key = "2D" if dimension.upper() == "2D" else "3D"
        if shape_type not in available[dim_key]:
            raise ValueError(f"Shape '{shape_type}' is not available for {dim_key} dimension")

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
    
    elif target_shape == "sphere":
        res = generate_sphere(rng, config)
        mesh = generate_sphere_mesh(res.dimensions["radius"])
        expression = f"Hitung volume bola dengan jari-jari {res.dimensions['radius']}"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "cylinder":
        res = generate_cylinder(rng, config)
        d = res.dimensions
        mesh = generate_cylinder_mesh(d["radius"], d["height"])
        expression = f"Hitung volume tabung (r={d['radius']}, t={d['height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "cone":
        res = generate_cone(rng, config)
        d = res.dimensions
        mesh = generate_cone_mesh(d["radius"], d["height"])
        expression = f"Hitung volume kerucut (r={d['radius']}, t={d['height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "hemisphere":
        res = generate_hemisphere(rng, config)
        d = res.dimensions
        mesh = generate_hemisphere_mesh(d["radius"])
        expression = f"Hitung volume belahan bola (r={d['radius']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "frustum":
        res = generate_frustum(rng, config)
        d = res.dimensions
        mesh = generate_frustum_mesh(d["bottom_radius"], d["top_radius"], d["height"])
        expression = f"Hitung volume kerucut terpancung (R={d['bottom_radius']}, r={d['top_radius']}, t={d['height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "torus":
        res = generate_torus(rng, config)
        d = res.dimensions
        mesh = generate_torus_mesh(d["major_radius"], d["minor_radius"])
        expression = f"Hitung volume torus (R={d['major_radius']}, r={d['minor_radius']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "ellipsoid":
        res = generate_ellipsoid(rng, config)
        d = res.dimensions
        mesh = generate_ellipsoid_mesh(d["semi_axis_a"], d["semi_axis_b"], d["semi_axis_c"])
        expression = f"Hitung volume ellipsoid (a={d['semi_axis_a']}, b={d['semi_axis_b']}, c={d['semi_axis_c']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "tetrahedron":
        res = generate_tetrahedron(rng, config)
        d = res.dimensions
        mesh = generate_tetrahedron_mesh(d["side"])
        expression = f"Hitung volume tetrahedron (sisi={d['side']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "hollow_sphere":
        res = generate_hollow_sphere(rng, config)
        d = res.dimensions
        mesh = generate_sphere_mesh(d["outer_radius"])
        expression = f"Hitung volume bola berongga (R={d['outer_radius']}, r={d['inner_radius']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "octahedron":
        res = generate_octahedron(rng, config)
        d = res.dimensions
        mesh = generate_octahedron_mesh(d["side"])
        expression = f"Hitung volume oktahedron (sisi={d['side']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "dodecahedron":
        res = generate_dodecahedron(rng, config)
        d = res.dimensions
        mesh = generate_dodecahedron_mesh(d["side"])
        expression = f"Hitung volume dodekahedron (sisi={d['side']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "right_triangular_prism":
        res = generate_right_triangular_prism(rng, config)
        d = res.dimensions
        mesh = _extrude_mesh(generate_right_triangle_2d_mesh(d["base_leg"], d["height_leg"])["vertices"], d["prism_height"])
        expression = f"Hitung volume prisma segitiga siku-siku (a={d['base_leg']}, b={d['height_leg']}, t={d['prism_height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "isosceles_triangular_prism":
        res = generate_isosceles_triangular_prism(rng, config)
        d = res.dimensions
        mesh = _extrude_mesh(generate_isosceles_triangle_mesh(d["base"], d["height"])["vertices"], d["prism_height"])
        expression = f"Hitung volume prisma segitiga sama kaki (a={d['base']}, kaki={d['leg']}, t={d['prism_height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "parallelogram_prism":
        res = generate_parallelogram_prism(rng, config)
        d = res.dimensions
        mesh = _extrude_mesh(generate_parallelogram_mesh(d["base"], d["side"], d["height"])["vertices"], d["prism_height"])
        expression = f"Hitung volume prisma jajargenjang (a={d['base']}, t={d['height']}, t_prisma={d['prism_height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "trapezoidal_prism":
        res = generate_trapezoidal_prism(rng, config)
        d = res.dimensions
        mesh = _extrude_mesh(generate_trapezoid_mesh(d["base_a"], d["base_b"], d["height"], is_isosceles=False)["vertices"], d["prism_height"])
        expression = f"Hitung volume prisma trapesium (a={d['base_a']}, b={d['base_b']}, t={d['height']}, t_prisma={d['prism_height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "rhombus_prism":
        res = generate_rhombus_prism(rng, config)
        d = res.dimensions
        mesh = _extrude_mesh(generate_rhombus_mesh(d["diagonal_1"], d["diagonal_2"])["vertices"], d["prism_height"])
        expression = f"Hitung volume prisma belah ketupat (d1={d['diagonal_1']}, d2={d['diagonal_2']}, t={d['prism_height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "kite_prism":
        res = generate_kite_prism(rng, config)
        d = res.dimensions
        mesh = _extrude_mesh(generate_kite_mesh(d["diagonal_1"], d["diagonal_2"], d["diagonal_1"] / 2)["vertices"], d["prism_height"])
        expression = f"Hitung volume prisma layang-layang (d1={d['diagonal_1']}, d2={d['diagonal_2']}, t={d['prism_height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "rectangular_pyramid":
        res = generate_rectangular_pyramid(rng, config)
        d = res.dimensions
        mesh = _pyramidize_mesh(generate_rectangle_2d_mesh(d["length"], d["width"])["vertices"], d["height"])
        expression = f"Hitung volume limas persegi panjang (p={d['length']}, l={d['width']}, t={d['height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "right_triangular_pyramid":
        res = generate_right_triangular_pyramid(rng, config)
        d = res.dimensions
        mesh = _pyramidize_mesh(generate_right_triangle_2d_mesh(d["base_leg"], d["height_leg"])["vertices"], d["pyramid_height"])
        expression = f"Hitung volume limas segitiga siku-siku (a={d['base_leg']}, b={d['height_leg']}, t={d['pyramid_height']})"
        correct_answer = f"{res.volume:.2f}"

    elif target_shape == "voxel_group":
        if level == 1:
            jml_kubus = rng.randint(4, 6)
        elif level == 2:
            jml_kubus = rng.randint(6, 8)
        elif level == 3:
            jml_kubus = rng.randint(8, 10)
        elif level == 4:
            jml_kubus = rng.randint(10, 14)
        else:
            jml_kubus = rng.randint(14, 20)

        warna_warni = True

        posisi_asli, colors_asli = create_voxel_group_data(rng, jml_kubus, warna_warni)
        jml_asli = len(posisi_asli)

        min_x = min(p[0] for p in posisi_asli)
        max_x = max(p[0] for p in posisi_asli)
        min_y = min(p[1] for p in posisi_asli)
        max_y = max(p[1] for p in posisi_asli)
        min_z = min(p[2] for p in posisi_asli)
        max_z = max(p[2] for p in posisi_asli)
        mid_x = (min_x + max_x) / 2.0 + 0.5
        mid_y = (min_y + max_y) / 2.0 + 0.5
        mid_z = (min_z + max_z) / 2.0 + 0.5

        voxels_list = []
        for p in posisi_asli:
            vx, vy, vz = p
            voxels_list.append({
                "position": [vx, vy, vz],
                "centered_position": [vx - mid_x + 0.5, vy - mid_y + 0.5, vz - mid_z + 0.5],
                "color": colors_asli[p]
            })

        mesh = generate_voxel_group_mesh(posisi_asli)

        options, correct_label = generate_voxel_group_options(rng, posisi_asli, colors_asli, jml_asli, warna_warni)
        target_view = rng.choice(['Depan', 'Kanan', 'Kiri', 'Atas', 'Belakang'])

        expression = "Berapa banyak kubus satuan yang menyusun bangun ruang berikut?"
        correct_answer = str(jml_asli)

        res_dict = {
            "meta": {"seed": seed, "level": level, "shape": target_shape, "dimension": dimension.upper()},
            "data": {
                "expression": expression,
                "story": None,
                "mesh": mesh,
                "dimensions": {"cubes_count": jml_asli},
                "perimeter": None,
                "angles": None,
                "area": None,
                "volume": float(jml_asli),
                "correct_answer": correct_answer,
                "voxels": voxels_list,
                "multiview_challenge": {
                    "expression": f"Opsi manakah yang menunjukkan sudut pandang '{target_view}' dari susunan kubus berikut?",
                    "target_view": target_view,
                    "correct_label": correct_label,
                    "options": options
                }
            }
        }
        if with_story:
            res_dict["data"]["story"] = await ai_storyteller.generate_story(expression, correct_answer, "geometry", "sekolah", rng)
        return res_dict

    else: # icosahedron
        res = generate_icosahedron(rng, config)
        d = res.dimensions
        mesh = generate_icosahedron_mesh(d["side"])
        expression = f"Hitung volume ikosahedron (sisi={d['side']})"
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
            "perimeter": res.perimeter,
            "angles": res.angles,
            "area": res.area,
            "volume": res.volume,
            "correct_answer": str(correct_answer)
        }
    }
