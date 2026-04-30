import sys
import os

sys.path.append(os.getcwd())

from app.core.seed.manager import SeedManager, SeedContext
from app.core.number_types.registry import NumberType
from app.core.levels.config import get_level_config
from app.core.arithmetic.modulo import generate_modulo
from app.core.arithmetic.number_properties import generate_gcd_problem, generate_lcm_problem, generate_factorization_problem
from app.core.arithmetic.comparison import generate_comparison, generate_ordering
from app.core.arithmetic.mixed_operations import generate_mixed_operations

def test_adv_op(name, generator, **kwargs):
    print(f"\n--- Testing {name} ---")
    seed = 100
    level = 4
    num_type = NumberType.NATURAL
    
    ctx = SeedContext(seed=seed, operation=name, level=level, number_type=num_type.value)
    manager = SeedManager(ctx)
    config = get_level_config(level)
    
    res = generator(manager.rng, config, num_type, **kwargs)
    
    safe_expr = res['expression'].replace("×", "*").replace("÷", "/").replace("√", "sqrt")
    print(f"Expression: {safe_expr}")
    print(f"Result: {res['result']}")
    
    # Verify steps exist
    assert "steps" in res
    print(f"SUCCESS: {name} generated with steps.")
    return res

if __name__ == "__main__":
    try:
        test_adv_op("modulo", generate_modulo)
        test_adv_op("gcd", lambda r, c, n: generate_gcd_problem(r, c))
        test_adv_op("lcm", lambda r, c, n: generate_lcm_problem(r, c))
        test_adv_op("factorization", lambda r, c, n: generate_factorization_problem(r, c))
        test_adv_op("comparison", generate_comparison)
        test_adv_op("ordering", generate_ordering)
        test_adv_op("mixed", generate_mixed_operations)
        
        print("\nALL ADVANCED ARITHMETIC TESTS PASSED!")
    except Exception as e:
        print(f"\nERROR: Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
