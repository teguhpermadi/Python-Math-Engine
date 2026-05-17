import math
import random
from typing import List, Dict, Any, Optional

def get_net_supported_shapes() -> List[Dict[str, str]]:
    """
    Mengembalikan daftar bangun ruang yang didukung untuk generator jaring-jaring.
    """
    return [
        {"type": "cube", "name_id": "Kubus"},
        {"type": "block", "name_id": "Balok"},
        {"type": "triangular_prism", "name_id": "Prisma Segitiga"},
        {"type": "rectangular_pyramid", "name_id": "Limas Segiempat"},
        {"type": "cylinder", "name_id": "Tabung"},
        {"type": "cone", "name_id": "Kerucut"}
    ]

def generate_shape_net(shape_type: str, seed: int, is_valid: bool = True) -> Dict[str, Any]:
    """
    Menghasilkan pola jaring-jaring (valid atau invalid) untuk bangun ruang tertentu.
    """
    rng = random.Random(seed)
    shape_type = shape_type.lower()
    
    supported_types = [s["type"] for s in get_net_supported_shapes()]
    if shape_type not in supported_types:
        raise ValueError(f"Shape '{shape_type}' is not supported for net generation. Supported: {supported_types}")
    
    if shape_type == "cube":
        return _generate_cube_net(rng, is_valid)
    elif shape_type == "block":
        return _generate_block_net(rng, is_valid)
    elif shape_type == "triangular_prism":
        return _generate_triangular_prism_net(rng, is_valid)
    elif shape_type == "rectangular_pyramid":
        return _generate_rectangular_pyramid_net(rng, is_valid)
    elif shape_type == "cylinder":
        return _generate_cylinder_net(rng, is_valid)
    elif shape_type == "cone":
        return _generate_cone_net(rng, is_valid)
    
    # Fallback (should not happen)
    return {"error": "Unsupported shape"}

def _generate_cube_net(rng: random.Random, is_valid: bool) -> Dict[str, Any]:
    name_id = "Kubus"
    color_palette = ["#FF6B6B", "#4DABF7", "#51CF66", "#FCC419", "#FF922B", "#845EF7"]
    
    if is_valid:
        # Seluruh 11 jaring-jaring kubus yang valid secara matematis (Hexominos unik)
        # Dipilih berdasarkan seed menggunakan rng
        pattern_idx = rng.randint(1, 11)
        patterns = {
            1: {
                "name": "Pola 1-4-1 (Tipe A - Salib Standard)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Tutup", "x": 1, "y": 0},
                    {"label": "Sisi Kiri", "x": 0, "y": 1},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 3, "y": 1},
                    {"label": "Sisi Belakang", "x": 1, "y": 2}
                ]
            },
            2: {
                "name": "Pola 1-4-1 (Tipe B - Flap Bawah Geser 1)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Tutup", "x": 1, "y": 0},
                    {"label": "Sisi Kiri", "x": 0, "y": 1},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 3, "y": 1},
                    {"label": "Sisi Belakang", "x": 2, "y": 2}
                ]
            },
            3: {
                "name": "Pola 1-4-1 (Tipe C - Flap Bawah Geser 2)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Tutup", "x": 1, "y": 0},
                    {"label": "Sisi Kiri", "x": 0, "y": 1},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 3, "y": 1},
                    {"label": "Sisi Belakang", "x": 3, "y": 2}
                ]
            },
            4: {
                "name": "Pola 1-4-1 (Tipe D - Flap Bawah Geser Kiri)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Tutup", "x": 1, "y": 0},
                    {"label": "Sisi Kiri", "x": 0, "y": 1},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 3, "y": 1},
                    {"label": "Sisi Belakang", "x": 0, "y": 2}
                ]
            },
            5: {
                "name": "Pola 1-4-1 (Tipe E - Flap Atas Geser 1, Bawah 1)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Tutup", "x": 2, "y": 0},
                    {"label": "Sisi Kiri", "x": 0, "y": 1},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 3, "y": 1},
                    {"label": "Sisi Belakang", "x": 1, "y": 2}
                ]
            },
            6: {
                "name": "Pola 1-4-1 (Tipe F - Flap Atas Geser 1, Bawah 2)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Tutup", "x": 2, "y": 0},
                    {"label": "Sisi Kiri", "x": 0, "y": 1},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 3, "y": 1},
                    {"label": "Sisi Belakang", "x": 2, "y": 2}
                ]
            },
            7: {
                "name": "Pola 2-3-1 (Tipe A)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Sisi Kiri", "x": 0, "y": 0},
                    {"label": "Tutup", "x": 1, "y": 0},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 3, "y": 1},
                    {"label": "Sisi Belakang", "x": 2, "y": 2}
                ]
            },
            8: {
                "name": "Pola 2-3-1 (Tipe B)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Sisi Kiri", "x": 0, "y": 0},
                    {"label": "Tutup", "x": 1, "y": 0},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 3, "y": 1},
                    {"label": "Sisi Belakang", "x": 3, "y": 2}
                ]
            },
            9: {
                "name": "Pola 2-3-1 (Tipe C)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Sisi Kiri", "x": 1, "y": 0},
                    {"label": "Tutup", "x": 2, "y": 0},
                    {"label": "Sisi Depan", "x": 0, "y": 1},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Belakang", "x": 0, "y": 2}
                ]
            },
            10: {
                "name": "Pola 2-2-2 (Zig-zag)",
                "grid_size": {"rows": 3, "cols": 4},
                "coords": [
                    {"label": "Sisi Kiri", "x": 0, "y": 0},
                    {"label": "Tutup", "x": 1, "y": 0},
                    {"label": "Alas", "x": 1, "y": 1},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 2, "y": 2},
                    {"label": "Sisi Belakang", "x": 3, "y": 2}
                ]
            },
            11: {
                "name": "Pola 3-3 (Tangga Ganda)",
                "grid_size": {"rows": 2, "cols": 5},
                "coords": [
                    {"label": "Sisi Kiri", "x": 0, "y": 0},
                    {"label": "Tutup", "x": 1, "y": 0},
                    {"label": "Alas", "x": 2, "y": 0},
                    {"label": "Sisi Kanan", "x": 2, "y": 1},
                    {"label": "Sisi Depan", "x": 3, "y": 1},
                    {"label": "Sisi Belakang", "x": 4, "y": 1}
                ]
            }
        }
        
        selected = patterns[pattern_idx]
        faces = []
        for i, face in enumerate(selected["coords"]):
            faces.append({
                "id": i,
                "shape_type": "square",
                "label": face["label"],
                "x": float(face["x"]),
                "y": float(face["y"]),
                "width": 1.0,
                "height": 1.0,
                "color": color_palette[i]
            })
            
        return {
            "shape": "cube",
            "name_id": name_id,
            "is_valid": True,
            "pattern_name": selected["name"],
            "grid_size": selected["grid_size"],
            "error_reason": None,
            "faces": faces
        }
    else:
        # Pola acak yang salah
        pattern_idx = rng.randint(1, 3)
        if pattern_idx == 1:
            pattern_name = "Pola 6 Sejajar (Garis Lurus)"
            grid_size = {"rows": 1, "cols": 6}
            error_reason = "Semua 6 sisi persegi berjejer lurus dalam satu baris, sehingga tidak memiliki penutup samping (bagian atas dan bawah terbuka saat dilipat)."
            faces_coords = [
                {"label": "Sisi 1", "x": 0, "y": 0},
                {"label": "Sisi 2", "x": 1, "y": 0},
                {"label": "Sisi 3", "x": 2, "y": 0},
                {"label": "Sisi 4", "x": 3, "y": 0},
                {"label": "Sisi 5", "x": 4, "y": 0},
                {"label": "Sisi 6", "x": 5, "y": 0}
            ]
        elif pattern_idx == 2:
            pattern_name = "Pola Tutup Tumpang Tindih"
            grid_size = {"rows": 3, "cols": 4}
            error_reason = "Kedua penutup (alas/tutup) berada di baris atas yang sama, sehingga saat dilipat akan saling bertumpuk di bagian atas dan bagian bawah kubus tetap bolong."
            faces_coords = [
                {"label": "Tutup A", "x": 1, "y": 0},
                {"label": "Tutup B", "x": 2, "y": 0}, # Overlapping position when folded
                {"label": "Sisi Kiri", "x": 0, "y": 1},
                {"label": "Alas", "x": 1, "y": 1},
                {"label": "Sisi Kanan", "x": 2, "y": 1},
                {"label": "Sisi Depan", "x": 3, "y": 1}
            ]
        else:
            pattern_name = "Pola Kurang Sisi"
            grid_size = {"rows": 3, "cols": 4}
            error_reason = "Hanya memiliki 5 sisi persegi. Kubus memerlukan tepat 6 buah sisi persegi agar dapat tertutup dengan sempurna."
            faces_coords = [
                {"label": "Tutup", "x": 1, "y": 0},
                {"label": "Sisi Kiri", "x": 0, "y": 1},
                {"label": "Alas", "x": 1, "y": 1},
                {"label": "Sisi Kanan", "x": 2, "y": 1},
                {"label": "Sisi Depan", "x": 3, "y": 1}
                # missing Sisi Belakang
            ]
            
        faces = []
        for i, face in enumerate(faces_coords):
            faces.append({
                "id": i,
                "shape_type": "square",
                "label": face["label"],
                "x": float(face["x"]),
                "y": float(face["y"]),
                "width": 1.0,
                "height": 1.0,
                "color": "#E0E0E0" # Greyed out or light red for invalid
            })
            
        return {
            "shape": "cube",
            "name_id": name_id,
            "is_valid": False,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": error_reason,
            "faces": faces
        }

def _generate_block_net(rng: random.Random, is_valid: bool) -> Dict[str, Any]:
    name_id = "Balok"
    # Gunakan dimensi balok yang proporsional
    L = 3.0 # Panjang
    W = 2.0 # Lebar
    H = 1.2 # Tinggi
    color_palette = ["#FF6B6B", "#4DABF7", "#51CF66", "#FCC419", "#FF922B", "#845EF7"]
    
    if is_valid:
        # Ada 4 pola valid balok yang kita tawarkan berdasarkan seed
        pattern_idx = rng.randint(1, 4)
        if pattern_idx == 1:
            pattern_name = "Pola 1-4-1 Simetris Standard (L-W-H)"
            # Koordinat x dan y dihitung berdasarkan dimensi aktual agar sambungan pas
            # Midline faces: Kiri (H x W), Alas (L x W), Kanan (H x W), Tutup (L x W)
            # Flap atas/bawah: Depan (L x H) di atas Alas, Belakang (L x H) di bawah Alas
            faces_data = [
                {"label": "Sisi Kiri", "type": "rectangle", "x": 0.0, "y": H, "w": H, "h": W},
                {"label": "Alas", "type": "rectangle", "x": H, "y": H, "w": L, "h": W},
                {"label": "Sisi Kanan", "type": "rectangle", "x": H + L, "y": H, "w": H, "h": W},
                {"label": "Tutup", "type": "rectangle", "x": H + L + H, "y": H, "w": L, "h": W},
                {"label": "Sisi Depan", "type": "rectangle", "x": H, "y": 0.0, "w": L, "h": H},
                {"label": "Sisi Belakang", "type": "rectangle", "x": H, "y": H + W, "w": L, "h": H}
            ]
            grid_size = {"width": H + L + H + L, "height": H + W + H}
        elif pattern_idx == 2:
            pattern_name = "Pola 1-4-1 Flap Geser Kanan"
            # Sama seperti di atas tapi Flap bawah digeser di bawah Tutup
            faces_data = [
                {"label": "Sisi Kiri", "type": "rectangle", "x": 0.0, "y": H, "w": H, "h": W},
                {"label": "Alas", "type": "rectangle", "x": H, "y": H, "w": L, "h": W},
                {"label": "Sisi Kanan", "type": "rectangle", "x": H + L, "y": H, "w": H, "h": W},
                {"label": "Tutup", "type": "rectangle", "x": H + L + H, "y": H, "w": L, "h": W},
                {"label": "Sisi Depan", "type": "rectangle", "x": H, "y": 0.0, "w": L, "h": H},
                {"label": "Sisi Belakang", "type": "rectangle", "x": H + L + H, "y": H + W, "w": L, "h": H}
            ]
            grid_size = {"width": H + L + H + L, "height": H + W + H}
        elif pattern_idx == 3:
            pattern_name = "Pola 1-4-1 Flap Geser Kiri"
            # Flap depan digeser di atas Tutup, Flap belakang di bawah Alas
            faces_data = [
                {"label": "Sisi Kiri", "type": "rectangle", "x": 0.0, "y": H, "w": H, "h": W},
                {"label": "Alas", "type": "rectangle", "x": H, "y": H, "w": L, "h": W},
                {"label": "Sisi Kanan", "type": "rectangle", "x": H + L, "y": H, "w": H, "h": W},
                {"label": "Tutup", "type": "rectangle", "x": H + L + H, "y": H, "w": L, "h": W},
                {"label": "Sisi Depan", "type": "rectangle", "x": H + L + H, "y": 0.0, "w": L, "h": H},
                {"label": "Sisi Belakang", "type": "rectangle", "x": H, "y": H + W, "w": L, "h": H}
            ]
            grid_size = {"width": H + L + H + L, "height": H + W + H}
        else:
            pattern_name = "Pola 1-4-1 Orientasi Vertikal"
            # Baris tengah: Kiri (W x H), Alas (L x H), Kanan (W x H), Tutup (L x H)
            # Flap: Depan (L x W), Belakang (L x W)
            faces_data = [
                {"label": "Sisi Kiri", "type": "rectangle", "x": 0.0, "y": W, "w": W, "h": H},
                {"label": "Alas", "type": "rectangle", "x": W, "y": W, "w": L, "h": H},
                {"label": "Sisi Kanan", "type": "rectangle", "x": W + L, "y": W, "w": W, "h": H},
                {"label": "Tutup", "type": "rectangle", "x": W + L + W, "y": W, "w": L, "h": H},
                {"label": "Sisi Depan", "type": "rectangle", "x": W, "y": 0.0, "w": L, "h": W},
                {"label": "Sisi Belakang", "type": "rectangle", "x": W, "y": W + H, "w": L, "h": W}
            ]
            grid_size = {"width": W + L + W + L, "height": W + H + W}
            
        faces = []
        for i, f in enumerate(faces_data):
            faces.append({
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "width": round(f["w"], 2),
                "height": round(f["h"], 2),
                "color": color_palette[i]
            })
            
        return {
            "shape": "block",
            "name_id": name_id,
            "is_valid": True,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": None,
            "faces": faces
        }
    else:
        pattern_idx = rng.randint(1, 3)
        if pattern_idx == 1:
            pattern_name = "Pola Ukuran Mismatch (Samping Beda)"
            error_reason = "Ukuran lebar sisi samping (Sisi Kanan) berbeda dari tinggi balok, sehingga tidak akan menutup dengan rapat atau menyisakan celah saat dilipat."
            # Sisi Kanan diganti dengan lebar yang salah (H + 0.8)
            faces_data = [
                {"label": "Sisi Kiri", "type": "rectangle", "x": 0.0, "y": H, "w": H, "h": W},
                {"label": "Alas", "type": "rectangle", "x": H, "y": H, "w": L, "h": W},
                {"label": "Sisi Kanan", "type": "rectangle", "x": H + L, "y": H, "w": H + 0.8, "h": W},
                {"label": "Tutup", "type": "rectangle", "x": H + L + (H + 0.8), "y": H, "w": L, "h": W},
                {"label": "Sisi Depan", "type": "rectangle", "x": H, "y": 0.0, "w": L, "h": H},
                {"label": "Sisi Belakang", "type": "rectangle", "x": H, "y": H + W, "w": L, "h": H}
            ]
            grid_size = {"width": H + L + H + 0.8 + L, "height": H + W + H}
        elif pattern_idx == 2:
            pattern_name = "Pola Flap Searah"
            error_reason = "Kedua flap (Sisi Depan & Belakang) menempel di sisi atas baris tengah yang sama, sehingga akan bertumpuk saat dirangkai dan sisi bawah balok tetap terbuka."
            faces_data = [
                {"label": "Sisi Kiri", "type": "rectangle", "x": 0.0, "y": H, "w": H, "h": W},
                {"label": "Alas", "type": "rectangle", "x": H, "y": H, "w": L, "h": W},
                {"label": "Sisi Kanan", "type": "rectangle", "x": H + L, "y": H, "w": H, "h": W},
                {"label": "Tutup", "type": "rectangle", "x": H + L + H, "y": H, "w": L, "h": W},
                {"label": "Sisi Depan", "type": "rectangle", "x": H, "y": 0.0, "w": L, "h": H},
                {"label": "Sisi Belakang", "type": "rectangle", "x": H + L + H, "y": 0.0, "w": L, "h": H} # attached to top instead of bottom
            ]
            grid_size = {"width": H + L + H + L, "height": H + W}
        else:
            pattern_name = "Pola Balok Sisi Kurang"
            error_reason = "Hanya memiliki 5 sisi persegi panjang. Balok memerlukan tepat 6 buah sisi persegi panjang (3 pasang sisi sejajar) agar dapat tertutup sempurna."
            faces_data = [
                {"label": "Sisi Kiri", "type": "rectangle", "x": 0.0, "y": H, "w": H, "h": W},
                {"label": "Alas", "type": "rectangle", "x": H, "y": H, "w": L, "h": W},
                {"label": "Sisi Kanan", "type": "rectangle", "x": H + L, "y": H, "w": H, "h": W},
                {"label": "Sisi Depan", "type": "rectangle", "x": H, "y": 0.0, "w": L, "h": H},
                {"label": "Sisi Belakang", "type": "rectangle", "x": H, "y": H + W, "w": L, "h": H}
                # Tutup is missing
            ]
            grid_size = {"width": H + L + H, "height": H + W + H}
            
        faces = []
        for i, f in enumerate(faces_data):
            faces.append({
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "width": round(f["w"], 2),
                "height": round(f["h"], 2),
                "color": "#E0E0E0"
            })
            
        return {
            "shape": "block",
            "name_id": name_id,
            "is_valid": False,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": error_reason,
            "faces": faces
        }

def _generate_triangular_prism_net(rng: random.Random, is_valid: bool) -> Dict[str, Any]:
    name_id = "Prisma Segitiga"
    # Segitiga siku-siku alas dengan sisi A=3.0, B=4.0, C=5.0
    A = 3.0
    B = 4.0
    C = 5.0
    H = 4.5 # Tinggi prisma
    color_palette = ["#FF6B6B", "#4DABF7", "#51CF66", "#FCC419", "#FF922B"]
    
    if is_valid:
        # Pola standar: 3 persegi panjang berderet horizontal, 2 segitiga di atas & bawah Side 2
        # Side 1 (A x H), Side 2 (B x H), Side 3 (C x H)
        # Segitiga Alas menempel di atas Side 2, Segitiga Tutup menempel di bawah Side 2
        pattern_name = "Pola Deret Standard"
        
        # Sisi segitiga alas berdimensi B x A (alas segitiga sits on Side 2 of width B, height of triangle is A)
        # Vertices segitiga 1 (Alas) di atas Side 2 (sits from x=A to x=A+B, y=0 to y=A):
        # Relatif terhadap origin:
        # Titik 1: (A, A) - sudut siku-siku/kiri bawah segitiga
        # Titik 2: (A+B, A) - kanan bawah segitiga
        # Titik 3: (A, 0) - puncak atas segitiga
        faces_data = [
            {
                "label": "Sisi Tegak 1", "type": "rectangle", 
                "x": 0.0, "y": A, "w": A, "h": H
            },
            {
                "label": "Sisi Tegak 2 (Tengah)", "type": "rectangle", 
                "x": A, "y": A, "w": B, "h": H
            },
            {
                "label": "Sisi Tegak 3", "type": "rectangle", 
                "x": A + B, "y": A, "w": C, "h": H
            },
            {
                "label": "Alas Segitiga", "type": "triangle", 
                "x": A, "y": 0.0, 
                "vertices": [[0.0, A], [B, A], [0.0, 0.0]] # Relatif terhadap x=A, y=0.0
            },
            {
                "label": "Tutup Segitiga", "type": "triangle", 
                "x": A, "y": A + H, 
                "vertices": [[0.0, 0.0], [B, 0.0], [0.0, A]] # Relatif terhadap x=A, y=A+H
            }
        ]
        grid_size = {"width": A + B + C, "height": A + H + A}
        
        faces = []
        for i, f in enumerate(faces_data):
            face_item = {
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "color": color_palette[i]
            }
            if f["type"] == "rectangle":
                face_item["width"] = round(f["w"], 2)
                face_item["height"] = round(f["h"], 2)
            else:
                face_item["vertices"] = [[round(vx, 2), round(vy, 2)] for vx, vy in f["vertices"]]
            faces.append(face_item)
            
        return {
            "shape": "triangular_prism",
            "name_id": name_id,
            "is_valid": True,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": None,
            "faces": faces
        }
    else:
        pattern_idx = rng.randint(1, 2)
        if pattern_idx == 1:
            pattern_name = "Pola Segitiga Searah (Bertumpuk)"
            error_reason = "Kedua alas segitiga diletakkan di sisi atas deretan persegi panjang, sehingga saat dilipat akan saling bertumpuk di bagian atas dan bagian bawah prisma tetap terbuka."
            faces_data = [
                {"label": "Sisi Tegak 1", "type": "rectangle", "x": 0.0, "y": A, "w": A, "h": H},
                {"label": "Sisi Tegak 2", "type": "rectangle", "x": A, "y": A, "w": B, "h": H},
                {"label": "Sisi Tegak 3", "type": "rectangle", "x": A + B, "y": A, "w": C, "h": H},
                {"label": "Alas Segitiga", "type": "triangle", "x": A, "y": 0.0, "vertices": [[0.0, A], [B, A], [0.0, 0.0]]},
                {"label": "Tutup Segitiga", "type": "triangle", "x": A + B, "y": 0.0, "vertices": [[0.0, A], [C, A], [C, 0.0]]} # attached to top Side 3 instead of bottom
            ]
            grid_size = {"width": A + B + C, "height": A + H}
        else:
            pattern_name = "Pola Kurang Sisi Tegak"
            error_reason = "Hanya memiliki 2 sisi tegak persegi panjang. Prisma segitiga memerlukan tepat 3 sisi tegak dan 2 sisi alas segitiga agar dapat membentuk bangun tertutup."
            faces_data = [
                {"label": "Sisi Tegak 1", "type": "rectangle", "x": 0.0, "y": A, "w": A, "h": H},
                {"label": "Sisi Tegak 2", "type": "rectangle", "x": A, "y": A, "w": B, "h": H},
                # Side 3 missing
                {"label": "Alas Segitiga", "type": "triangle", "x": A, "y": 0.0, "vertices": [[0.0, A], [B, A], [0.0, 0.0]]},
                {"label": "Tutup Segitiga", "type": "triangle", "x": A, "y": A + H, "vertices": [[0.0, 0.0], [B, 0.0], [0.0, A]]}
            ]
            grid_size = {"width": A + B, "height": A + H + A}
            
        faces = []
        for i, f in enumerate(faces_data):
            face_item = {
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "color": "#E0E0E0"
            }
            if f["type"] == "rectangle":
                face_item["width"] = round(f["w"], 2)
                face_item["height"] = round(f["h"], 2)
            else:
                face_item["vertices"] = [[round(vx, 2), round(vy, 2)] for vx, vy in f["vertices"]]
            faces.append(face_item)
            
        return {
            "shape": "triangular_prism",
            "name_id": name_id,
            "is_valid": False,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": error_reason,
            "faces": faces
        }

def _generate_rectangular_pyramid_net(rng: random.Random, is_valid: bool) -> Dict[str, Any]:
    name_id = "Limas Segiempat"
    # Dimensi alas segiempat L=4.0, W=3.0.
    # Tinggi segitiga untuk alas L: H1 = 3.5.
    # Tinggi segitiga untuk alas W: H2 = 3.0.
    L = 4.0
    W = 3.0
    H1 = 3.5
    H2 = 3.0
    color_palette = ["#FF6B6B", "#4DABF7", "#51CF66", "#FCC419", "#FF922B"]
    
    if is_valid:
        # Pola Bintang (Star)
        # Alas (L x W) di tengah, dikelilingi 4 segitiga
        # Posisi Alas: x = H2, y = H1
        pattern_name = "Pola Bintang (Star Pattern)"
        faces_data = [
            {
                "label": "Alas Segiempat", "type": "rectangle", 
                "x": H2, "y": H1, "w": L, "h": W
            },
            {
                "label": "Sisi Tegak Atas", "type": "triangle", 
                "x": H2, "y": 0.0, 
                "vertices": [[0.0, H1], [L, H1], [L / 2.0, 0.0]] # Menempel di atas alas
            },
            {
                "label": "Sisi Tegak Bawah", "type": "triangle", 
                "x": H2, "y": H1 + W, 
                "vertices": [[0.0, 0.0], [L, 0.0], [L / 2.0, H1]] # Menempel di bawah alas
            },
            {
                "label": "Sisi Tegak Kiri", "type": "triangle", 
                "x": 0.0, "y": H1, 
                "vertices": [[H2, 0.0], [H2, W], [0.0, W / 2.0]] # Menempel di kiri alas
            },
            {
                "label": "Sisi Tegak Kanan", "type": "triangle", 
                "x": H2 + L, "y": H1, 
                "vertices": [[0.0, 0.0], [0.0, W], [H2, W / 2.0]] # Menempel di kanan alas
            }
        ]
        grid_size = {"width": H2 + L + H2, "height": H1 + W + H1}
        
        faces = []
        for i, f in enumerate(faces_data):
            face_item = {
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "color": color_palette[i]
            }
            if f["type"] == "rectangle":
                face_item["width"] = round(f["w"], 2)
                face_item["height"] = round(f["h"], 2)
            else:
                face_item["vertices"] = [[round(vx, 2), round(vy, 2)] for vx, vy in f["vertices"]]
            faces.append(face_item)
            
        return {
            "shape": "rectangular_pyramid",
            "name_id": name_id,
            "is_valid": True,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": None,
            "faces": faces
        }
    else:
        pattern_idx = rng.randint(1, 2)
        if pattern_idx == 1:
            pattern_name = "Pola Sisi Tegak Bertumpuk"
            error_reason = "Dua buah segitiga tegak dipasang di sisi atas alas yang sama, sehingga saat dilipat akan bertumpuk dan sisi bawah limas tetap terbuka tanpa penutup."
            faces_data = [
                {"label": "Alas Segiempat", "type": "rectangle", "x": H2, "y": H1, "w": L, "h": W},
                {"label": "Sisi Tegak Atas A", "type": "triangle", "x": H2, "y": 0.0, "vertices": [[0.0, H1], [L / 2.0, H1], [L / 4.0, 0.0]]}, # split top edge A
                {"label": "Sisi Tegak Atas B", "type": "triangle", "x": H2 + L / 2.0, "y": 0.0, "vertices": [[0.0, H1], [L / 2.0, H1], [L / 4.0, 0.0]]}, # split top edge B (overlap!)
                {"label": "Sisi Tegak Kiri", "type": "triangle", "x": 0.0, "y": H1, "vertices": [[H2, 0.0], [H2, W], [0.0, W / 2.0]]},
                {"label": "Sisi Tegak Kanan", "type": "triangle", "x": H2 + L, "y": H1, "vertices": [[0.0, 0.0], [0.0, W], [H2, W / 2.0]]}
                # Sisi Tegak Bawah missing!
            ]
            grid_size = {"width": H2 + L + H2, "height": H1 + W}
        else:
            pattern_name = "Pola Kurang Sisi Tegak"
            error_reason = "Hanya memiliki 3 segitiga tegak. Limas segiempat memerlukan tepat 4 buah segitiga tegak agar dapat menutupi keempat arah sisi alasnya."
            faces_data = [
                {"label": "Alas Segiempat", "type": "rectangle", "x": H2, "y": H1, "w": L, "h": W},
                {"label": "Sisi Tegak Atas", "type": "triangle", "x": H2, "y": 0.0, "vertices": [[0.0, H1], [L, H1], [L / 2.0, 0.0]]},
                {"label": "Sisi Tegak Kiri", "type": "triangle", "x": 0.0, "y": H1, "vertices": [[H2, 0.0], [H2, W], [0.0, W / 2.0]]},
                {"label": "Sisi Tegak Kanan", "type": "triangle", "x": H2 + L, "y": H1, "vertices": [[0.0, 0.0], [0.0, W], [H2, W / 2.0]]}
                # bottom triangle missing
            ]
            grid_size = {"width": H2 + L + H2, "height": H1 + W}
            
        faces = []
        for i, f in enumerate(faces_data):
            face_item = {
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "color": "#E0E0E0"
            }
            if f["type"] == "rectangle":
                face_item["width"] = round(f["w"], 2)
                face_item["height"] = round(f["h"], 2)
            else:
                face_item["vertices"] = [[round(vx, 2), round(vy, 2)] for vx, vy in f["vertices"]]
            faces.append(face_item)
            
        return {
            "shape": "rectangular_pyramid",
            "name_id": name_id,
            "is_valid": False,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": error_reason,
            "faces": faces
        }

def _generate_cylinder_net(rng: random.Random, is_valid: bool) -> Dict[str, Any]:
    name_id = "Tabung"
    R = 1.5 # Jari-jari lingkaran
    H = 4.0 # Tinggi tabung
    W = round(2.0 * math.pi * R, 2) # Lebar selimut tabung (keliling lingkaran ≈ 9.42)
    color_palette = ["#FF6B6B", "#4DABF7", "#51CF66"]
    
    if is_valid:
        pattern_name = "Pola Standard Tabung"
        # Selimut di tengah, lingkaran alas di atas, lingkaran tutup di bawah
        faces_data = [
            {
                "label": "Selimut Tabung", "type": "rectangle", 
                "x": 0.0, "y": 2 * R, "w": W, "h": H
            },
            {
                "label": "Alas Lingkaran", "type": "circle", 
                "x": W / 2.0, "y": R, "r": R
            },
            {
                "label": "Tutup Lingkaran", "type": "circle", 
                "x": W / 2.0, "y": 2 * R + H + R, "r": R
            }
        ]
        grid_size = {"width": W, "height": 2 * R + H + 2 * R}
        
        faces = []
        for i, f in enumerate(faces_data):
            face_item = {
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "color": color_palette[i]
            }
            if f["type"] == "rectangle":
                face_item["width"] = round(f["w"], 2)
                face_item["height"] = round(f["h"], 2)
            else:
                face_item["radius"] = round(f["r"], 2)
            faces.append(face_item)
            
        return {
            "shape": "cylinder",
            "name_id": name_id,
            "is_valid": True,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": None,
            "faces": faces
        }
    else:
        pattern_idx = rng.randint(1, 2)
        if pattern_idx == 1:
            pattern_name = "Pola Alas Lingkaran Searah"
            error_reason = "Kedua alas lingkaran diletakkan di sisi atas selimut yang sama, sehingga saat selimut digulung, kedua lingkaran bertumpuk di bagian atas dan bagian bawah tabung tetap berlubang."
            faces_data = [
                {"label": "Selimut Tabung", "type": "rectangle", "x": 0.0, "y": 2 * R, "w": W, "h": H},
                {"label": "Alas Lingkaran A", "type": "circle", "x": W / 4.0, "y": R, "r": R},
                {"label": "Alas Lingkaran B", "type": "circle", "x": 3.0 * W / 4.0, "y": R, "r": R}
            ]
            grid_size = {"width": W, "height": 2 * R + H}
        else:
            pattern_name = "Pola Ukuran Lingkaran Salah (Kecil)"
            error_reason = "Keliling/ukuran lingkaran alas terlalu kecil dibandingkan dengan panjang selimut tabung, sehingga tidak dapat menutup tabung dengan pas (selimut longgar/berlebih)."
            wrong_R = R - 0.6
            faces_data = [
                {"label": "Selimut Tabung", "type": "rectangle", "x": 0.0, "y": 2 * R, "w": W, "h": H},
                {"label": "Alas Lingkaran", "type": "circle", "x": W / 2.0, "y": wrong_R, "r": wrong_R},
                {"label": "Tutup Lingkaran", "type": "circle", "x": W / 2.0, "y": 2 * R + H + wrong_R, "r": wrong_R}
            ]
            grid_size = {"width": W, "height": 2 * R + H + 2 * wrong_R}
            
        faces = []
        for i, f in enumerate(faces_data):
            face_item = {
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "color": "#E0E0E0"
            }
            if f["type"] == "rectangle":
                face_item["width"] = round(f["w"], 2)
                face_item["height"] = round(f["h"], 2)
            else:
                face_item["radius"] = round(f["r"], 2)
            faces.append(face_item)
            
        return {
            "shape": "cylinder",
            "name_id": name_id,
            "is_valid": False,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": error_reason,
            "faces": faces
        }

def _generate_cone_net(rng: random.Random, is_valid: bool) -> Dict[str, Any]:
    name_id = "Kerucut"
    R = 1.5 # Jari-jari alas kerucut
    S = 4.5 # Garis pelukis (slant height / jari-jari juring selimut)
    theta = 120.0 # Sudut pusat juring selimut (360 * R/S = 360 * 1.5/4.5 = 120)
    color_palette = ["#FF6B6B", "#4DABF7"]
    
    if is_valid:
        pattern_name = "Pola Standard Kerucut"
        # Selimut berbentuk juring lingkaran di atas, lingkaran alas menempel di lengkungan busur bawah
        # Juring diletakkan dengan pusat juring di (S, S), menghadap ke bawah
        # Titik singgung busur di x = S, y = 2*S
        # Pusat lingkaran alas di x = S, y = 2*S + R
        faces_data = [
            {
                "label": "Selimut Juring", "type": "sector", 
                "x": S, "y": S, "radius": S, "angle": theta, "start_angle": 90.0 - theta / 2.0
            },
            {
                "label": "Alas Lingkaran", "type": "circle", 
                "x": S, "y": S + S + R, "r": R
            }
        ]
        grid_size = {"width": 2 * S, "height": S + S + 2 * R}
        
        faces = []
        for i, f in enumerate(faces_data):
            face_item = {
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "color": color_palette[i]
            }
            if f["type"] == "sector":
                face_item["radius"] = round(f["radius"], 2)
                face_item["angle"] = round(f["angle"], 2)
                face_item["start_angle"] = round(f["start_angle"], 2)
            else:
                face_item["radius"] = round(f["r"], 2)
            faces.append(face_item)
            
        return {
            "shape": "cone",
            "name_id": name_id,
            "is_valid": True,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": None,
            "faces": faces
        }
    else:
        pattern_idx = rng.randint(1, 2)
        if pattern_idx == 1:
            pattern_name = "Pola Alas Lingkaran Terpisah (Posisi Salah)"
            error_reason = "Lingkaran alas diletakkan di samping/tidak menempel pada bagian busur lengkung selimut kerucut, sehingga saat dilipat tidak dapat membentuk kerucut utuh."
            # Tempatkan lingkaran terpisah jauh ke samping
            faces_data = [
                {"label": "Selimut Juring", "type": "sector", "x": S, "y": S, "radius": S, "angle": theta, "start_angle": 90.0 - theta / 2.0},
                {"label": "Alas Lingkaran", "type": "circle", "x": S + S + R, "y": S, "r": R}
            ]
            grid_size = {"width": 2 * S + 2 * R, "height": 2 * S}
        else:
            pattern_name = "Pola Sudut Selimut Salah (Terlalu Sempit)"
            error_reason = "Sudut juring selimut kerucut terlalu sempit sehingga panjang busurnya tidak cukup untuk membungkus keliling lingkaran alas."
            wrong_theta = 60.0 # Harusnya 120
            faces_data = [
                {"label": "Selimut Juring", "type": "sector", "x": S, "y": S, "radius": S, "angle": wrong_theta, "start_angle": 90.0 - wrong_theta / 2.0},
                {"label": "Alas Lingkaran", "type": "circle", "x": S, "y": S + S + R, "r": R}
            ]
            grid_size = {"width": 2 * S, "height": S + S + 2 * R}
            
        faces = []
        for i, f in enumerate(faces_data):
            face_item = {
                "id": i,
                "shape_type": f["type"],
                "label": f["label"],
                "x": round(f["x"], 2),
                "y": round(f["y"], 2),
                "color": "#E0E0E0"
            }
            if f["type"] == "sector":
                face_item["radius"] = round(f["radius"], 2)
                face_item["angle"] = round(f["angle"], 2)
                face_item["start_angle"] = round(f["start_angle"], 2)
            else:
                face_item["radius"] = round(f["r"], 2)
            faces.append(face_item)
            
        return {
            "shape": "cone",
            "name_id": name_id,
            "is_valid": False,
            "pattern_name": pattern_name,
            "grid_size": grid_size,
            "error_reason": error_reason,
            "faces": faces
        }
