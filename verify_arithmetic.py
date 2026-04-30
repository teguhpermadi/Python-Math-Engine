import sys
import os

sys.path.append(os.getcwd())

from app.core.seed.manager import SeedManager, SeedContext
from app.core.number_types.registry import NumberType
from app.core.levels.config import get_level_config
from app.core.arithmetic.addition import generate_addition
from app.core.arithmetic.subtraction import generate_subtraction
from app.core.arithmetic.multiplication import generate_multiplication
from app.core.arithmetic.division import generate_division
from app.core.arithmetic.power import generate_power
from app.core.arithmetic.root import generate_root

def test_operation(name, generator, **kwargs):
    print(f"\n--- Testing {name} ---")
    seed = 42
    level = 3
    num_type = NumberType.NATURAL
    
    ctx = SeedContext(seed=seed, operation=name, level=level, number_type=num_type.value)
    manager = SeedManager(ctx)
    config = get_level_config(level)
    
    # Run twice for reproducibility
    res1 = generator(manager.rng, config, num_type, **kwargs)
    
    # Re-init manager for run 2
    manager2 = SeedManager(ctx)
    res2 = generator(manager2.rng, config, num_type, **kwargs)
    
    # ASCII-safe printing
    safe_expr = res1['expression'].replace("×", "*").replace("÷", "/").replace("√", "sqrt")
    # Replace superscripts
    for s, p in {"⁰": "^0", "¹": "^1", "²": "^2", "³": "^3", "⁴": "^4", "⁵": "^5", "⁶": "^6", "⁷": "^7", "⁸": "^8", "⁹": "^9"}.items():
        safe_expr = safe_expr.replace(s, p)
    print(f"Expression: {safe_expr}")
    print(f"Result: {res1['result']} ({res1['result_type']})")
    
    assert res1 == res2
    print(f"SUCCESS: {name} is reproducible.")
    return res1

def test_subtraction_constraints():
    print("\n--- Testing Subtraction Constraints ---")
    # Level 1 should not have negative results
    level1 = get_level_config(1)
    num_type = NumberType.NATURAL
    
    for i in range(20):
        ctx = SeedContext(seed=i, operation="subtraction", level=1, number_type=num_type.value)
        rng = SeedManager(ctx).rng
        res = generate_subtraction(rng, level1, num_type)
        if int(res['result']) < 0:
            raise Exception(f"Level 1 subtraction produced negative result: {res['expression']} = {res['result']}")
    
    print("SUCCESS: Level 1 subtraction always >= 0.")

if __name__ == "__main__":
    try:
        test_operation("addition", generate_addition)
        test_operation("subtraction", generate_subtraction)
        test_operation("multiplication", generate_multiplication)
        test_operation("division", generate_division)
        test_operation("power", generate_power)
        test_operation("root", generate_root)
        
        test_subtraction_constraints()
        
        print("\nALL ARITHMETIC TESTS PASSED!")
    except Exception as e:
        print(f"\nERROR: Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
