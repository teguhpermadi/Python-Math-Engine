import random
import math

def generate_complementary_angle(rng: random.Random):
    """Sudut Penyiku (x + y = 90)"""
    angle_a = rng.randint(10, 80)
    angle_b = 90 - angle_a
    return {
        "type": "complementary",
        "angle_a": angle_a,
        "angle_b": angle_b,
        "sum": 90
    }

def generate_supplementary_angle(rng: random.Random):
    """Sudut Pelurus (x + y = 180)"""
    angle_a = rng.randint(20, 160)
    angle_b = 180 - angle_a
    return {
        "type": "supplementary",
        "angle_a": angle_a,
        "angle_b": angle_b,
        "sum": 180
    }

def generate_parallel_line_angles(rng: random.Random):
    """Hubungan sudut pada dua garis sejajar yang dipotong transversal"""
    base_angle = rng.randint(30, 150)
    other_angle = 180 - base_angle
    
    # Hubungan: 
    # 1. Sehadap (Corresponding) -> sama
    # 2. Dalam Berseberangan (Alt Interior) -> sama
    # 3. Luar Berseberangan (Alt Exterior) -> sama
    # 4. Dalam Sepihak (Consecutive Interior) -> jumlah 180
    
    relationships = ["sehadap", "dalam_berseberangan", "luar_berseberangan", "dalam_sepihak"]
    rel = rng.choice(relationships)
    
    return {
        "type": "parallel_lines",
        "relationship": rel,
        "angle_1": base_angle,
        "angle_2": base_angle if rel != "dalam_sepihak" else other_angle,
        "is_equal": rel != "dalam_sepihak"
    }
