# --- MODULAR VOXEL GEOMETRY CORE ---

def create_voxel_group_data(rng, jml_kubus: int, warna_warni: bool):
    """
    Procedural voxel generation algorithm that grows a connected group of cubes.
    Starts at center bottom (4, 4, 0) inside an 8x8x8 grid.
    """
    grid_size = 8
    posisi_terisi = []
    occupied = set()
    colors = {}
    palette = ['#FF3366', '#33CCFF', '#FFD700', '#33FF77', '#FF8833'] if warna_warni else ['#DCDCDC']

    # Start at center bottom
    x, y, z = grid_size // 2, grid_size // 2, 0
    posisi_terisi.append((x, y, z))
    occupied.add((x, y, z))
    colors[(x, y, z)] = rng.choice(palette)

    attempts = 0
    while len(posisi_terisi) < jml_kubus and attempts < 500:
        curr = rng.choice(posisi_terisi)
        tetangga = [
            (curr[0]+1, curr[1], curr[2]), (curr[0]-1, curr[1], curr[2]),
            (curr[0], curr[1]+1, curr[2]), (curr[0], curr[1]-1, curr[2]),
            (curr[0], curr[1], curr[2]+1)
        ]
        valid = [
            t for t in tetangga 
            if 0 <= t[0] < grid_size and 0 <= t[1] < grid_size and 0 <= t[2] < grid_size 
            and t not in occupied
        ]
        if valid:
            p = rng.choice(valid)
            posisi_terisi.append(p)
            occupied.add(p)
            colors[p] = rng.choice(palette)
        attempts += 1
    return posisi_terisi, colors

def generate_voxel_group_mesh(posisi_terisi) -> dict:
    """
    Builds a single combined 3D mesh (vertices and faces) for a list of voxel coordinates.
    Centers the mesh vertices around (0, 0, 0) using bounding box centering.
    """
    min_x = min(p[0] for p in posisi_terisi)
    max_x = max(p[0] for p in posisi_terisi)
    min_y = min(p[1] for p in posisi_terisi)
    max_y = max(p[1] for p in posisi_terisi)
    min_z = min(p[2] for p in posisi_terisi)
    max_z = max(p[2] for p in posisi_terisi)

    # Perfect bounding-box centering
    mid_x = (min_x + max_x) / 2.0 + 0.5
    mid_y = (min_y + max_y) / 2.0 + 0.5
    mid_z = (min_z + max_z) / 2.0 + 0.5

    vertices = []
    faces = []
    
    # 12 triangular faces of a single cube relative to its index
    cube_faces_base = [
        [0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6],
        [0, 3, 7], [0, 7, 4], [1, 2, 6], [1, 6, 5]
    ]

    for i, p in enumerate(posisi_terisi):
        vx, vy, vz = p
        x0, x1 = vx - mid_x, vx + 1 - mid_x
        y0, y1 = vy - mid_y, vy + 1 - mid_y
        z0, z1 = vz - mid_z, vz + 1 - mid_z
        
        # 8 vertices for this cube
        vertices.extend([
            [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
            [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]
        ])
        
        # Shift indices by 8 * i
        idx_offset = 8 * i
        for f in cube_faces_base:
            faces.append([f[0] + idx_offset, f[1] + idx_offset, f[2] + idx_offset])
            
    return {"vertices": vertices, "faces": faces}

def generate_voxel_group_options(rng, posisi_asli, colors_asli, jml_kubus, warna_warni):
    """
    Generates 4 multiple choice options (A, B, C, D) for the multi-view puzzle:
    - 1 Correct shape & colors
    - 1 Same shape with colors shuffled
    - 2 Randomly grown voxel shapes of the same size
    """
    # Option Correct (Option 0)
    opt_correct = {
        "type": "correct",
        "posisi": posisi_asli,
        "colors": colors_asli
    }
    
    # Option Distractor 1: Same shape, colors shuffled (Option 1)
    if warna_warni and len(posisi_asli) > 1:
        colors_list = [colors_asli[p] for p in posisi_asli]
        shuffled_colors_list = list(colors_list)
        # Try to shuffle until they are not identical, max 10 attempts
        for _ in range(10):
            rng.shuffle(shuffled_colors_list)
            if shuffled_colors_list != colors_list:
                break
        colors_shuffled = {p: shuffled_colors_list[idx] for idx, p in enumerate(posisi_asli)}
    else:
        colors_shuffled = colors_asli
        
    opt_color_shuffled = {
        "type": "color_shuffled",
        "posisi": posisi_asli,
        "colors": colors_shuffled
    }
    
    # Option Distractor 2: Different shape (Option 2)
    posisi_diff1, colors_diff1 = create_voxel_group_data(rng, jml_kubus, warna_warni)
    opt_diff1 = {
        "type": "different_shape_1",
        "posisi": posisi_diff1,
        "colors": colors_diff1
    }
    
    # Option Distractor 3: Different shape (Option 3)
    posisi_diff2, colors_diff2 = create_voxel_group_data(rng, jml_kubus, warna_warni)
    opt_diff2 = {
        "type": "different_shape_2",
        "posisi": posisi_diff2,
        "colors": colors_diff2
    }
    
    options_raw = [opt_correct, opt_color_shuffled, opt_diff1, opt_diff2]
    rng.shuffle(options_raw)
    
    labels = ["A", "B", "C", "D"]
    options = []
    correct_label = None
    
    for idx, opt in enumerate(options_raw):
        label = labels[idx]
        if opt["type"] == "correct":
            correct_label = label
            
        mesh_opt = generate_voxel_group_mesh(opt["posisi"])
        
        min_x = min(p[0] for p in opt["posisi"])
        max_x = max(p[0] for p in opt["posisi"])
        min_y = min(p[1] for p in opt["posisi"])
        max_y = max(p[1] for p in opt["posisi"])
        min_z = min(p[2] for p in opt["posisi"])
        max_z = max(p[2] for p in opt["posisi"])
        mid_x = (min_x + max_x) / 2.0 + 0.5
        mid_y = (min_y + max_y) / 2.0 + 0.5
        mid_z = (min_z + max_z) / 2.0 + 0.5
        
        voxels_opt = []
        for p in opt["posisi"]:
            vx, vy, vz = p
            voxels_opt.append({
                "position": [vx, vy, vz],
                "centered_position": [vx - mid_x + 0.5, vy - mid_y + 0.5, vz - mid_z + 0.5],
                "color": opt["colors"][p]
            })
            
        options.append({
            "label": label,
            "type": opt["type"],
            "mesh": mesh_opt,
            "voxels": voxels_opt
        })
        
    return options, correct_label
