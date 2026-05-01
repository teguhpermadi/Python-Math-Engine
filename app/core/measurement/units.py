# Unit Conversion Tables (Metric Base)

LENGTH_UNITS = {
    "km": 1000,
    "hm": 100,
    "dam": 10,
    "m": 1,
    "dm": 0.1,
    "cm": 0.01,
    "mm": 0.001
}

MASS_UNITS = {
    "kg": 1000,
    "hg": 100,
    "dag": 10,
    "g": 1,
    "dg": 0.1,
    "cg": 0.01,
    "mg": 0.001
}

TIME_UNITS = {
    "hour": 3600,
    "minute": 60,
    "second": 1
}

def convert_unit(value: float, from_unit: str, to_unit: str, unit_type: str = "length") -> float:
    table = LENGTH_UNITS if unit_type == "length" else MASS_UNITS if unit_type == "mass" else TIME_UNITS
    
    if from_unit not in table or to_unit not in table:
        raise ValueError(f"Unit {from_unit} or {to_unit} not supported for {unit_type}")
        
    # Convert to base unit (m, g, or second)
    base_value = value * table[from_unit]
    # Convert to target unit
    return base_value / table[to_unit]
