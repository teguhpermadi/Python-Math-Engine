import math

def generate_cube_mesh(side: float) -> dict:
    s = side / 2
    vertices = [
        [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],
        [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]
    ]
    faces = [
        [0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6],
        [0, 3, 7], [0, 7, 4], [1, 2, 6], [1, 6, 5]
    ]
    return {"vertices": vertices, "faces": faces}

def generate_block_mesh(l: float, w: float, h: float) -> dict:
    x, y, z = l/2, w/2, h/2
    vertices = [
        [-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z],
        [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]
    ]
    faces = [
        [0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6],
        [0, 3, 7], [0, 7, 4], [1, 2, 6], [1, 6, 5]
    ]
    return {"vertices": vertices, "faces": faces}

def _get_polygon_points(n: int, radius: float, y: float) -> list:
    """Menghasilkan titik-titik poligon pada bidang XZ."""
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        points.append([
            round(radius * math.cos(angle), 3),
            round(y, 3),
            round(radius * math.sin(angle), 3)
        ])
    return points

def generate_pyramid_mesh(n: int, side: float, height: float) -> dict:
    # Radius lingkaran luar (circumradius) poligon
    radius = side / (2 * math.sin(math.pi / n))
    
    # 1. Vertices (Alas + Titik Puncak)
    vertices = _get_polygon_points(n, radius, 0)
    vertices.append([0, height, 0]) # Titik puncak di index 'n'
    
    # 2. Faces
    faces = []
    apex_idx = n
    for i in range(n):
        next_idx = (i + 1) % n
        # Sisi tegak (segitiga)
        faces.append([i, next_idx, apex_idx])
        # Alas (segitiga fans dari titik 0)
        if i > 0 and i < n - 1:
            faces.append([0, i, next_idx])
            
    return {"vertices": vertices, "faces": faces}

def generate_prism_mesh(n: int, side: float, height: float) -> dict:
    radius = side / (2 * math.sin(math.pi / n))
    
    # 1. Vertices (Alas bawah + Alas atas)
    vertices = _get_polygon_points(n, radius, 0)
    vertices += _get_polygon_points(n, radius, height)
    
    # 2. Faces
    faces = []
    for i in range(n):
        next_idx = (i + 1) % n
        top_i = i + n
        top_next = next_idx + n
        
        # Sisi tegak (persegi/2 segitiga)
        faces.append([i, next_idx, top_next])
        faces.append([i, top_next, top_i])
        
        # Alas bawah & atas
        if i > 0 and i < n - 1:
            faces.append([0, next_idx, i]) # Alas bawah
            faces.append([n, top_i, top_next]) # Alas atas
            
    return {"vertices": vertices, "faces": faces}

# ── 2D MESH ─────────────────────────────────────────────────────────────────

def generate_right_triangle_2d_mesh(base: float, height: float) -> dict:
    vertices = [[0, 0, 0], [base, 0, 0], [0, height, 0]]
    faces = [[0, 1, 2]]
    return {"vertices": vertices, "faces": faces}


def generate_equilateral_triangle_mesh(side: float) -> dict:
    h = (math.sqrt(3) / 2) * side
    vertices = [[0, 0, 0], [side, 0, 0], [side / 2, h, 0]]
    faces = [[0, 1, 2]]
    return {"vertices": vertices, "faces": faces}


def generate_isosceles_triangle_mesh(base: float, height: float) -> dict:
    vertices = [[0, 0, 0], [base, 0, 0], [base / 2, height, 0]]
    faces = [[0, 1, 2]]
    return {"vertices": vertices, "faces": faces}


def generate_scalene_triangle_mesh(a: float, b: float, c: float) -> dict:
    cx = (a**2 + c**2 - b**2) / (2 * c)
    cy = math.sqrt(max(0, a**2 - cx**2))
    vertices = [[0, 0, 0], [c, 0, 0], [cx, cy, 0]]
    faces = [[0, 1, 2]]
    return {"vertices": vertices, "faces": faces}


def generate_parallelogram_mesh(base: float, side: float, height: float) -> dict:
    offset = math.sqrt(max(0, side**2 - height**2))
    vertices = [[0, 0, 0], [base, 0, 0], [base + offset, height, 0], [offset, height, 0]]
    faces = [[0, 1, 2], [0, 2, 3]]
    return {"vertices": vertices, "faces": faces}


def generate_trapezoid_mesh(a: float, b: float, height: float, is_isosceles: bool = True) -> dict:
    offset = (b - a) / 2
    vertices = [[0, 0, 0], [b, 0, 0], [offset + a, height, 0], [offset, height, 0]]
    faces = [[0, 1, 2], [0, 2, 3]]
    return {"vertices": vertices, "faces": faces}


def generate_kite_mesh(d1: float, d2: float, p: float) -> dict:
    t = d2 / 2
    vertices = [[0, 0, 0], [d1, 0, 0], [p, t, 0], [p, -t, 0]]
    faces = [[0, 2, 1], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    return {"vertices": vertices, "faces": faces}


def generate_rhombus_mesh(d1: float, d2: float) -> dict:
    vertices = [[-d1 / 2, 0, 0], [0, d2 / 2, 0], [d1 / 2, 0, 0], [0, -d2 / 2, 0]]
    faces = [[0, 1, 2], [0, 2, 3]]
    return {"vertices": vertices, "faces": faces}


def generate_ellipse_mesh(a: float, b: float, segments: int = 32) -> dict:
    vertices = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        vertices.append([a * math.cos(angle), b * math.sin(angle), 0])
    faces = []
    for i in range(1, segments - 1):
        faces.append([0, i, i + 1])
    return {"vertices": vertices, "faces": faces}


def generate_rectangle_2d_mesh(l: float, w: float) -> dict:
    x, y = l/2, w/2
    vertices = [[-x, -y, 0], [x, -y, 0], [x, y, 0], [-x, y, 0]]
    faces = [[0, 1, 2], [0, 2, 3]]
    return {"vertices": vertices, "faces": faces}

def generate_polygon_2d_mesh(n: int, radius: float) -> dict:
    vertices = _get_polygon_points(n, radius, 0)
    faces = []
    for i in range(1, n - 1):
        faces.append([0, i, i + 1])
    return {"vertices": vertices, "faces": faces}
