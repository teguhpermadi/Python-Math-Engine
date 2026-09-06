"""Test endpoint geometry via in-process TestClient (bukan HTTP ke port eksternal)."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
BASE = "/api/v1/geometry"


def _test_shape(shape: str, level: int = 3, expect_vertices: int | None = None):
    resp = client.post(
        f"{BASE}/generate",
        json={"seed": 777, "level": level, "shape": shape, "with_story": False, "dimension": "3D"},
    )
    assert resp.status_code == 200, f"{shape}: {resp.status_code} - {resp.text}"
    data = resp.json()

    assert data["meta"]["shape"] == shape
    assert len(data["data"]["mesh"]["vertices"]) > 0
    assert len(data["data"]["mesh"]["faces"]) > 0
    if expect_vertices:
        assert len(data["data"]["mesh"]["vertices"]) == expect_vertices
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
    resp = client.get(f"{BASE}/shapes")
    assert resp.status_code == 200
    data = resp.json()
    assert "2D" in data and "3D" in data
    for shape in ("cube", "cylinder", "cone", "dodecahedron"):
        assert shape in data["3D"]


def test_2d_shapes_generate_without_dimension():
    """Regression: shape 2D harus tetap bisa digenerate meski dimension salah/lewat default 3D."""
    resp = client.post(f"{BASE}/generate", json={"seed": 5, "level": 1, "shape": "square"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["meta"]["dimension"] == "2D"


def test_alias_shapes():
    """Alias klien lama (cuboid / rectangular_prism) dipetakan ke block."""
    resp = client.post(f"{BASE}/generate", json={"seed": 5, "level": 3, "shape": "cuboid"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["meta"]["shape"] == "block"

    resp2 = client.post(f"{BASE}/generate", json={"seed": 5, "level": 3, "shape": "rectangular_prism"})
    assert resp2.status_code == 200, resp2.text
    assert resp2.json()["meta"]["shape"] == "block"


def test_all_3d_shapes():
    """Test that ALL 3D shapes can be generated successfully."""
    shapes = {
        "cube": 3, "block": 3, "pyramid": 3, "prism": 3,
        "cylinder": 3, "cone": 3, "tetrahedron": 3,
        "hemisphere": 4, "frustum": 4, "octahedron": 4,
        "sphere": 5, "torus": 5, "ellipsoid": 5,
        "dodecahedron": 5, "icosahedron": 5, "hollow_sphere": 5,
    }
    for shape, level in shapes.items():
        data = _test_shape(shape, level)
        assert data["data"]["volume"] is not None, shape
        assert data["data"]["correct_answer"] is not None, shape


if __name__ == "__main__":
    test_shapes_endpoint()
    test_all_3d_shapes()
    print("All tests PASSED!")

