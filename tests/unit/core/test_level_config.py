"""
Test LevelConfig and LEVEL_REGISTRY.
TRD Section 7 - Arithmetic Level System
"""
import pytest
from app.core.levels.config import get_level_config, LEVEL_REGISTRY, LevelConfig


class TestLevelConfig:
    """Tests for level configuration system."""

    def test_get_level_config_valid(self):
        """Should return config for valid level."""
        config = get_level_config(1)
        assert config.level == 1
        assert config.max_value == 10

    def test_get_level_config_invalid(self):
        """Should raise error for invalid level."""
        with pytest.raises(Exception):
            get_level_config(99)

    def test_level_1_allows_natural_whole(self):
        """Level 1 should allow natural and whole number types."""
        config = get_level_config(1)
        type_names = [t.value for t in config.allowed_number_types]
        assert "natural" in type_names
        assert "whole" in type_names
