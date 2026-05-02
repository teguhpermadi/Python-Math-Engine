"""
Test SeedManager reproducibility.
TRD Section 16.2 - Mandatory: Seed Reproducibility
"""
import pytest
from app.core.seed.manager import SeedManager


class TestSeedManager:
    """Tests for seed-based generation consistency."""

    def test_same_seed_produces_same_rng(self):
        """Same seed should produce identical Random objects."""
        sm1 = SeedManager(42)
        sm2 = SeedManager(42)
        rng1 = sm1.get_rng()
        rng2 = sm2.get_rng()
        assert rng1.randint(1, 100) == rng2.randint(1, 100)

    def test_different_seed_produces_different_rng(self):
        """Different seeds should produce different results."""
        sm1 = SeedManager(42)
        sm2 = SeedManager(99)
        rng1 = sm1.get_rng()
        rng2 = sm2.get_rng()
        # Very low probability of being equal
        assert rng1.randint(1, 100) != rng2.randint(1, 100)
