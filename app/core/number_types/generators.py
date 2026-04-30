import random
from fractions import Fraction
from sympy import isprime, primerange
from .registry import NumberType
from ..levels.config import LevelConfig

def generate_number(
    number_type: NumberType,
    level_config: LevelConfig,
    rng: random.Random
) -> int | float | Fraction:
    """
    Menghasilkan satu bilangan sesuai tipe dan konfigurasi level.
    Selalu menggunakan `rng` (seeded).
    """
    match number_type:
        case NumberType.NATURAL | NumberType.INTEGER_POS | NumberType.WHOLE:
            lo = 0 if number_type == NumberType.WHOLE else 1
            return rng.randint(lo, level_config.max_value)

        case NumberType.INTEGER:
            val = rng.randint(1, level_config.max_value)
            return val if rng.random() > 0.5 else -val

        case NumberType.INTEGER_NEG:
            return -rng.randint(1, level_config.max_value)

        case NumberType.PRIME:
            primes = list(primerange(2, level_config.max_value + 1))
            if not primes:
                return 2 # Fallback
            return rng.choice(primes)

        case NumberType.COMPOSITE:
            composites = [n for n in range(4, level_config.max_value + 1)
                          if not isprime(n)]
            if not composites:
                return 4 # Fallback
            return rng.choice(composites)

        case NumberType.DECIMAL:
            val = round(rng.uniform(level_config.min_decimal, level_config.max_decimal),
                        level_config.decimal_places)
            return val

        case NumberType.FRACTION:
            if not level_config.allowed_denominators:
                return Fraction(1, 2) # Fallback
            denom = rng.choice(level_config.allowed_denominators)
            numer = rng.randint(1, denom - 1)
            return Fraction(numer, denom)

        case NumberType.MIXED_FRACTION:
            if not level_config.allowed_denominators:
                return Fraction(3, 2) # Fallback
            whole_part = rng.randint(1, level_config.max_mixed_whole)
            denom = rng.choice(level_config.allowed_denominators)
            numer = rng.randint(1, denom - 1)
            return Fraction(whole_part * denom + numer, denom)

        case NumberType.REAL:
            if not level_config.real_sub_types:
                return rng.randint(1, level_config.max_value)
            sub_type = rng.choice(level_config.real_sub_types)
            return generate_number(sub_type, level_config, rng)

    return rng.randint(1, 10) # Default fallback
