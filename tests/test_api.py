import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_arithmetic_generate():
    response = client.post("/api/v1/arithmetic/generate", json={
        "seed": 42, "level": 1, "operation": "addition", "number_type": "natural"
    })
    assert response.status_code == 200
    assert "expression" in response.json()["data"]

def test_geometry_generate():
    response = client.post("/api/v1/geometry/generate", json={
        "seed": 42, "level": 3, "shape": "cube"
    })
    assert response.status_code == 200
    assert "mesh" in response.json()["data"]

def test_exam_pack():
    response = client.post("/api/v1/exam/generate", json={
        "master_seed": 999,
        "requirements": [
            {"domain": "arithmetic", "operation": "addition", "level": 1},
            {"domain": "geometry", "shape": "block", "level": 2},
            {"domain": "algebra", "level": 3}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["total_questions"] == 3
    assert len(data["questions"]) == 3
    
    response2 = client.post("/api/v1/exam/generate", json={
        "master_seed": 999,
        "requirements": [
            {"domain": "arithmetic", "operation": "addition", "level": 1},
            {"domain": "geometry", "shape": "block", "level": 2},
            {"domain": "algebra", "level": 3}
        ]
    })
    assert response.json() == response2.json()

def test_geometry_nets_shapes():
    response = client.get("/api/v1/geometry/nets/shapes")
    assert response.status_code == 200
    shapes = response.json()
    assert len(shapes) == 6
    assert any(s["type"] == "cube" for s in shapes)

def test_geometry_nets_generate_valid():
    response = client.post("/api/v1/geometry/nets/generate", json={
        "shape": "cube", "seed": 42, "is_valid": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["shape"] == "cube"
    assert data["is_valid"] is True
    assert data["error_reason"] is None
    assert len(data["faces"]) == 6

def test_geometry_nets_generate_invalid():
    response = client.post("/api/v1/geometry/nets/generate", json={
        "shape": "cube", "seed": 42, "is_valid": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["shape"] == "cube"
    assert data["is_valid"] is False
    assert isinstance(data["error_reason"], str)
    assert len(data["faces"]) > 0

