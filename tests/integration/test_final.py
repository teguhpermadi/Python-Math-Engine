"""Test domain measurement/algebra/statistics via in-process TestClient."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_measurement():
    resp = client.post("/api/v1/measurement/generate", json={"seed": 1, "level": 2})
    assert resp.status_code == 200, resp.text
    assert "expression" in resp.json()["data"]


def test_algebra():
    resp = client.post("/api/v1/algebra/generate", json={"seed": 1, "level": 2})
    assert resp.status_code == 200, resp.text
    assert "expression" in resp.json()["data"]


def test_statistics():
    resp = client.post("/api/v1/statistics/generate", json={"seed": 1, "level": 2})
    assert resp.status_code == 200, resp.text
    assert "results" in resp.json()["data"]
    assert "mean" in resp.json()["data"]["results"]


def test_arithmetic_all_operations():
    """Regression: seluruh operasi yang diiklankan /arithmetic/levels harus 200.

    gcd/lcm/factorization/modulo diizinkan lintas number_type integer-ish
    (konsisten dengan model_validator ArithmeticRequest).
    """
    cases = [
        {"operation": "addition", "number_type": "natural", "operand_count": 3},
        {"operation": "subtraction", "number_type": "natural"},
        {"operation": "multiplication", "number_type": "natural"},
        {"operation": "division", "number_type": "natural"},
        {"operation": "power", "number_type": "natural"},
        {"operation": "root", "number_type": "natural"},
        {"operation": "modulo", "number_type": "natural"},
        {"operation": "gcd", "number_type": "natural"},
        {"operation": "lcm", "number_type": "natural"},
        {"operation": "mixed", "number_type": "natural"},
        {"operation": "comparison", "number_type": "natural"},
        {"operation": "ordering", "number_type": "natural"},
        {"operation": "factorization", "number_type": "natural"},
    ]
    for case in cases:
        payload = {"seed": 11, "level": 3, **case}
        resp = client.post("/api/v1/arithmetic/generate", json=payload)
        assert resp.status_code == 200, f"{case}: {resp.status_code} - {resp.text}"
        assert resp.json()["data"]["correct_answer"], case


if __name__ == "__main__":
    test_measurement()
    test_algebra()
    test_statistics()
    test_arithmetic_all_operations()
    print("ALL DOMAINS VERIFIED SUCCESS.")

