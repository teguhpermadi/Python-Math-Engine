import httpx
import json

BASE_URL = "http://localhost:8000/api/v1/geometry"

def _test_shape(shape: str, level: int = 3, expect_vertices: int | None = None):
    url = f"{BASE_URL}/generate"
    payload = {
        "seed": 777,
        "level": level,
        "shape": shape,
        "with_story": False,
        "dimension": "3D"
    }
    print(f"\nTesting {shape}...")
    resp = httpx.post(url, json=payload)
    assert resp.status_code == 200, f"Status: {resp.status_code} - {resp.text}"
    data = resp.json()
    print(f"  Shape: {data['meta']['shape']}")
    print(f"  Expression: {data['data']['expression']}")
    print(f"  Answer: {data['data']['correct_answer']}")
    print(f"  Vertices: {len(data['data']['mesh']['vertices'])}")
    print(f"  Faces: {len(data['data']['mesh']['faces'])}")
    assert data['meta']['shape'] == shape
    assert len(data['data']['mesh']['vertices']) > 0
    assert len(data['data']['mesh']['faces']) > 0
    if expect_vertices:
        assert len(data['data']['mesh']['vertices']) == expect_vertices
    print(f"  SUCCESS: {shape} is correct.")
    return data


def test_cube():
    _test_shape("cube", level=3, expect_vertices=8)

def test_block():
    _test_shape("block", level=3)

def test_pyramid():
    _test_shape("pyramid", level=3)

def test_prism():
    _test_shape("prism", level=3)

def test_sphere():
    _test_shape("sphere", level=5)

def test_cylinder():
    _test_shape("cylinder", level=3)

def test_cone():
    _test_shape("cone", level=3)

def test_hemisphere():
    _test_shape("hemisphere", level=4)

def test_frustum():
    _test_shape("frustum", level=4)

def test_torus():
    _test_shape("torus", level=5)

def test_ellipsoid():
    _test_shape("ellipsoid", level=5)

def test_tetrahedron():
    _test_shape("tetrahedron", level=3, expect_vertices=4)

def test_hollow_sphere():
    _test_shape("hollow_sphere", level=5)

def test_octahedron():
    _test_shape("octahedron", level=4, expect_vertices=6)

def test_dodecahedron():
    _test_shape("dodecahedron", level=5, expect_vertices=20)

def test_icosahedron():
    _test_shape("icosahedron", level=5, expect_vertices=12)


def test_shapes_endpoint():
    print("\nTesting /shapes endpoint...")
    resp = httpx.get(f"{BASE_URL}/shapes")
    assert resp.status_code == 200
    data = resp.json()
    assert "2D" in data
    assert "3D" in data
    print(f"  2D shapes: {len(data['2D'])}")
    print(f"  3D shapes: {len(data['3D'])}")
    assert "cube" in data["3D"]
    assert "cylinder" in data["3D"]
    assert "cone" in data["3D"]
    assert "dodecahedron" in data["3D"]
    print("  SUCCESS: Shapes endpoint is correct.")


def test_all_3d_shapes():
    """Test that ALL 3D shapes can be generated successfully."""
    shapes = [
        "cube", "block", "pyramid", "prism", "sphere",
        "cylinder", "cone", "hemisphere", "frustum",
        "torus", "ellipsoid", "tetrahedron", "hollow_sphere",
        "octahedron", "dodecahedron", "icosahedron",
    ]
    levels = {
        "cube": 3, "block": 3, "pyramid": 3, "prism": 3,
        "cylinder": 3, "cone": 3, "tetrahedron": 3,
        "hemisphere": 4, "frustum": 4, "octahedron": 4,
        "sphere": 5, "torus": 5, "ellipsoid": 5,
        "dodecahedron": 5, "icosahedron": 5, "hollow_sphere": 5,
    }
    for shape in shapes:
        data = _test_shape(shape, levels[shape])
        assert data['data']['volume'] is not None
        assert data['data']['correct_answer'] is not None


if __name__ == "__main__":
    test_shapes_endpoint()
    print("\n" + "=" * 50)
    test_all_3d_shapes()
    print("\n" + "=" * 50)
    print("\nAll tests PASSED!")
