import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_angles_complementary():
    """Complementary angles + drawing data via in-process client (bukan HTTP ke port eksternal)."""
    payload = {
        "seed": 123,
        "level": 3,
        "type": "complementary",
    }

    resp = client.post("/api/v1/angles/generate", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["meta"]["type"] == "complementary"
    assert "drawing_data" in data["data"]
    assert list(data["data"]["drawing_data"]["points"].keys())


def test_parallel_lines():
    """Parallel lines relationships (level >= 4)."""
    payload = {
        "seed": 123,
        "level": 5,
        "type": "parallel_lines",
    }

    resp = client.post("/api/v1/angles/generate", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert "parallel_lines" in data["meta"]["type"]
    assert data["data"]["drawing_data"]["type"] == "parallel_lines_schema"


def test_invalid_angle_type_is_rejected():
    """Tipe tidak dikenal harus ditolak (regression guard untuk kontrak API)."""
    resp = client.post(
        "/api/v1/angles/generate",
        json={"seed": 1, "level": 2, "type": "tidak_ada"},
    )
    assert resp.status_code in (400, 422), resp.text


if __name__ == "__main__":
    test_angles_complementary()
    test_parallel_lines()
    print(json.dumps({"status": "ok"}, indent=2))

