"""
Test SeedManager reproducibility.
TRD Section 16.2 - Mandatory: Seed Reproducibility
"""
from app.core.seed.manager import SeedManager, SeedContext


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

    def test_same_seed_context_produces_same_rng(self):
        """Same SeedContext must produce identical RNG streams (TRD §16.2)."""
        ctx = SeedContext(seed=42, operation="addition", level=3, number_type="fraction")
        sm1 = SeedManager(ctx)
        sm2 = SeedManager(ctx)
        assert sm1.rng.random() == sm2.rng.random()

    def test_same_seed_different_context_produces_different_rng(self):
        """Same seed but different operation/level/number_type → different stream."""
        sm1 = SeedManager(SeedContext(seed=42, operation="addition", level=1, number_type="natural"))
        sm2 = SeedManager(SeedContext(seed=42, operation="addition", level=5, number_type="natural"))
        # Probability of equality is negligible
        assert sm1.rng.random() != sm2.rng.random()

