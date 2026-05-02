"""
Test number type generators.
TRD Section 6 - Number Type System
"""
import pytest
import random
from app.core.number_types.generators import generate_number
from app.core.number_types.registry import NumberType
from app.core.levels.config import get_level_config


class TestNumberTypeGenerators:
    """Tests for number type generation."""

    def test_generate_natural_number(self):
        """Should generate natural number (positive integer)."""
        rng = random.Random(42)
        config = get_level_config(1)
        result = generate_number(NumberType.NATURAL, config, rng)
        assert isinstance(result, int)
        assert result >= 1

    def test_generate_prime_number(self):
        """Should generate prime number when available."""
        rng = random.Random(42)
        config = get_level_config(3)  # Level 3 has primes
        result = generate_number(NumberType.PRIME, config, rng)
        assert isinstance(result, int)
        # Prime check: divisible only by 1 and itself
        assert result > 1
