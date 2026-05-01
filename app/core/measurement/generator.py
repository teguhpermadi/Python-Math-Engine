import random
from .units import LENGTH_UNITS, MASS_UNITS, TIME_UNITS, convert_unit
from ..levels.config import LevelConfig

def generate_conversion_problem(rng: random.Random, level_config: LevelConfig):
    unit_types = ["length", "mass"]
    if level_config.level >= 2: unit_types.append("time")
    
    unit_type = rng.choice(unit_types)
    table = LENGTH_UNITS if unit_type == "length" else MASS_UNITS if unit_type == "mass" else TIME_UNITS
    
    units = list(table.keys())
    from_unit = rng.choice(units)
    to_unit = rng.choice([u for u in units if u != from_unit])
    
    # Generate clean values
    value = rng.randint(1, level_config.level * 10)
    result = convert_unit(value, from_unit, to_unit, unit_type)
    
    # Format result string
    if result.is_integer():
        result_str = str(int(result))
    else:
        result_str = f"{result:g}" # Standard scientific/float notation without trailing zeros
        
    expression = f"{value} {from_unit} = ... {to_unit}"
    
    return {
        "unit_type": unit_type,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "value": value,
        "result": result_str,
        "expression": expression
    }
