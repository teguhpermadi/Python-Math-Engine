"""
Test Seed reproducibility - MANDATORY.
TRD Section 16.2 - Seed Reproducibility Test

Dijalankan in-process via fixture `client` (tests/conftest.py) sehingga
tidak bergantung pada port server yang sedang berjalan.
"""


def test_same_seed_same_output(client):
    """Two requests with same seed & params MUST produce identical output."""
    params = {
        "seed": 42,
        "level": 3,
        "operation": "addition",
        "number_type": "fraction",
        "with_story": False,
        "with_distractors": False,
    }
    resp1 = client.post("/api/v1/arithmetic/generate", json=params)
    resp2 = client.post("/api/v1/arithmetic/generate", json=params)

    assert resp1.status_code == 200, resp1.text
    assert resp2.status_code == 200, resp2.text
    assert resp1.json()["data"]["expression"] == resp2.json()["data"]["expression"]
    assert resp1.json()["data"]["correct_answer"] == resp2.json()["data"]["correct_answer"]


def test_different_seed_different_output(client):
    """Different seeds should produce different results."""
    params1 = {
        "seed": 42,
        "level": 3,
        "operation": "addition",
        "number_type": "natural",
        "with_story": False,
    }
    params2 = {
        "seed": 99,
        "level": 3,
        "operation": "addition",
        "number_type": "natural",
        "with_story": False,
    }
    resp1 = client.post("/api/v1/arithmetic/generate", json=params1)
    resp2 = client.post("/api/v1/arithmetic/generate", json=params2)

    assert resp1.status_code == 200, resp1.text
    assert resp2.status_code == 200, resp2.text
    # Different seeds must map to different meta.seed values
    assert resp1.json()["meta"]["seed"] != resp2.json()["meta"]["seed"]


def test_same_seed_context_produces_same_output(client):
    """Same seed + same (operation, level, number_type) → identical result
    (TRD §16.2: determinisme atas konteks penuh, bukan seed saja)."""
    params = {
        "seed": 777,
        "level": 2,
        "operation": "multiplication",
        "number_type": "whole",
        "with_story": False,
        "with_distractors": True,
    }
    resp1 = client.post("/api/v1/arithmetic/generate", json=params)
    resp2 = client.post("/api/v1/arithmetic/generate", json=params)

    assert resp1.status_code == 200, resp1.text
    assert resp1.json() == resp2.json()

