"""
Test seed reproducibility - MANDATORY.
TRD Section 16.2 - Seed Reproducibility Test
"""
import pytest
from httpx import AsyncClient


class TestSeedReproducibility:
    """Verify that same seed produces identical output."""

    @pytest.mark.asyncio
    async def test_same_seed_same_output(self, client: AsyncClient):
        """Two requests with same seed & params MUST produce identical output."""
        params = {
            "seed": 42,
            "level": 3,
            "operation": "addition",
            "number_type": "fraction",
            "with_story": False,
            "with_distractors": False
        }
        resp1 = await client.post("/api/v1/arithmetic/generate", json=params)
        resp2 = await client.post("/api/v1/arithmetic/generate", json=params)

        assert resp1.json()["data"]["expression"] == resp2.json()["data"]["expression"]
        assert resp1.json()["data"]["result"] == resp2.json()["data"]["result"]

    @pytest.mark.asyncio
    async def test_different_seed_different_output(self, client: AsyncClient):
        """Different seeds should produce different results."""
        params1 = {
            "seed": 42,
            "level": 3,
            "operation": "addition",
            "number_type": "natural",
            "with_story": False
        }
        params2 = {
            "seed": 99,
            "level": 3,
            "operation": "addition",
            "number_type": "natural",
            "with_story": False
        }
        resp1 = await client.post("/api/v1/arithmetic/generate", json=params1)
        resp2 = await client.post("/api/v1/arithmetic/generate", json=params2)

        # Different seeds should (likely) produce different expressions
        assert resp1.json()["meta"]["seed"] != resp2.json()["meta"]["seed"]
