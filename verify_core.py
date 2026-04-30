import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.core.seed.manager import SeedManager
from app.core.number_types.registry import NumberType
from app.core.levels.config import get_level_config
from app.core.number_types.generators import generate_number

def test_seed_reproducibility():
    seed = 42
    level = 3
    num_type = NumberType.NATURAL
    
    config = get_level_config(level)
    
    # First run
    manager1 = SeedManager(seed)
    rng1 = manager1.get_rng()
    results1 = [generate_number(num_type, config, rng1) for _ in range(5)]
    
    # Second run
    manager2 = SeedManager(seed)
    rng2 = manager2.get_rng()
    results2 = [generate_number(num_type, config, rng2) for _ in range(5)]
    
    print(f"Run 1: {results1}")
    print(f"Run 2: {results2}")
    
    assert results1 == results2
    print("SUCCESS: Seed reproducibility test passed!")

def test_different_seeds():
    seed1 = 42
    seed2 = 43
    level = 3
    num_type = NumberType.NATURAL
    
    config = get_level_config(level)
    
    rng1 = SeedManager(seed1).get_rng()
    results1 = [generate_number(num_type, config, rng1) for _ in range(5)]
    
    rng2 = SeedManager(seed2).get_rng()
    results2 = [generate_number(num_type, config, rng2) for _ in range(5)]
    
    print(f"Seed 42: {results1}")
    print(f"Seed 43: {results2}")
    
    assert results1 != results2
    print("SUCCESS: Different seeds produce different results test passed!")

if __name__ == "__main__":
    try:
        test_seed_reproducibility()
        test_different_seeds()
    except Exception as e:
        print(f"ERROR: Test failed: {e}")
        sys.exit(1)
