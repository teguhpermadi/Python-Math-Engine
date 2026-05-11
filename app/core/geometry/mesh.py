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


def _extrude_mesh(vertices_2d: list, height: float) -> dict:
    bottom = [list(v) for v in vertices_2d]
    top = [[v[0], v[1], height] for v in vertices_2d]
    vertices = bottom + top
    n = len(bottom)
    faces = []
    for i in range(1, n - 1):
        faces.append([0, i, i + 1])
    for i in range(1, n - 1):
        faces.append([n, n + i + 1, n + i])
    for i in range(n):
        nxt = (i + 1) % n
        a, b, c, d = i, nxt, n + i, n + nxt
        faces.append([a, b, d])
        faces.append([a, d, c])
    return {"vertices": vertices, "faces": faces}


def _pyramidize_mesh(vertices_2d: list, height: float) -> dict:
    cx = sum(v[0] for v in vertices_2d) / len(vertices_2d)
    cy = sum(v[1] for v in vertices_2d) / len(vertices_2d)
    vertices = [list(v) for v in vertices_2d]
    vertices.append([cx, cy, height])
    n = len(vertices_2d)
    apex = n
    faces = []
    for i in range(n):
        nxt = (i + 1) % n
        faces.append([i, nxt, apex])
        if i > 0 and i < n - 1:
            faces.append([0, i, nxt])
    return {"vertices": vertices, "faces": faces}


# ── 3D MESH GENERATORS ─────────────────────────────────────────────────────

def generate_sphere_mesh(radius: float, segments: int = 16) -> dict:
    vertices = []
    faces = []
    for i in range(segments + 1):
        theta = math.pi * i / segments
        for j in range(segments):
            phi = 2 * math.pi * j / segments
            x = radius * math.sin(theta) * math.cos(phi)
            y = radius * math.cos(theta)
            z = radius * math.sin(theta) * math.sin(phi)
            vertices.append([round(x, 4), round(y, 4), round(z, 4)])
    for i in range(segments):
        for j in range(segments):
            a = i * segments + j
            b = a + segments
            faces.append([a, b, b + 1])
            faces.append([a, b + 1, a + 1])
    return {"vertices": vertices, "faces": faces}


def generate_cylinder_mesh(radius: float, height: float, segments: int = 32) -> dict:
    vertices = []
    faces = []
    vertices.append([0, -height / 2, 0])
    vertices.append([0, height / 2, 0])
    bot_start = 2
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        vertices.append([round(x, 4), -height / 2, round(z, 4)])
    top_start = 2 + segments
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        vertices.append([round(x, 4), height / 2, round(z, 4)])
    for i in range(segments):
        nxt = (i + 1) % segments
        faces.append([0, bot_start + nxt, bot_start + i])
        faces.append([1, top_start + i, top_start + nxt])
        a, b = bot_start + i, bot_start + nxt
        c, d = top_start + i, top_start + nxt
        faces.append([a, b, d])
        faces.append([a, d, c])
    return {"vertices": vertices, "faces": faces}


def generate_cone_mesh(radius: float, height: float, segments: int = 32) -> dict:
    vertices = []
    faces = []
    vertices.append([0, height / 2, 0])
    vertices.append([0, -height / 2, 0])
    base_start = 2
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        vertices.append([round(x, 4), -height / 2, round(z, 4)])
    for i in range(segments):
        nxt = (i + 1) % segments
        faces.append([1, base_start + i, base_start + nxt])
        faces.append([0, base_start + nxt, base_start + i])
    return {"vertices": vertices, "faces": faces}


def generate_hemisphere_mesh(radius: float, rings: int = 8, segments: int = 16) -> dict:
    vertices = []
    faces = []
    vertices.append([0, 0, 0])
    base_start = 1
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        vertices.append([round(x, 4), 0, round(z, 4)])
    for i in range(1, rings + 1):
        theta = math.pi * i / (2 * rings)
        y = radius * math.cos(theta)
        r = radius * math.sin(theta)
        for j in range(segments):
            phi = 2 * math.pi * j / segments
            x = r * math.cos(phi)
            z = r * math.sin(phi)
            vertices.append([round(x, 4), round(y, 4), round(z, 4)])
    for i in range(segments):
        nxt = (i + 1) % segments
        faces.append([0, base_start + nxt, base_start + i])
    for ring in range(rings):
        row_start = base_start + segments + ring * segments
        prev_row = base_start + segments + (ring - 1) * segments if ring > 0 else base_start
        for j in range(segments):
            nxt = (j + 1) % segments
            a = prev_row + j
            b = prev_row + nxt
            c = row_start + j
            d = row_start + nxt
            faces.append([a, b, d])
            faces.append([a, d, c])
    return {"vertices": vertices, "faces": faces}


def generate_frustum_mesh(bottom_radius: float, top_radius: float, height: float, segments: int = 32) -> dict:
    vertices = []
    faces = []
    vertices.append([0, -height / 2, 0])
    vertices.append([0, height / 2, 0])
    bot_start = 2
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = bottom_radius * math.cos(angle)
        z = bottom_radius * math.sin(angle)
        vertices.append([round(x, 4), -height / 2, round(z, 4)])
    top_start = 2 + segments
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = top_radius * math.cos(angle)
        z = top_radius * math.sin(angle)
        vertices.append([round(x, 4), height / 2, round(z, 4)])
    for i in range(segments):
        nxt = (i + 1) % segments
        faces.append([0, bot_start + nxt, bot_start + i])
        faces.append([1, top_start + i, top_start + nxt])
        a, b = bot_start + i, bot_start + nxt
        c, d = top_start + i, top_start + nxt
        faces.append([a, b, d])
        faces.append([a, d, c])
    return {"vertices": vertices, "faces": faces}


def generate_torus_mesh(major_radius: float, minor_radius: float, rings: int = 16, segments: int = 16) -> dict:
    vertices = []
    faces = []
    for i in range(rings):
        u = 2 * math.pi * i / rings
        for j in range(segments):
            v = 2 * math.pi * j / segments
            x = (major_radius + minor_radius * math.cos(v)) * math.cos(u)
            y = minor_radius * math.sin(v)
            z = (major_radius + minor_radius * math.cos(v)) * math.sin(u)
            vertices.append([round(x, 4), round(y, 4), round(z, 4)])
    for i in range(rings):
        for j in range(segments):
            a = i * segments + j
            b = ((i + 1) % rings) * segments + j
            c = ((i + 1) % rings) * segments + (j + 1) % segments
            d = i * segments + (j + 1) % segments
            faces.append([a, b, c])
            faces.append([a, c, d])
    return {"vertices": vertices, "faces": faces}


def generate_ellipsoid_mesh(a: float, b: float, c: float, segments: int = 16) -> dict:
    vertices = []
    faces = []
    for i in range(segments + 1):
        theta = math.pi * i / segments
        for j in range(segments):
            phi = 2 * math.pi * j / segments
            x = a * math.sin(theta) * math.cos(phi)
            y = b * math.cos(theta)
            z = c * math.sin(theta) * math.sin(phi)
            vertices.append([round(x, 4), round(y, 4), round(z, 4)])
    for i in range(segments):
        for j in range(segments):
            a_idx = i * segments + j
            b_idx = a_idx + segments
            faces.append([a_idx, b_idx, b_idx + 1])
            faces.append([a_idx, b_idx + 1, a_idx + 1])
    return {"vertices": vertices, "faces": faces}


def _scale_vertices(vertices: list, scale: float) -> list:
    return [[round(v[0] * scale, 4), round(v[1] * scale, 4), round(v[2] * scale, 4)] for v in vertices]


def generate_tetrahedron_mesh(side: float) -> dict:
    s = side / (2 * math.sqrt(2))
    vertices = [
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
    ]
    vertices = _scale_vertices(vertices, s)
    faces = [[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]]
    return {"vertices": vertices, "faces": faces}


def generate_octahedron_mesh(side: float) -> dict:
    s = side / math.sqrt(2)
    vertices = [
        [1, 0, 0], [-1, 0, 0], [0, 1, 0],
        [0, -1, 0], [0, 0, 1], [0, 0, -1]
    ]
    vertices = _scale_vertices(vertices, s)
    faces = [
        [0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
        [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]
    ]
    return {"vertices": vertices, "faces": faces}


def generate_dodecahedron_mesh(side: float) -> dict:
    phi = (1 + math.sqrt(5)) / 2
    s = side * phi / 2
    v = [
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
        [0, 1/phi, phi], [0, -1/phi, phi], [0, 1/phi, -phi], [0, -1/phi, -phi],
        [1/phi, phi, 0], [-1/phi, phi, 0], [1/phi, -phi, 0], [-1/phi, -phi, 0],
        [phi, 0, 1/phi], [phi, 0, -1/phi], [-phi, 0, 1/phi], [-phi, 0, -1/phi],
    ]
    vertices = _scale_vertices(v, s)
    pentagons = [
        [0, 8, 4, 13, 12], [0, 12, 1, 17, 16], [0, 16, 2, 9, 8],
        [1, 10, 5, 13, 12], [1, 10, 11, 3, 17], [2, 14, 15, 6, 9],
        [2, 14, 3, 17, 16], [4, 13, 5, 19, 18], [4, 8, 9, 6, 18],
        [7, 11, 3, 14, 15], [7, 11, 10, 5, 19], [7, 15, 6, 18, 19],
    ]
    faces = []
    for p in pentagons:
        for i in range(1, len(p) - 1):
            faces.append([p[0], p[i], p[i + 1]])
    return {"vertices": vertices, "faces": faces}


def generate_icosahedron_mesh(side: float) -> dict:
    phi = (1 + math.sqrt(5)) / 2
    s = side / 2
    v = [
        [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
        [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
        [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1],
    ]
    vertices = _scale_vertices(v, s)
    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
    ]
    return {"vertices": vertices, "faces": faces}
