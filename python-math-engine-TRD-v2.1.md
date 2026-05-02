# 📐 Technical Requirement Document: Python Math Engine for CBT

> **Version:** 2.1.0 | **Status:** Draft | **Framework:** FastAPI (Python 3.11+)
> **Changelog v2.1:** Added exam & angles modules, fixed typos, improved structure

---

## Table of Contents

1. [Project Summary](#1-project-summary)
2. [Core Concepts: Level, Number Type & Seed](#2-core-concepts-level-number-type--seed)
3. [System Architecture](#3-system-architecture)
4. [Tech Stack & Dependencies](#4-tech-stack--dependencies)
5. [Directory Structure (v2.1)](#5-directory-structure-v21)
6. [Number Type System](#6-number-type-system)
7. [Arithmetic Level System](#7-arithmetic-level-system)
8. [Core Arithmetic — Module Specifications](#8-core-arithmetic--module-specifications)
9. [Angles & Geometry Helpers](#9-angles--geometry-helpers)
10. [Seed-Based Generation System](#10-seed-based-generation-system)
11. [Layer Service & Blueprint](#11-layer-service--blueprint)
12. [Schemas (JSON Contracts)](#12-schemas-json-contracts)
13. [API Endpoint Specification](#13-api-endpoint-specification)
14. [Code Standards & Conventions](#14-code-standards--conventions)
15. [Error Handling](#15-error-handling)
16. [Testing Strategy](#16-testing-strategy)
17. [Environment & Configuration](#17-environment--configuration)
18. [Work Plan (Roadmap)](#18-work-plan-roadmap)
19. [Architecture Decision Records (ADR)](#19-architecture-decision-records-adr)

---

## 1. Project Summary

**Python Math Engine** is a REST API-based *microservice* that functions as a mathematical backend for **CBT (Computer Based Test)** applications. This system generates math problems that are *reproducible* (can be repeated with the same seed), structured per level, and supports various number types.

### 1.1 Core Responsibilities

| Responsibility | Description |
|---|---|
| **Seed-Based Math Generation** | Same seed produces same math problems |
| **Level-Based Difficulty** | Difficulty parameter as integer (Level 1–N) |
| **Number Type System** | Supports 12+ different number types |
| **Precision Arithmetic** | Free from floating-point errors using `Fraction` and `Decimal` |
| **Logic Blueprinting** | Operation sequence as drag-and-drop answer key |
| **Distractor Logic** | Wrong answers based on student misconceptions per operation |
| **AI Contextualization** | Word problems via local LM Studio |
| **Geometry Mesh Computing** | 3D coordinates for Three.js renderer |

### 1.2 System Constraints

- ✅ Stateless — each request stands alone
- ✅ Reproducible — same seed → same problems
- ✅ Supports multi-step mixed operations
- ❌ Does not store problem data to database
- ❌ Does not manage student sessions or exam results
- ❌ Does not perform visual rendering (delegated to React)

---

## 2. Core Concepts: Level, Number Type & Seed

These are the three main pillars of the problem generation system in v2.

### 2.1 Level (Difficulty Parameter)

Level is an **integer** that represents the overall complexity of a problem. Level controls:

- Range of number values used
- Number types allowed
- Number of operations in mixed problems
- Structural complexity (e.g., multi-step vs single-step)

```
Level 1  → Easiest    (small whole numbers, single operation)
Level 2  → Easy
Level 3  → Medium
Level 4  → Moderately difficult
Level 5  → Difficult
Level 6  → Very difficult
Level 7  → Expert (complex mixed operations, real numbers)
...
Level N  → Can be developed according to curriculum needs
```

> **Design Decision:** Using numbers (not "easy/medium/hard") for more granularity, can be developed without changing API, and easily mapped to grade levels (Level 1 = Grade 1, etc.).

### 2.2 Number Type

Number Type is the **type of number** used as operands in problems. This is separate from level — level controls *complexity*, number type controls *number type*.

### 2.3 Seed

Seed is an **integer** that serves as a deterministic key for PRNG (Pseudo-Random Number Generator). With the same seed and same parameters, the engine will always generate identical problems.

```
seed=42, operation="addition", level=3, number_type="fraction"
→ Always generates: 3/7 + 5/14
```

---

## 3. System Architecture

### 3.1 Data Flow Diagram

```
┌──────────────┐    POST /arithmetic/generate     ┌────────────────────────────┐
│   Laravel    │ ──────────────────────────────►  │    Python Math Engine      │
│  (Orchestr.) │ ◄──────────────────────────────  │       (FastAPI)            │
└──────────────┘         JSON Response            └────────────┬───────────────┘
                                                                │
                     ┌──────────────────────────────────────────┼──────────────────┐
                     ▼                                          ▼                  ▼
              ┌─────────────┐                        ┌──────────────────┐  ┌────────────┐
              │ NumberType  │                        │  SeedManager     │  │ LM Studio  │
              │  Resolver   │                        │  (random.seed)   │  │ (Local AI) │
              └──────┬──────┘                        └────────┬─────────┘  └────────────┘
                     │                                        │
                     ▼                                        ▼
              ┌─────────────────────────────────────────────────────┐
              │              Core Arithmetic Layer                  │
              │  addition / subtraction / multiplication / division  │
              │  power / root / mixed_operation / etc.              │
              └─────────────────────────────────────────────────────┘
```

### 3.2 Architecture Principles

1. **Seed-First** — SeedManager initialized before any generator is called
2. **Number Type as Constraint** — each operation receives `NumberType` as domain filter
3. **Pure Functions in Core** — no I/O, no side effects
4. **Level as Config Bundle** — each level maps to a `LevelConfig` containing all parameters

---

## 4. Tech Stack & Dependencies

```toml
# requirements.txt

# Web Framework
fastapi==0.111.0
uvicorn[standard]==0.29.0

# Data Validation
pydantic==2.7.0
pydantic-settings==2.2.1

# Mathematics — Precision
sympy==1.12            # Symbolic: simplification, primality check, factorization
numpy==1.26.4          # Geometry computation & arrays

# Utilities
python-dotenv==1.0.1
httpx==0.27.0          # Async HTTP for LM Studio

# requirements-dev.txt
pytest==8.2.0
pytest-asyncio==0.23.6
ruff==0.4.4
mypy==1.10.0
```

> **Note:** `fractions` and `decimal` libraries are Python stdlib — no additional installation needed.

---

## 5. Directory Structure (v2.1)

```text
python-math-engine/
│
├── app/
│   ├── main.py                          # Entry point FastAPI & router registration
│   ├── config.py                        # Settings via pydantic-settings
│   ├── exceptions.py                    # Custom exception hierarchy
│   │
│   ├── core/                            # LAYER 1: Pure Mathematical Engine
│   │   │
│   │   ├── number_types/                # ★ NEW: Number type definitions & validators
│   │   │   ├── __init__.py
│   │   │   ├── registry.py              # Enum & mapping all NumberTypes
│   │   │   ├── validators.py            # Check functions: is_prime(), is_composite(), etc.
│   │   │   └── generators.py           # Number generators per type & level
│   │   │
│   │   ├── seed/                        # ★ NEW: Seed management
│   │   │   ├── __init__.py
│   │   │   └── manager.py              # SeedManager class (random wrapper)
│   │   │
│   │   ├── levels/                      # ★ NEW: Level configuration definitions
│   │   │   ├── __init__.py
│   │   │   └── config.py               # LevelConfig dataclass & registry level 1-7+
│   │   │
│   │   ├── arithmetic/                  # ★ RESTRUCTURED: One file per operation
│   │   │   ├── __init__.py
│   │   │   ├── addition.py              # Addition
│   │   │   ├── subtraction.py          # Subtraction
│   │   │   ├── multiplication.py       # Multiplication
│   │   │   ├── division.py             # Division
│   │   │   ├── power.py                # Exponentiation
│   │   │   ├── root.py                 # Root extraction
│   │   │   ├── modulo.py               # Modulo / remainder operation
│   │   │   ├── mixed_operations.py     # Multi-step mixed operations
│   │   │   ├── number_properties.py    # GCD, LCM, factors, multiples
│   │   │   └── comparison.py           # Comparison & number ordering
│   │   │
│   │   ├── geometry/
│   │   │   ├── __init__.py
│   │   │   ├── shapes_2d.py
│   │   │   ├── shapes_3d.py
│   │   │   ├── mesh_generator.py
│   │   │   ├── composite.py
│   │   │   ├── angles.py               # ★ NEW: Angle generation
│   │   │   └── lines.py                 # ★ NEW: Line helpers for angles
│   │   │
│   │   ├── measurement/
│   │   │   ├── __init__.py
│   │   │   ├── length.py
│   │   │   ├── weight.py
│   │   │   ├── volume.py
│   │   │   └── time.py
│   │   │
│   │   ├── algebra/
│   │   │   ├── __init__.py
│   │   │   ├── linear_equation.py
│   │   │   └── number_pattern.py
│   │   │
│   │   ├── statistics/
│   │   │   ├── __init__.py
│   │   │   ├── central_tendency.py
│   │   │   └── chart_data.py
│   │   │
│   │   └── probability/
│   │       ├── __init__.py
│   │       └── sample_space.py
│   │
│   ├── services/                        # LAYER 2: Business Logic & Context Engine
│   │   ├── __init__.py
│   │   ├── ai_storyteller.py
│   │   ├── blueprint.py
│   │   ├── distractor.py
│   │   ├── arithmetic_service.py        # Coordination: core → blueprint
│   │   ├── geometry_service.py
│   │   ├── measurement_service.py
│   │   ├── algebra_service.py
│   │   ├── statistics_service.py
│   │   ├── angle_service.py              # ★ NEW: Angle question service
│   │   ├── exam_service.py                # ★ NEW: Exam pack generation
│   │   └── probability_service.py
│   │
│   ├── schemas/                         # LAYER 3: Pydantic Models
│   │   ├── __init__.py
│   │   ├── request.py
│   │   └── response.py
│   │
│   └── routers/                         # FastAPI Routers per domain
│       ├── __init__.py
│       ├── arithmetic.py
│       ├── geometry.py
│       ├── measurement.py
│       ├── algebra.py
│       ├── statistics.py
│       ├── angles.py                   # ★ NEW: Angles endpoints
│       ├── exam.py                     # ★ NEW: Exam pack endpoint
│       └── probability.py
│
├── tests/
│   ├── unit/
│   │   ├── core/
│   │   │   ├── test_number_types.py
│   │   │   ├── test_seed_manager.py
│   │   │   ├── test_level_config.py
│   │   │   ├── test_addition.py
│   │   │   ├── test_subtraction.py
│   │   │   ├── test_multiplication.py
│   │   │   ├── test_division.py
│   │   │   ├── test_power.py
│   │   │   ├── test_root.py
│   │   │   ├── test_mixed_operations.py
│   │   │   └── test_number_properties.py
│   │   └── services/
│   │       ├── test_blueprint.py
│   │       └── test_distractor.py
│   └── integration/
│       ├── test_arithmetic_endpoint.py
│       └── test_seed_reproducibility.py  # ★ Important: test seed produces same output
│
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## 6. Number Type System

### 6.1 Number Type Registry

File: `app/core/number_types/registry.py`

```python
from enum import Enum

class NumberType(str, Enum):
    """
    All number types supported by the engine.
    String values are used directly as API parameters.
    """
    # ── Set-based Numbers ──────────────────────────────────────────
    NATURAL        = "natural"        # Natural numbers: {1, 2, 3, ...}
    WHOLE          = "whole"          # Whole numbers: {0, 1, 2, 3, ...}
    INTEGER        = "integer"        # Integers: {..., -2, -1, 0, 1, 2, ...}
    INTEGER_POS    = "integer_pos"    # Positive integers: {1, 2, 3, ...}
    INTEGER_NEG    = "integer_neg"    # Negative integers: {..., -3, -2, -1}
    REAL           = "real"           # Real numbers (encompasses all below)

    # ── Property-based Numbers ─────────────────────────────────────
    PRIME          = "prime"          # Prime numbers: {2, 3, 5, 7, 11, ...}
    COMPOSITE      = "composite"      # Composite numbers: {4, 6, 8, 9, 10, ...}

    # ── Representation-based Numbers ─────────────────────────────────────
    DECIMAL        = "decimal"        # Decimal: 1.5, 3.14, 0.25
    FRACTION       = "fraction"       # Common fraction: 1/2, 3/4, 5/6
    MIXED_FRACTION = "mixed_fraction" # Mixed fraction: 1½, 2¾, 3⅓
```

### 6.2 Definitions & Constraints per Type

| NumberType | Set | Example Values | Negative? | Zero? | Decimal? |
|---|---|---|---|---|---|
| `natural` | ℕ = {1, 2, 3, ...} | 1, 5, 100 | ❌ | ❌ | ❌ |
| `whole` | ℕ₀ = {0, 1, 2, ...} | 0, 1, 50 | ❌ | ✅ | ❌ |
| `integer` | ℤ = {...,-1, 0, 1,...} | -5, 0, 12 | ✅ | ✅ | ❌ |
| `integer_pos` | ℤ⁺ = {1, 2, 3, ...} | 1, 7, 99 | ❌ | ❌ | ❌ |
| `integer_neg` | ℤ⁻ = {...,-2,-1} | -1, -8, -50 | ✅ | ❌ | ❌ |
| `prime` | {2,3,5,7,11,...} | 2, 13, 97 | ❌ | ❌ | ❌ |
| `composite` | {4,6,8,9,10,...} | 4, 15, 100 | ❌ | ❌ | ❌ |
| `decimal` | Subset ℝ | 1.5, 3.14, 0.5 | ✅ | ✅ | ✅ |
| `fraction` | Subset ℚ | 1/2, 3/4, 7/8 | ✅ | ❌ | — |
| `mixed_fraction` | Subset ℚ | 1½, 2¾ | ❌ | ❌ | — |
| `real` | ℝ (combination) | All above | ✅ | ✅ | ✅ |

### 6.3 Number Generator Implementation

File: `app/core/number_types/generators.py`

```python
import random
from fractions import Fraction
from sympy import isprime, primerange
from .registry import NumberType

def generate_number(
    number_type: NumberType,
    level_config: "LevelConfig",
    rng: random.Random
) -> int | float | Fraction:
    """
    Generate a number according to type and level configuration.
    Always uses `rng` (seeded) — never calls random directly.

    Args:
        number_type:  Desired number type
        level_config: Level configuration with ranges
        rng:          Seeded random.Random instance

    Returns:
        Number according to type: int, float, or Fraction
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
            return rng.choice(primes)

        case NumberType.COMPOSITE:
            composites = [n for n in range(4, level_config.max_value + 1)
                          if not isprime(n)]
            return rng.choice(composites)

        case NumberType.DECIMAL:
            val = round(rng.uniform(level_config.min_decimal, level_config.max_decimal),
                        level_config.decimal_places)
            return val

        case NumberType.FRACTION:
            denom = rng.choice(level_config.allowed_denominators)
            numer = rng.randint(1, denom - 1)
            return Fraction(numer, denom)  # Auto-simplified

        case NumberType.MIXED_FRACTION:
            whole_part = rng.randint(1, level_config.max_mixed_whole)
            denom = rng.choice(level_config.allowed_denominators)
            numer = rng.randint(1, denom - 1)
            return Fraction(whole_part * denom + numer, denom)

        case NumberType.REAL:
            # Randomly select subtype from level-allowed types
            sub_type = rng.choice(level_config.real_sub_types)
            return generate_number(sub_type, level_config, rng)
```

### 6.4 Validator Implementation

File: `app/core/number_types/validators.py`

```python
from fractions import Fraction
from sympy import isprime as sympy_isprime

def is_prime(n: int) -> bool:
    return n > 1 and sympy_isprime(n)

def is_composite(n: int) -> bool:
    return n > 1 and not sympy_isprime(n)

def is_whole(n) -> bool:
    return isinstance(n, int) and n >= 0

def is_natural(n) -> bool:
    return isinstance(n, int) and n >= 1

def is_proper_fraction(f: Fraction) -> bool:
    """Proper fraction: 0 < f < 1"""
    return 0 < f < 1

def is_mixed_fraction(f: Fraction) -> bool:
    """Mixed fraction: f > 1 and not integer"""
    return f > 1 and f.denominator != 1

def classify_number(n) -> list[str]:
    """
    Classify a number into all applicable NumberTypes.
    Useful for debugging and validation.

    Returns: list of applicable labels, e.g.: ["natural", "whole", "integer_pos", "prime"]
    """
    labels = []
    if isinstance(n, int):
        if n > 0:
            labels += ["natural", "whole", "integer", "integer_pos"]
            if is_prime(n):    labels.append("prime")
            if is_composite(n): labels.append("composite")
        elif n == 0:
            labels += ["whole", "integer"]
        else:
            labels += ["integer", "integer_neg"]
    elif isinstance(n, Fraction):
        if is_proper_fraction(n):  labels.append("fraction")
        if is_mixed_fraction(n):   labels.append("mixed_fraction")
    elif isinstance(n, float):
        labels.append("decimal")
    labels.append("real")  # All numbers are real
    return labels
```

---

## 7. Arithmetic Level System

### 7.1 LevelConfig Dataclass

File: `app/core/levels/config.py`

```python
from dataclasses import dataclass, field
from ..number_types.registry import NumberType

@dataclass(frozen=True)
class LevelConfig:
    """
    Configuration bundle for one level.
    Immutable (frozen=True) — cannot be changed at runtime.
    """
    level: int

    # ── Integer range ───────────────────────────────────────────────
    min_value: int            # Minimum integer operand value
    max_value: int            # Maximum integer operand value

    # ── Decimal configuration ─────────────────────────────────────────
    min_decimal: float        # Minimum value for decimal numbers
    max_decimal: float        # Maximum value for decimal numbers
    decimal_places: int       # Number of digits after decimal point

    # ── Fraction configuration ─────────────────────────────────────────
    allowed_denominators: list[int]  # Allowed denominators
    max_mixed_whole: int      # Maximum whole part for mixed fractions

    # ── Mixed operations configuration ────────────────────────────────
    max_operations: int       # Max operations in mixed problem
    allow_parentheses: bool   # Whether parentheses are allowed

    # ── Root & power configuration ──────────────────────────────────
    max_exponent: int         # Maximum exponent (e.g., x² → max_exponent=2)
    allowed_roots: list[int]  # Allowed root types (e.g., [2, 3] = √ and ∛)

    # ── NumberTypes valid for this level ───────────────────────────────
    allowed_number_types: list[NumberType]

    # ── Sub-types for NumberType.REAL ─────────────────────────────
    real_sub_types: list[NumberType] = field(default_factory=list)
```

### 7.2 Level Registry (Levels 1–7)

```python
# app/core/levels/config.py (continued)

LEVEL_REGISTRY: dict[int, LevelConfig] = {

    1: LevelConfig(
        level=1,
        # Small integers only
        min_value=1,            max_value=10,
        # Decimals not used at this level
        min_decimal=0.0,        max_decimal=0.0,    decimal_places=0,
        # Fractions not used
        allowed_denominators=[],                    max_mixed_whole=0,
        # Single operation, no parentheses
        max_operations=1,       allow_parentheses=False,
        # Minimal power & root
        max_exponent=1,         allowed_roots=[],
        allowed_number_types=[NumberType.NATURAL, NumberType.WHOLE],
        real_sub_types=[]
    ),

    2: LevelConfig(
        level=2,
        min_value=1,            max_value=50,
        min_decimal=0.0,        max_decimal=0.0,    decimal_places=0,
        allowed_denominators=[],                    max_mixed_whole=0,
        max_operations=1,       allow_parentheses=False,
        max_exponent=2,         allowed_roots=[2],  # Square root only
        allowed_number_types=[NumberType.NATURAL, NumberType.WHOLE, NumberType.PRIME],
        real_sub_types=[]
    ),

    3: LevelConfig(
        level=3,
        min_value=1,            max_value=100,
        min_decimal=0.1,        max_decimal=9.9,    decimal_places=1,
        allowed_denominators=[2, 4, 5, 10],         max_mixed_whole=5,
        max_operations=2,       allow_parentheses=False,
        max_exponent=2,         allowed_roots=[2],
        allowed_number_types=[
            NumberType.NATURAL, NumberType.WHOLE,
            NumberType.DECIMAL, NumberType.FRACTION,
        ],
        real_sub_types=[NumberType.NATURAL, NumberType.DECIMAL]
    ),

    4: LevelConfig(
        level=4,
        min_value=1,            max_value=500,
        min_decimal=0.01,       max_decimal=99.99,  decimal_places=2,
        allowed_denominators=[2, 3, 4, 5, 6, 8, 10], max_mixed_whole=10,
        max_operations=2,       allow_parentheses=True,
        max_exponent=3,         allowed_roots=[2, 3],
        allowed_number_types=[
            NumberType.NATURAL, NumberType.INTEGER, NumberType.INTEGER_NEG,
            NumberType.DECIMAL, NumberType.FRACTION, NumberType.MIXED_FRACTION,
            NumberType.PRIME, NumberType.COMPOSITE,
        ],
        real_sub_types=[NumberType.NATURAL, NumberType.DECIMAL, NumberType.FRACTION]
    ),

    5: LevelConfig(
        level=5,
        min_value=1,            max_value=1000,
        min_decimal=0.001,      max_decimal=999.999, decimal_places=3,
        allowed_denominators=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12], max_mixed_whole=20,
        max_operations=3,       allow_parentheses=True,
        max_exponent=4,         allowed_roots=[2, 3, 4],
        allowed_number_types=[
            NumberType.INTEGER, NumberType.INTEGER_NEG,
            NumberType.DECIMAL, NumberType.FRACTION, NumberType.MIXED_FRACTION,
            NumberType.PRIME, NumberType.COMPOSITE, NumberType.REAL,
        ],
        real_sub_types=[
            NumberType.INTEGER, NumberType.DECIMAL,
            NumberType.FRACTION, NumberType.MIXED_FRACTION,
        ]
    ),

    6: LevelConfig(
        level=6,
        min_value=1,            max_value=10_000,
        min_decimal=0.0001,     max_decimal=9999.9999, decimal_places=4,
        allowed_denominators=list(range(2, 21)),       max_mixed_whole=50,
        max_operations=4,       allow_parentheses=True,
        max_exponent=5,         allowed_roots=[2, 3, 4, 5],
        allowed_number_types=[NumberType.REAL, NumberType.INTEGER_NEG],
        real_sub_types=[
            NumberType.INTEGER, NumberType.INTEGER_NEG, NumberType.DECIMAL,
            NumberType.FRACTION, NumberType.MIXED_FRACTION,
        ]
    ),

    7: LevelConfig(
        level=7,
        min_value=1,            max_value=100_000,
        min_decimal=0.00001,    max_decimal=99999.99999, decimal_places=5,
        allowed_denominators=list(range(2, 51)),           max_mixed_whole=100,
        max_operations=5,       allow_parentheses=True,
        max_exponent=6,         allowed_roots=[2, 3, 4, 5, 6],
        allowed_number_types=[NumberType.REAL, NumberType.INTEGER_NEG],
        real_sub_types=[
            NumberType.INTEGER, NumberType.INTEGER_NEG, NumberType.DECIMAL,
            NumberType.FRACTION, NumberType.MIXED_FRACTION,
            NumberType.PRIME, NumberType.COMPOSITE,
        ]
    ),
}


def get_level_config(level: int) -> LevelConfig:
    """Get LevelConfig from registry. Raise error if level not available."""
    if level not in LEVEL_REGISTRY:
        raise ValueError(
            f"Level {level} not available. Valid levels: {sorted(LEVEL_REGISTRY.keys())}"
        )
    return LEVEL_REGISTRY[level]
```

### 7.3 Level × Operation Matrix

This table defines which operations are available at each level:

| Operation | L1 | L2 | L3 | L4 | L5 | L6 | L7 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Addition | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Subtraction | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Multiplication | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Division | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Exponentiation | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Square Root | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| N-th Root | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Modulo | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GCD / LCM | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Mixed Operations | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Mixed + Parentheses | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Negative Numbers | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Mixed Fractions | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |

---

## 8. Core Arithmetic — Module Specifications

> **Global Rule:** All functions in `core/arithmetic/` are **pure functions**. They receive `rng: random.Random` and `level_config: LevelConfig` as parameters — never call `random` directly.

### 8.1 `addition.py` — Addition

```python
from fractions import Fraction
from ..number_types.registry import NumberType
from ..number_types.generators import generate_number
from ..levels.config import LevelConfig
import random

def generate_addition(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    operand_count: int = 2
) -> dict:
    """
    Generate addition problem.

    Args:
        rng:           Seeded RNG
        level_config:  Active level configuration
        number_type:   Operand number type
        operand_count: Number of operands (default 2, max 5)

    Returns:
        {
            "operands": ["3/4", "1/4"],
            "operation": "addition",
            "expression": "3/4 + 1/4",
            "result": "1",
            "result_type": "whole",
            "steps": ["3/4 + 1/4 = 4/4 = 1"]
        }

    Constraint:
        - Result always "clean" (no repeating decimals)
        - For fractions: result denominator ≤ allowed_denominators
        - operand_count limited by level_config.max_operations + 1
    """
    ...

def _ensure_clean_result_fraction(operands: list[Fraction]) -> list[Fraction] | None:
    """
    Validate that fraction addition produces a simple fraction.
    Return None if invalid (trigger re-generate).
    """
    ...
```

**"Clean Result" Rules per NumberType:**

| NumberType | Clean Result Requirement |
|---|---|
| `natural` / `whole` | Result is non-negative integer |
| `integer` | Result is integer (can be negative) |
| `fraction` | Result already simplified, denominator ≤ 60 |
| `mixed_fraction` | Fraction part already simplified |
| `decimal` | Decimal digits ≤ `level_config.decimal_places` |

---

### 8.2 `subtraction.py` — Subtraction

```python
def generate_subtraction(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    allow_negative_result: bool | None = None
) -> dict:
    """
    Generate subtraction problem.

    Args:
        allow_negative_result: If None, follows level_config automatically.
                               If level < 4, result always ≥ 0.

    Returns:
        {
            "operands": ["15", "7"],
            "operation": "subtraction",
            "expression": "15 - 7",
            "result": "8",
            "result_type": "natural",
            "steps": ["15 - 7 = 8"]
        }

    Constraint:
        - For levels 1-3: operand_1 always ≥ operand_2 (result not negative)
        - For levels 4+: negative allowed if number_type supports
    """
    ...
```

---

### 8.3 `multiplication.py` — Multiplication

```python
def generate_multiplication(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    operand_count: int = 2
) -> dict:
    """
    Generate multiplication problem.

    Returns:
        {
            "operands": ["1/2", "3/4"],
            "operation": "multiplication",
            "expression": "1/2 × 3/4",
            "result": "3/8",
            "result_type": "fraction",
            "steps": ["1/2 × 3/4 = (1×3)/(2×4) = 3/8"]
        }

    Constraint (fractions specifically):
        - Result must not exceed level_config.max_value (for reasonable problems)
        - For two fractions: result auto-simplified
    """
    ...
```

---

### 8.4 `division.py` — Division

```python
def generate_division(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    result_type: NumberType | None = None
) -> dict:
    """
    Generate division problem with always-clean results.

    Strategy:
        To ensure clean results, generate result (quotient) first,
        then backward-compute dividend from divisor × quotient.

    Args:
        result_type: Desired number type for result.
                     If None, follows number_type.

    Returns:
        {
            "operands": ["12", "4"],
            "operation": "division",
            "expression": "12 ÷ 4",
            "result": "3",
            "result_type": "natural",
            "steps": ["12 ÷ 4 = 3"]
        }

    Constraint:
        - Divisor never 0
        - For levels 1-3: result always positive integer (no remainders)
        - For levels 4+: result can be fraction if number_type = fraction
    """
    ...

def _generate_clean_division_pair(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType
) -> tuple:
    """
    Backward strategy: pick quotient first → multiply by divisor → get dividend.
    Ensures always-clean results.
    """
    ...
```

---

### 8.5 `power.py` — Exponentiation

```python
def generate_power(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    exponent: int | None = None
) -> dict:
    """
    Generate exponentiation problem: base^exponent.

    Args:
        exponent: If None, randomly chosen from range [2, level_config.max_exponent]

    Returns:
        {
            "base": "3",
            "exponent": "2",
            "operation": "power",
            "expression": "3²",
            "expression_latex": "3^{2}",
            "result": "9",
            "result_type": "natural",
            "steps": ["3² = 3 × 3 = 9"]
        }

    Constraint:
        - Result must not exceed level_config.max_value × 100
        - For fractions: (a/b)^n — numerator and denominator computed separately
        - Exponent 0 only appears in level 5+ (concept x⁰ = 1 needs understanding)
        - Negative exponents only in level 6+
    """
    ...
```

---

### 8.6 `root.py` — Root Extraction

```python
def generate_root(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    root_degree: int | None = None
) -> dict:
    """
    Generate root extraction problem: ⁿ√radicand.

    Strategy:
        Backward approach — pick result (clean integer) first,
        then compute radicand = result^degree.

    Args:
        root_degree: Root degree (2=square, 3=cube, etc.).
                     If None, chosen from level_config.allowed_roots.

    Returns:
        {
            "radicand": "144",
            "root_degree": 2,
            "operation": "root",
            "expression": "√144",
            "expression_latex": "\\sqrt{144}",
            "result": "12",
            "result_type": "natural",
            "steps": ["√144 = √(12²) = 12"]
        }

    Constraint:
        - Result ALWAYS clean integer (backward generation guarantees this)
        - root_degree 2 = square root, 3 = cube root, etc.
        - Cube root only appears in level 4+ (per LevelConfig.allowed_roots)
    """
    ...

def _generate_perfect_root(
    rng: random.Random,
    level_config: LevelConfig,
    degree: int
) -> tuple[int, int]:
    """
    Returns (radicand, result) where radicand = result^degree.
    Result chosen from [2, int(level_config.max_value**(1/degree))].
    """
    ...
```

---

### 8.7 `modulo.py` — Modulo / Remainder Operation

```python
def generate_modulo(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType
) -> dict:
    """
    Generate remainder problem: dividend % divisor.

    Returns:
        {
            "operands": ["17", "5"],
            "operation": "modulo",
            "expression": "17 mod 5",
            "result": "2",
            "result_type": "whole",
            "steps": ["17 ÷ 5 = 3 remainder 2", "Thus 17 mod 5 = 2"]
        }

    Constraint:
        - Only for integer NumberTypes (natural, whole, integer)
        - Divisor always ≥ 2
        - Remainder always < divisor (modulo property)
        - Appears starting Level 3
    """
    ...
```

---

### 8.8 `number_properties.py` — GCD, LCM, Factors, Multiples

```python
from sympy import gcd, lcm, factorint

def generate_gcd_problem(
    rng: random.Random,
    level_config: LevelConfig
) -> dict:
    """
    Generate GCD (Greatest Common Divisor) problem.

    Strategy:
        Pick GCD target first, then create two numbers that are
        both multiples of the GCD target.

    Returns:
        {
            "operands": ["12", "18"],
            "operation": "gcd",
            "expression": "GCD(12, 18)",
            "result": "6",
            "steps": [
                "Factors of 12: 1, 2, 3, 4, 6, 12",
                "Factors of 18: 1, 2, 3, 6, 9, 18",
                "Common factors: 1, 2, 3, 6",
                "GCD = 6"
            ]
        }
    """
    ...

def generate_lcm_problem(rng, level_config) -> dict:
    """Generate LCM (Least Common Multiple) problem."""
    ...

def generate_factor_problem(rng, level_config) -> dict:
    """Generate prime factorization problem."""
    ...

def generate_multiple_problem(rng, level_config) -> dict:
    """Generate number multiples problem."""
    ...
```

---

### 8.9 `mixed_operations.py` — Mixed Operations

```python
from dataclasses import dataclass
from typing import Literal

OperationName = Literal["addition", "subtraction", "multiplication", "division",
                        "power", "root", "modulo"]

@dataclass
class MixedStep:
    step_id: str            # "s1", "s2", etc.
    operation: OperationName
    inputs: list[str]       # Variable IDs or previous step IDs
    result: str             # Result of this step
    expression: str         # String representation of this step

def generate_mixed_operations(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    operation_count: int | None = None,
    with_parentheses: bool | None = None
) -> dict:
    """
    Generate multi-step mixed operations problem.

    Args:
        operation_count: Number of operations. If None, chosen from
                         range [2, level_config.max_operations]
        with_parentheses: If None, follows level_config.allow_parentheses.

    Returns:
        {
            "variables": [
                {"id": "v1", "value": "12"},
                {"id": "v2", "value": "4"},
                {"id": "v3", "value": "3"}
            ],
            "operation": "mixed",
            "expression": "(12 + 4) × 3",
            "expression_latex": "(12 + 4) \\times 3",
            "steps": [
                {"step_id": "s1", "operation": "addition", "inputs": ["v1","v2"],
                 "expression": "12 + 4", "result": "16"},
                {"step_id": "s2", "operation": "multiplication", "inputs": ["s1","v3"],
                 "expression": "16 × 3", "result": "48"}
            ],
            "result": "48",
            "result_type": "natural"
        }

    Generation Strategy:
        1. Randomly pick operation sequence valid for this level
        2. Generate intermediate results first to ensure clean final result
        3. Backward-compute all operands
        4. Validate no division by zero or negative radicands
    """
    ...

def _build_expression_tree(steps: list[MixedStep], with_parentheses: bool) -> str:
    """
    Build expression string from step list, with or without parentheses.
    Respects BODMAS/PEMDAS for correct parenthesis placement.
    """
    ...
```

**Mixed Operations Validation Rules:**

```
1. No division by zero in any step
2. No square root of negative numbers
3. Intermediate results must not exceed level_config.max_value × 1000
4. Final expression must be deterministic (same operation sequence → same result)
5. Parentheses placed according to correct BODMAS rules
```

---

### 8.10 `comparison.py` — Comparison & Number Ordering

```python
def generate_comparison(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType
) -> dict:
    """
    Generate comparison problem for two numbers (>, <, =).

    Returns:
        {
            "operands": ["3/4", "2/3"],
            "operation": "comparison",
            "expression": "3/4 ___ 2/3",
            "result": ">",
            "steps": [
                "Equalize denominators: 3/4 = 9/12, 2/3 = 8/12",
                "9/12 > 8/12",
                "Thus 3/4 > 2/3"
            ]
        }
    """
    ...

def generate_ordering(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    count: int = 4,
    order: Literal["ascending", "descending"] = "ascending"
) -> dict:
    """
    Generate number ordering problem.

    Returns:
        {
            "numbers": ["3/4", "1/2", "2/3", "1/4"],
            "operation": "ordering",
            "order_type": "ascending",
            "result": ["1/4", "1/2", "2/3", "3/4"],
            "steps": [...]
        }
    """
    ...
```

---

## 9. Angles & Geometry Helpers

### 9.1 `angles.py` — Angle Generation (Geometry Core)

File: `app/core/geometry/angles.py`

```python
import random
import math

def generate_complementary_angle(rng: random.Random):
    """Complementary angles (x + y = 90°)"""
    angle_a = rng.randint(10, 80)
    angle_b = 90 - angle_a
    return {
        "type": "complementary",
        "angle_a": angle_a,
        "angle_b": angle_b,
        "sum": 90
    }

def generate_supplementary_angle(rng: random.Random):
    """Supplementary angles (x + y = 180°)"""
    angle_a = rng.randint(20, 160)
    angle_b = 180 - angle_a
    return {
        "type": "supplementary",
        "angle_a": angle_a,
        "angle_b": angle_b,
        "sum": 180
    }

def generate_parallel_line_angles(rng: random.Random):
    """Angle relationships in parallel lines cut by transversal"""
    base_angle = rng.randint(30, 150)
    other_angle = 180 - base_angle
    
    # Relationships:
    # 1. Corresponding (Sehadap) -> equal
    # 2. Alternate Interior (Dalam Berseberangan) -> equal
    # 3. Alternate Exterior (Luar Berseberangan) -> equal
    # 4. Consecutive Interior (Dalam Sepihak) -> sum 180
    
    relationships = ["sehadap", "dalam_berseberangan", "luar_berseberangan", "dalam_sepihak"]
    rel = rng.choice(relationships)
    
    return {
        "type": "parallel_lines",
        "relationship": rel,
        "angle_1": base_angle,
        "angle_2": base_angle if rel != "dalam_sepihak" else other_angle,
        "is_equal": rel != "dalam_sepihak"
    }
```

### 9.2 `lines.py` — Line Drawing Helpers

File: `app/core/geometry/lines.py`

```python
import math

def get_line_coords(x1, y1, angle_deg, length):
    """Get end coordinates based on angle and length."""
    angle_rad = math.radians(angle_deg)
    x2 = x1 + length * math.cos(angle_rad)
    y2 = y1 + length * math.sin(angle_rad)
    return [round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]

def generate_complementary_drawing(angle_a_deg):
    """Visual data for complementary angles (L-shape)"""
    origin = [0, 0]
    p_a = [50, 0]  # Horizontal line (OA)
    p_b = [0, 50]  # Vertical line (OB)
    _, p_c = get_line_coords(0, 0, angle_a_deg, 50)
    
    return {
        "points": {"O": origin, "A": p_a, "B": p_b, "C": p_c},
        "lines": [["O", "A"], ["O", "B"], ["O", "C"]],
        "angles": [
            {"label": "x", "points": ["A", "O", "C"], "value": angle_a_deg},
            {"label": "y", "points": ["C", "O", "B"], "value": 90 - angle_a_deg}
        ]
    }

def generate_supplementary_drawing(angle_a_deg):
    """Visual data for supplementary angles (Straight line)"""
    origin = [0, 0]
    p_a = [50, 0]   # Right
    p_b = [-50, 0]  # Left
    _, p_c = get_line_coords(0, 0, angle_a_deg, 50)
    
    return {
        "points": {"O": origin, "A": p_a, "B": p_b, "C": p_c},
        "lines": [["O", "A"], ["O", "B"], ["O", "C"]],
        "angles": [
            {"label": "x", "points": ["A", "O", "C"], "value": angle_a_deg},
            {"label": "y", "points": ["C", "O", "B"], "value": 180 - angle_a_deg}
        ]
    }
```

---

## 10. Seed-Based Generation System

### 10.1 Seed Philosophy

Seed enables **reproducibility** — same problems generated anytime with the same seed, without storing problems to database.

```
Input: seed=1234, operation="addition", level=3, number_type="fraction"
Output: Always produces identical expression
```

→ Useful for: retry problems, sharing problems with other students, auditing, debugging

### 10.2 SeedManager

File: `app/core/seed/manager.py`

```python
import random
import hashlib
from dataclasses import dataclass

@dataclass(frozen=True)
class SeedContext:
    """Complete context that forms unique seed per problem."""
    seed: int
    operation: str
    level: int
    number_type: str

class SeedManager:
    """
    Wrapper over random.Random for seed-based generation.
    Each instance is independent — no shared state.
    """

    def __init__(self, context: SeedContext):
        self._context = context
        self._rng = random.Random()
        self._rng.seed(self._make_deterministic_seed(context))

    @property
    def rng(self) -> random.Random:
        """Seeded RNG instance. Use this for all random operations."""
        return self._rng

    @staticmethod
    def _make_deterministic_seed(ctx: SeedContext) -> int:
        """
        Combine all parameters into one deterministic seed integer.

        Uses SHA-256 for even distribution and collision-free.
        Format string: "seed:op:level:numtype"
        """
        raw = f"{ctx.seed}:{ctx.operation}:{ctx.level}:{ctx.number_type}"
        hash_bytes = hashlib.sha256(raw.encode()).digest()
        return int.from_bytes(hash_bytes[:8], byteorder="big")

    def get_context(self) -> SeedContext:
        return self._context
```

### 10.3 Seed Integration in Generators

Every generator function **must** accept `rng: random.Random` as parameter, not call it globally:

```python
# ✅ CORRECT — Deterministic because rng is controlled from outside
def generate_addition(rng: random.Random, level_config: LevelConfig, ...) -> dict:
    a = generate_number(number_type, level_config, rng)  # rng passed down
    b = generate_number(number_type, level_config, rng)
    ...

# ❌ WRONG — Calls random directly, not reproducible
def generate_addition(level_config: LevelConfig, ...) -> dict:
    a = random.randint(1, 100)   # ← not deterministic!
    ...
```

### 10.4 Seed Flow in Service Layer

```python
# app/services/arithmetic_service.py

from app.core.seed.manager import SeedManager, SeedContext
from app.core.levels.config import get_level_config
from app.core.arithmetic.addition import generate_addition

def generate_arithmetic_question(
    seed: int,
    operation: str,
    level: int,
    number_type: str,
    ...
) -> dict:

    # 1. Create SeedContext — unique combination of all parameters
    ctx = SeedContext(seed=seed, operation=operation, level=level, number_type=number_type)

    # 2. Initialize SeedManager — RNG seeded here
    seed_manager = SeedManager(ctx)

    # 3. Get LevelConfig
    level_config = get_level_config(level)

    # 4. Run generator with rng from seed_manager
    raw_data = generate_addition(
        rng=seed_manager.rng,
        level_config=level_config,
        number_type=NumberType(number_type)
    )

    # 5. Build blueprint & distractor
    ...
```

### 10.5 Reproducibility Guarantee

Reproducibility is guaranteed by two things:

1. **Deterministic seed** — SHA-256 of (seed + operation + level + number_type) → consistent integer
2. **Fixed rng call order** — every generator must call `rng` in the same order every time it's executed (no conditionals that change rng call count based on intermediate values)

```python
# ✅ CORRECT — rng call order always same
a = rng.randint(1, 10)   # call #1
b = rng.randint(1, 10)   # call #2
result = a + b

# ❌ WRONG — rng call count changes based on value
a = rng.randint(1, 10)
if a > 5:
    b = rng.randint(1, 20)   # call #2 ONLY if a > 5 → not deterministic
```

---

## 11. Layer Service & Blueprint

### 11.1 `services/arithmetic_service.py`

Main coordinator that combines all layers:

```python
async def generate_arithmetic_question(request: ArithmeticRequest) -> ArithmeticResponse:
    """
    Complete arithmetic problem generation flow:
    
    1. Resolve SeedContext & SeedManager
    2. Resolve LevelConfig
    3. Validate NumberType vs Level (is this type available at this level?)
    4. Call core generator according to operation
    5. Build blueprint via blueprint.py
    6. Build distractors via distractor.py
    7. (Optional) Call AI storyteller
    8. Return ArithmeticResponse
    """
    ...

def _validate_number_type_for_level(number_type: NumberType, level_config: LevelConfig):
    """Validate if number_type is available at requested level."""
    if number_type not in level_config.allowed_number_types:
        raise InvalidNumberTypeForLevelError(
            f"NumberType '{number_type}' not available at Level {level_config.level}. "
            f"Available: {[t.value for t in level_config.allowed_number_types]}"
        )
```

### 11.2 `services/blueprint.py`

```python
def build_arithmetic_blueprint(raw_data: dict, operation: str) -> list[dict]:
    """
    Transform raw_data from core into drag-and-drop blueprint.

    Blueprint Step Format:
    {
        "step": 1,
        "op": "addition",
        "op_symbol": "+",
        "inputs": ["v1", "v2"],
        "correct_result": "3/4",
        "result_type": "fraction",
        "hint": "Equalize denominators first"
    }
    """
    ...
```

### 11.3 `services/distractor.py`

```python
MISCONCEPTION_RULES: dict[str, list[callable]] = {
    "addition_fraction": [
        _add_numerators_and_denominators,   # 1/2 + 1/3 → 2/5
        _forget_simplify,                    # result not simplified
        _use_wrong_lcd,                      # Wrong LCD calculation
    ],
    "subtraction_integer_neg": [
        _ignore_negative_sign,               # -5 - 3 → 2 (should be -8)
        _flip_sign,                          # -5 - 3 → 8
    ],
    "division_fraction": [
        _forget_reciprocal,                  # forgot to flip second fraction
        _divide_numerators_separately,       # dividing numerator & denominator separately
    ],
    "power_fraction": [
        _only_power_numerator,               # (1/2)² → 1/2 (should be 1/4)
    ],
    "root": [
        _halve_radicand,                     # √144 → 72 (divide by 2 not root)
        _subtract_degree_from_radicand,      # √144 → 142
    ],
    # ... and so on
}

def generate_distractors(
    correct_answer: str,
    operation: str,
    number_type: str,
    count: int = 3,
    rng: random.Random | None = None   # Optional: can also be seed-based
) -> list[str]:
    """
    Generate `count` misconception-based distractors.
    All distractors guaranteed different from correct_answer and each other.
    """
    ...
```

### 11.4 `services/angle_service.py` — Angle Question Service (NEW)

```python
from app.core.seed.manager import SeedManager, SeedContext
from app.core.geometry.angles import (
    generate_complementary_angle,
    generate_supplementary_angle,
    generate_parallel_line_angles
)
from app.core.geometry.lines import (
    generate_complementary_drawing,
    generate_supplementary_drawing
)
from app.services.ai_storyteller import ai_storyteller

async def generate_angle_question(
    seed: int,
    level: int,
    angle_type: str | None = None,
    with_story: bool = False
):
    """
    Generate angle problem (complementary, supplementary, parallel_lines).
    
    Types:
    - complementary: x + y = 90° (Level 1+)
    - supplementary: x + y = 180° (Level 1+)
    - parallel_lines: Parallel lines + transversal (Level 4+)
    """
    ctx = SeedContext(seed=seed, operation="angles", level=level, number_type="natural")
    rng = SeedManager(ctx).rng
    
    types = ["complementary", "supplementary"]
    if level >= 4:
        types.append("parallel_lines")
    target_type = angle_type or rng.choice(types)
    
    drawing_data = None
    if target_type == "complementary":
        res = generate_complementary_angle(rng)
        drawing_data = generate_complementary_drawing(res["angle_a"])
        expression = f"If angle x is {res['angle_a']} degrees, determine its complement (y)."
        correct_answer = str(res["angle_b"])
    elif target_type == "supplementary":
        res = generate_supplementary_angle(rng)
        drawing_data = generate_supplementary_drawing(res["angle_a"])
        expression = f"If angle x is {res['angle_a']} degrees, determine its supplement (y)."
        correct_answer = str(res["angle_b"])
    else:  # Parallel lines
        res = generate_parallel_line_angles(rng)
        expression = f"On two parallel lines cut by another line, determine angle {res['relationship'].replace('_', ' ')} if the first angle is {res['angle_1']} degrees."
        correct_answer = str(res["angle_2"])
        drawing_data = {"type": "parallel_lines_schema", "relationship": res["relationship"]}
    
    story = None
    if with_story:
        story = await ai_storyteller.generate_story(expression, correct_answer, "angles", "construction", rng)
    
    return {
        "meta": {"seed": seed, "level": level, "type": target_type},
        "data": {
            "expression": expression,
            "story": story,
            "correct_answer": correct_answer,
            "drawing_data": drawing_data
        }
    }
```

### 11.5 `services/exam_service.py` — Exam Pack Generation (NEW)

Exam module generates a collection of problems from various domains with a single master seed.

#### Seed Derivation for Exam

```python
def derive_sub_seed(master_seed: int, index: int, domain: str) -> int:
    """Generate unique yet deterministic sub-seed."""
    seed_str = f"{master_seed}:{index}:{domain}"
    return int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (10**9)
```

#### Exam Pack Generator

```python
async def generate_exam_pack(master_seed: int, requirements: list[dict]) -> dict:
    """
    Generate exam pack from multiple domains.
    
    Request format:
    {
        "master_seed": 2024,
        "requirements": [
            {"domain": "arithmetic", "operation": "addition", "level": 1, "number_type": "natural"},
            {"domain": "geometry", "shape": "cube", "level": 2},
            {"domain": "angles", "type": "complementary", "level": 3}
        ]
    }
    
    Response format:
    {
        "master_seed": 2024,
        "total_questions": 3,
        "questions": [
            {"id": 1, "domain": "arithmetic", "content": {ArithmeticResponse}},
            {"id": 2, "domain": "geometry", "content": {GeometryResponse}},
            {"id": 3, "domain": "angles", "content": {AngleResponse}}
        ]
    }
    """
    questions = []
    
    for i, req in enumerate(requirements):
        domain = req.get("domain", "arithmetic")
        level = req.get("level", 1)
        sub_seed = derive_sub_seed(master_seed, i, domain)
        
        if domain == "arithmetic":
            ar_req = ArithmeticRequest(
                seed=sub_seed,
                level=level,
                operation=req.get("operation", "addition"),
                number_type=NumberType(req.get("number_type", "natural")),
                with_story=req.get("with_story", False)
            )
            q = await generate_arithmetic_question(ar_req)
            questions.append({"id": i+1, "domain": domain, "content": q.model_dump()})
        elif domain == "geometry":
            q = await generate_geometry_question(
                seed=sub_seed, level=level,
                shape_type=req.get("shape"),
                with_story=req.get("with_story", False),
                dimension=req.get("dimension", "3D")
            )
            questions.append({"id": i+1, "domain": domain, "content": q})
        elif domain == "angles":
            q = await generate_angle_question(
                sub_seed, level,
                req.get("type"),
                req.get("with_story", False)
            )
            questions.append({"id": i+1, "domain": domain, "content": q})
        # ... other domains (measurement, algebra, statistics)
    
    return {
        "master_seed": master_seed,
        "total_questions": len(questions),
        "questions": questions
    }
```

**Supported Domains:** `arithmetic`, `geometry`, `measurement`, `algebra`, `statistics`, `angles`

**Sub-Seed Logic:** Each problem in the pack gets a sub-seed derived from master_seed + index + domain, guaranteeing pack reproducibility.

---

## 12. Schemas (JSON Contracts)

### 12.1 `schemas/request.py`

```python
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional
from app.core.number_types.registry import NumberType
from app.core.levels.config import LEVEL_REGISTRY

ArithmeticOperation = Literal[
    "addition", "subtraction", "multiplication", "division",
    "power", "root", "modulo", "gcd", "lcm", "mixed",
    "comparison", "ordering", "factorization"
]

class ArithmeticRequest(BaseModel):
    # ── Required Parameters ──────────────────────────────────────────────
    seed: int = Field(..., description="Seed for reproducible generation")
    level: int = Field(..., ge=1, le=7, description="Difficulty level (1–7)")
    operation: ArithmeticOperation = Field(..., description="Math operation type")
    number_type: NumberType = Field(..., description="Number type to use")

    # ── Optional Parameters ───────────────────────────────────────────
    operand_count: int = Field(default=2, ge=2, le=5,
                               description="Number of operands (for addition/multiplication)")
    with_story: bool = Field(default=True, description="Generate word problem via LM Studio")
    with_distractors: bool = Field(default=True, description="Include wrong answer choices")
    distractor_count: int = Field(default=3, ge=2, le=4)
    theme: str = Field(default="general", description="Word problem theme")

    # ── Cross-Field Validation ─────────────────────────────────────────
    @model_validator(mode="after")
    def validate_number_type_for_level(self):
        from app.core.levels.config import get_level_config
        cfg = get_level_config(self.level)
        if self.number_type not in cfg.allowed_number_types:
            raise ValueError(
                f"NumberType '{self.number_type}' not available at Level {self.level}. "
                f"Use: {[t.value for t in cfg.allowed_number_types]}"
            )
        return self
```

### 12.2 `schemas/response.py` — Complete Structure

#### Standard Arithmetic Response

```json
{
  "status": "success",
  "meta": {
    "seed": 1234,
    "level": 3,
    "operation": "addition",
    "number_type": "fraction",
    "generated_at": "2025-01-15T10:30:00Z"
  },
  "context": {
    "story": "Budi has 3/4 kg of rice and Susi has 1/4 kg of rice. What is their total rice?",
    "theme": "shopping"
  },
  "data": {
    "variables": [
      {"id": "v1", "label": "Budi's rice", "value": "3/4", "unit": "kg", "type": "fraction"},
      {"id": "v2", "label": "Susi's rice", "value": "1/4", "unit": "kg", "type": "fraction"}
    ],
    "expression": "3/4 + 1/4",
    "expression_latex": "\\frac{3}{4} + \\frac{1}{4}",
    "blueprint": [
      {
        "step": 1,
        "op": "addition",
        "op_symbol": "+",
        "inputs": ["v1", "v2"],
        "correct_result": "1",
        "result_type": "whole",
        "hint": "Denominators already same, just add numerators"
      }
    ],
    "answer_choices": ["1", "4/8", "2/4", "1/2"],
    "correct_answer": "1",
    "answer_type": "whole"
  }
}
```

#### Angle Response (NEW)

```json
{
  "status": "success",
  "meta": {
    "seed": 5678,
    "level": 3,
    "type": "complementary"
  },
  "data": {
    "expression": "If angle x is 35 degrees, determine its complement (y).",
    "story": "In a right triangle, one acute angle measures 35°. What is the other acute angle?",
    "correct_answer": "55",
    "drawing_data": {
      "points": {"O": [0, 0], "A": [50, 0], "B": [0, 50], "C": [35.35, 24.72]},
      "lines": [["O", "A"], ["O", "B"], ["O", "C"]],
      "angles": [
        {"label": "x", "points": ["A", "O", "C"], "value": 35},
        {"label": "y", "points": ["C", "O", "B"], "value": 55}
      ]
    }
  }
}
```

#### Exam Pack Response (NEW)

```json
{
  "master_seed": 2024,
  "total_questions": 3,
  "questions": [
    {
      "id": 1,
      "domain": "arithmetic",
      "content": {ArithmeticResponse...}
    },
    {
      "id": 2,
      "domain": "angles",
      "content": {AngleResponse...}
    },
    {
      "id": 3,
      "domain": "geometry",
      "content": {GeometryResponse...}
    }
  ]
}
```

### 12.3 Angle & Exam Request Schemas (NEW)

```python
class AngleRequest(BaseModel):
    seed: int
    level: int
    type: Optional[str] = None  # complementary | supplementary | parallel_lines
    with_story: bool = False

class ExamRequest(BaseModel):
    master_seed: int
    requirements: list[dict]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "master_seed": 2024,
                "requirements": [
                    {"domain": "arithmetic", "operation": "addition", "level": 1, "number_type": "natural"},
                    {"domain": "angles", "type": "complementary", "level": 3}
                ]
            }
        }
    }
```

---

## 13. API Endpoint Specification

### Base URL: `/api/v1`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/levels` | List all levels with configurations |
| `GET` | `/levels/{level}` | Single level configuration details |
| `GET` | `/number-types` | List all supported number types |
| `GET` | `/operations` | List all supported operations |
| `GET` | `/operations/{level}` | Operations available for a level |
| `POST` | `/arithmetic/generate` | Generate arithmetic problem |
| `POST` | `/arithmetic/validate-params` | Validate parameters without generating problem |
| `POST` | `/geometry/generate` | Generate geometry problem |
| `POST` | `/measurement/generate` | Generate measurement problem |
| `POST` | `/algebra/generate` | Generate algebra problem |
| `POST` | `/statistics/generate` | Generate statistics problem |
| `POST` | `/angles/generate` | **NEW:** Generate angle problem (complementary, supplementary, parallel lines) |
| `POST` | `/exam/generate` | **NEW:** Generate exam pack from multiple domains |
| `POST` | `/probability/generate` | Generate probability problem |

### Example Request: Generate Problem

```bash
# Addition with fractions, level 3, seed 42
curl -X POST "http://localhost:8000/api/v1/arithmetic/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "seed": 42,
    "level": 3,
    "operation": "addition",
    "number_type": "fraction",
    "with_story": false,
    "with_distractors": true,
    "distractor_count": 3
  }'

# Mixed operations, level 5, integer numbers
curl -X POST "http://localhost:8000/api/v1/arithmetic/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "seed": 9999,
    "level": 5,
    "operation": "mixed",
    "number_type": "integer",
    "with_story": true,
    "theme": "cooking"
  }'

# Angle problem (NEW)
curl -X POST "http://localhost:8000/api/v1/angles/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "seed": 5678,
    "level": 3,
    "type": "complementary",
    "with_story": true
  }'

# Exam pack (NEW)
curl -X POST "http://localhost:8000/api/v1/exam/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "master_seed": 2024,
    "requirements": [
      {"domain": "arithmetic", "operation": "addition", "level": 1, "number_type": "natural"},
      {"domain": "angles", "type": "supplementary", "level": 3}
    ]
  }'
```

### Example Response: GET /levels

```json
{
  "levels": [
    {
      "level": 1,
      "label": "Level 1",
      "description": "Small whole numbers, single operation",
      "max_value": 10,
      "allowed_operations": ["addition", "subtraction"],
      "allowed_number_types": ["natural", "whole"]
    },
    {
      "level": 2,
      "label": "Level 2",
      "description": "Natural numbers up to 50, including primes",
      "max_value": 50,
      "allowed_operations": ["addition", "subtraction", "multiplication", "division", "power", "root"],
      "allowed_number_types": ["natural", "whole", "prime"]
    }
  ]
}
```

---

## 14. Code Standards & Conventions

### 14.1 Naming Convention

| Type | Convention | Example |
|---|---|---|
| File & Folder | `snake_case` | `mixed_operations.py` |
| Class | `PascalCase` | `SeedManager`, `LevelConfig` |
| Function & Variable | `snake_case` | `generate_addition()` |
| Constant | `UPPER_SNAKE_CASE` | `LEVEL_REGISTRY` |
| Enum Value | `UPPER_SNAKE_CASE` | `NumberType.MIXED_FRACTION` |
| Endpoint | `kebab-case` | `/number-types` |

### 14.2 Mandatory Rules for Core Functions

```python
# ✅ ALL core functions MUST:
# 1. Be pure functions (no side effects)
# 2. Accept rng as parameter
# 3. Use type hints
# 4. Have Google-style docstrings
# 5. Return dict with consistent keys

def generate_addition(
    rng: random.Random,           # ← REQUIRED: RNG from SeedManager
    level_config: LevelConfig,    # ← REQUIRED: level configuration
    number_type: NumberType,      # ← REQUIRED: number type
    operand_count: int = 2        # ← Optional with default
) -> dict:                        # ← Always return dict
    ...

# ❌ FORBIDDEN in core/:
# - import httpx, requests (I/O)
# - print(), logging.info() (side effects)
# - random.randint() directly (must go through rng parameter)
# - any global state
```

### 14.3 Dict Output Key Convention

All generator functions **must** return dict with following keys (if relevant):

```python
{
    "operands":         list[str],     # List of operand strings
    "operation":        str,           # Operation name
    "expression":       str,           # Text expression: "3/4 + 1/4"
    "expression_latex": str,           # LaTeX expression: "\\frac{3}{4} + \\frac{1}{4}"
    "result":           str,           # Result as string
    "result_type":      str,           # NumberType of result
    "steps":            list[str],     # Solution steps
}
```

---

## 15. Error Handling

### 15.1 Exception Hierarchy

```python
# app/exceptions.py

class MathEngineError(Exception):
    """Base exception."""
    pass

# ── Level & Config ───────────────────────────────────────────────────
class InvalidLevelError(MathEngineError):
    """Level not available."""
    pass

class InvalidNumberTypeForLevelError(MathEngineError):
    """NumberType not available for selected level."""
    pass

class InvalidOperationForLevelError(MathEngineError):
    """Operation not available for selected level."""
    pass

# ── Generation ───────────────────────────────────────────────────────
class GenerationFailedError(MathEngineError):
    """Failed to generate valid number after max_retries attempts."""
    pass

class DivisionByZeroError(MathEngineError):
    """Operation resulted in division by zero."""
    pass

class NegativeRadicandError(MathEngineError):
    """Attempted to take root of negative number."""
    pass

# ── External ─────────────────────────────────────────────────────────
class LMStudioConnectionError(MathEngineError):
    """Failed to connect to LM Studio."""
    pass
```

### 15.2 Retry Strategy for Generators

Some generators might fail to produce valid numbers on first attempt (e.g., no primes in too-small range). Use retry loop with limit:

```python
MAX_GENERATION_RETRIES = 50

def generate_with_retry(generator_fn, *args, **kwargs) -> dict:
    for attempt in range(MAX_GENERATION_RETRIES):
        try:
            result = generator_fn(*args, **kwargs)
            if _is_valid_result(result):
                return result
        except (ValueError, ZeroDivisionError):
            continue
    raise GenerationFailedError(
        f"Failed to generate valid problem after {MAX_GENERATION_RETRIES} attempts. "
        f"Try using different level or number_type."
    )
```

---

## 16. Testing Strategy

### 16.1 Test Structure

```
tests/
├── unit/
│   ├── core/
│   │   ├── test_seed_manager.py        # ★ Highest priority
│   │   ├── test_level_config.py
│   │   ├── test_number_type_generators.py
│   │   ├── test_addition.py
│   │   ├── test_subtraction.py
│   │   ├── test_multiplication.py
│   │   ├── test_division.py
│   │   ├── test_power.py
│   │   ├── test_root.py
│   │   ├── test_modulo.py
│   │   ├── test_mixed_operations.py
│   │   └── test_number_properties.py
│   └── services/
│       ├── test_blueprint.py
│       └── test_distractor.py
└── integration/
    ├── test_arithmetic_endpoint.py
    └── test_seed_reproducibility.py   # ★ Mandatory: verify seed works
```

### 16.2 Mandatory Test: Seed Reproducibility

```python
# tests/integration/test_seed_reproducibility.py

import pytest
from httpx import AsyncClient

class TestSeedReproducibility:

    @pytest.mark.asyncio
    async def test_same_seed_same_output(self, client: AsyncClient):
        """Two requests with same seed & params MUST produce identical output."""
        params = {
            "seed": 42,
            "level": 3,
            "operation": "addition",
            "number_type": "fraction",
            "with_story": False,
            "with_distractors": False
        }
        resp1 = await client.post("/api/v1/arithmetic/generate", json=params)
        resp2 = await client.post("/api/v1/arithmetic/generate", json=params)

        assert resp1.json()["data"]["expression"] == resp2.json()["data"]["expression"]
        assert resp1.json()["data"]["result"] == resp2.json()["data"]["result"]

    @pytest.mark.asyncio
    async def test_different_seed_different_output(self, client: AsyncClient):
        """Two requests with different seeds MUST produce different output."""
        base_params = {"level": 3, "operation": "addition",
                       "number_type": "fraction", "with_story": False}

        resp1 = await client.post("/api/v1/arithmetic/generate",
                                  json={**base_params, "seed": 1})
        resp2 = await client.post("/api/v1/arithmetic/generate",
                                  json={**base_params, "seed": 2})

        # Very small chance different seeds produce same problem
        assert resp1.json()["data"]["expression"] != resp2.json()["data"]["expression"]

    @pytest.mark.asyncio
    async def test_seed_across_all_operations(self, client: AsyncClient):
        """Reproducibility works for all operations."""
        operations = ["addition", "subtraction", "multiplication", "division",
                      "power", "root", "modulo"]
        for op in operations:
            params = {"seed": 1234, "level": 4, "operation": op,
                      "number_type": "natural", "with_story": False}
            r1 = await client.post("/api/v1/arithmetic/generate", json=params)
            r2 = await client.post("/api/v1/arithmetic/generate", json=params)
            assert r1.json()["data"]["result"] == r2.json()["data"]["result"], \
                f"Seed reproducibility failed for operation: {op}"
```

### 16.3 Mandatory Test: Clean Result

```python
# tests/unit/core/test_division.py

class TestDivisionCleanResult:

    def test_integer_division_always_exact(self):
        """Integer division must always produce integer (no remainder)."""
        rng = random.Random(42)
        cfg = get_level_config(2)
        for _ in range(100):   # Test 100 times
            result = generate_division(rng, cfg, NumberType.NATURAL)
            assert "." not in result["result"], \
                f"Division result not clean: {result['expression']} = {result['result']}"

    def test_fraction_result_is_simplified(self):
        """Fraction result from division must be simplified."""
        rng = random.Random(99)
        cfg = get_level_config(3)
        for _ in range(50):
            result = generate_division(rng, cfg, NumberType.FRACTION)
            f = Fraction(result["result"])
            # Fraction() auto-simplifies, so just compare string
            assert result["result"] == str(f), \
                f"Fraction not simplified: {result['result']}"
```

---

## 17. Environment & Configuration

### 17.1 File `.env.example`

```bash
# ── Server ───────────────────────────────────────────────────────────
APP_HOST=0.0.0.0
APP_PORT=8000
APP_ENV=development          # development | production

# ── LM Studio ────────────────────────────────────────────────────────
LM_STUDIO_URL=http://localhost:1234
LM_MODEL=local-model
LM_TIMEOUT_SECONDS=30

# ── Math Engine ───────────────────────────────────────────────────────
DEFAULT_LEVEL=3
DEFAULT_NUMBER_TYPE=natural
MAX_GENERATION_RETRIES=50    # Retry limit for generators
MAX_DISTRACTOR_COUNT=4
ENABLE_AI_STORY=true         # Set false to skip LM Studio (faster)

# ── Seed ─────────────────────────────────────────────────────────────
# No seed config — seed always sent per-request
```

### 17.2 `app/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_env: str = "development"

    lm_studio_url: str = "http://localhost:1234"
    lm_model: str = "local-model"
    lm_timeout_seconds: int = 30

    default_level: int = 3
    default_number_type: str = "natural"
    max_generation_retries: int = 50
    max_distractor_count: int = 4
    enable_ai_story: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 18. Work Plan (Roadmap)

### Phase 1 — Foundation & Infrastructure
**Target:** Boilerplate, seed system, level system, and number type system working.

- [x] Init project & directory structure per Section 5
- [x] Setup `requirements.txt` and virtual environment
- [x] Implement `app/config.py` and `app/exceptions.py`
- [x] Implement `core/number_types/registry.py` (NumberType Enum)
- [x] Implement `core/number_types/validators.py`
- [x] Implement `core/levels/config.py` (LevelConfig + LEVEL_REGISTRY level 1–7)
- [x] Implement `core/seed/manager.py` (SeedManager + SeedContext)
- [x] Implement `core/number_types/generators.py`
- [x] Unit test for seed manager (reproducibility test manual)
- [x] `GET /health` and `GET /levels` functional

**Phase 1 Verification:**
```python
# Manual reproducibility test
from app.core.seed.manager import SeedManager, SeedContext
from app.core.number_types.generators import generate_number
from app.core.number_types.registry import NumberType
from app.core.levels.config import get_level_config

ctx = SeedContext(seed=42, operation="addition", level=3, number_type="fraction")
sm1 = SeedManager(ctx)
sm2 = SeedManager(ctx)

cfg = get_level_config(3)
n1 = generate_number(NumberType.FRACTION, cfg, sm1.rng)
n2 = generate_number(NumberType.FRACTION, cfg, sm2.rng)
assert n1 == n2, "Seed not working!"
print(f"✅ Seed works: {n1}")
```

---

### Phase 2 — Core Arithmetic (Basic Operations)
**Target:** Addition, subtraction, multiplication, division ready for all NumberTypes.

- [x] `core/arithmetic/addition.py` — all NumberTypes, all levels
- [x] `core/arithmetic/subtraction.py`
- [x] `core/arithmetic/multiplication.py`
- [x] `core/arithmetic/division.py` (backward strategy)
- [x] `services/blueprint.py` (JSON blueprint format)
- [x] `services/distractor.py` (basic misconceptions)
- [x] `schemas/request.py` and `schemas/response.py`
- [x] `routers/arithmetic.py` — endpoint `/arithmetic/generate`
- [x] Unit test per operation (min. 50 cases, ensure clean results)
- [x] Integration test reproducibility for basic operations

---

### Phase 3 — Core Arithmetic (Advanced Operations)
**Target:** Power, root, modulo, number properties, mixed operations.

- [x] `core/arithmetic/power.py`
- [x] `core/arithmetic/root.py` (backward strategy)
- [x] `core/arithmetic/modulo.py`
- [x] `core/arithmetic/number_properties.py` (GCD, LCM, factors)
- [x] `core/arithmetic/comparison.py`
- [x] `core/arithmetic/mixed_operations.py` (BODMAS-aware)
- [x] Distractor rules for all new operations
- [x] Test coverage ≥ 80% for all arithmetic files

---

### Phase 4 — AI Storyteller Integration
**Target:** Word problems generated by LM Studio with robust fallback.

- [x] Implement `services/ai_storyteller.py`
- [x] Prompt template per domain & theme
- [x] Fallback story generator (without LM Studio)
- [x] Integration to arithmetic_service
- [x] Test: storyteller active and inactive

---

### Phase 5 — Other Domains & Finalization
**Target:** Geometry, measurement, algebra, statistics, angles, exam.

- [x] Implement all non-arithmetic domains (with seed & level system)
- [x] Implement angles module (complementary, supplementary, parallel_lines)
- [x] Implement exam module (multi-domain pack generation)
- [x] `GET /operations/{level}` endpoint
- [x] Finalize Swagger docs
- [x] Performance test: every endpoint < 500ms (without LM Studio)
- [x] Load test: 50 concurrent requests remain reproducible

---

## 19. Architecture Decision Records (ADR)

### ADR-001: Why Level Uses Integer, Not String?

**Decision:** Level uses integer (1, 2, 3...) not string ("easy", "medium", "hard").

**Reasons:**
- More granular — can add new levels without breaking change
- Easily mapped to grade levels (Level 1 ≈ Grade 1)
- Sorting and range queries easier (`level >= 3`)
- Can be configured dynamically by admin without changing code

---

### ADR-002: Why Seed is Hashed with SHA-256?

**Decision:** Final seed = `SHA-256(f"{seed}:{operation}:{level}:{number_type}")[:8 bytes]`

**Reasons:**
- Same seed with different parameters produces different RNG states
- Without hashing: `seed=1, level=1` and `seed=10, level=1` could be too close in value and produce similar numbers
- SHA-256 provides even distribution and practically collision-free

**Trade-off:** Slight computation overhead (~microseconds) — not significant.

---

### ADR-003: Why Backward Generation for Division & Root?

**Decision:** Division and root generators pick result (quotient/root) first, then compute operands backward.

**Reasons:**
- Forward generation (pick operands first) often produces "dirty" results (3 ÷ 7 = 0.428...)
- Backward generation **guarantees 100%** clean results without excessive retries
- More efficient: no retry loops needed

**Example:**
```
Backward Division:
  1. Pick quotient = 4 (random)
  2. Pick divisor = 3 (random)
  3. Compute dividend = 4 × 3 = 12
  4. Problem: 12 ÷ 3 = 4 ✅
```

---

### ADR-004: Why NumberType is Separate from Level?

**Decision:** NumberType is a separate parameter, not part of level.

**Reasons:**
- Flexibility: teacher can choose "multiplication Level 5 with fractions" explicitly
- Level controls **operation complexity**; NumberType controls **number type**
- Validation still exists: not all NumberTypes available at all levels (via `allowed_number_types`)

---

### ADR-005: Why `fractions.Fraction`, Not `float`?

**Decision:** All fraction operations use `fractions.Fraction` from Python stdlib.

**Reasons:**
```python
# Float problem
0.1 + 0.2 == 0.30000000000000004  # ← CANNOT use for problems!

# Fraction solution
Fraction('1/10') + Fraction('2/10') == Fraction(3, 10)  # ← Precise ✅
str(Fraction(3, 10))  # → "3/10"
```

**Trade-off:** Slightly slower than float — not significant for this use case.

---

### ADR-006: Why Results are Always Stored as Strings in JSON?

**Decision:** Fields `result`, `operands`, and `variables[].value` are always strings in JSON response.

**Reasons:**
- JSON has no `Fraction` type
- Using float `0.75` loses pedagogical info of fraction `3/4`
- String allows representation: integer `"12"`, fraction `"3/4"`, mixed `"1 3/4"`, decimal `"3.14"`
- Frontend can parse according to display needs

---

### ADR-007: Why We Added Angles & Exam Modules?

**Decision:** Add `angles` module for geometry angle problems and `exam` module for multi-domain pack generation.

**Reasons:**
- **Angles:** Supports complementary (90°), supplementary (180°), and parallel line angles — common CBT math problems
- **Exam:** Allows generating a complete exam with one master seed, deriving sub-seeds deterministically per domain
- Both modules follow the same seed-based, level-based architecture as arithmetic

---

*This document is a living document. Update whenever there is an architecture or design decision change.*

*Last updated: v2.1.0 — Added: Angles Module, Exam Module, Fixed Typos, Improved Structure*
