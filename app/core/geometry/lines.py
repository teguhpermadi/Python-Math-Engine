import math

def get_line_coords(x1, y1, angle_deg, length):
    """Mendapatkan koordinat akhir garis berdasarkan sudut dan panjang."""
    angle_rad = math.radians(angle_deg)
    x2 = x1 + length * math.cos(angle_rad)
    y2 = y1 + length * math.sin(angle_rad)
    return [round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]

def generate_complementary_drawing(angle_a_deg):
    """Visual data for complementary angles (L-shape)"""
    # Base vertex at (0,0)
    origin = [0, 0]
    # Horizontal line (OA)
    p_a = [50, 0]
    # Vertical line (OB)
    p_b = [0, 50]
    # Middle line (OC) based on angle_a
    _, p_c = get_line_coords(0, 0, angle_a_deg, 50)
    
    return {
        "points": {"O": origin, "A": p_a, "B": p_b, "C": p_c},
        "lines": [["O", "A"], ["O", "B"], ["O", "C"]],
        "angles": [
            {"label": "x", "points": ["A", "O", "C"], "value": angle_a_deg},
            {"label": "y", "points": ["C", "O", "B"], "value": 90 - angle_a_deg}
        ]
    }

def generate_supplementary_drawing(angle_a_deg):
    """Visual data for supplementary angles (Straight line)"""
    origin = [0, 0]
    p_a = [50, 0] # Right
    p_b = [-50, 0] # Left
    _, p_c = get_line_coords(0, 0, angle_a_deg, 50)
    
    return {
        "points": {"O": origin, "A": p_a, "B": p_b, "C": p_c},
        "lines": [["O", "A"], ["O", "B"], ["O", "C"]],
        "angles": [
            {"label": "x", "points": ["A", "O", "C"], "value": angle_a_deg},
            {"label": "y", "points": ["C", "O", "B"], "value": 180 - angle_a_deg}
        ]
    }
