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
    
    # Test Determinism: Second request with same seed should be identical
    response2 = client.post("/api/v1/exam/generate", json={
        "master_seed": 999,
        "requirements": [
            {"domain": "arithmetic", "operation": "addition", "level": 1},
            {"domain": "geometry", "shape": "block", "level": 2},
            {"domain": "algebra", "level": 3}
        ]
    })
    assert response.json() == response2.json()
