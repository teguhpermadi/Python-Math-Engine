# 📐 Technical Requirement Document: Python Math Engine for CBT

> **Versi:** 2.0.0 | **Status:** Draft | **Framework:** FastAPI (Python 3.11+)
> **Changelog v2:** Restruktur modul arithmetic, sistem level berbasis angka, seed-based generation, tipe bilangan lengkap

---

## Daftar Isi

1. [Ringkasan Proyek](#1-ringkasan-proyek)
2. [Konsep Inti: Level, Number Type & Seed](#2-konsep-inti-level-number-type--seed)
3. [Arsitektur Sistem](#3-arsitektur-sistem)
4. [Tech Stack & Dependensi](#4-tech-stack--dependensi)
5. [Struktur Direktori (v2)](#5-struktur-direktori-v2)
6. [Sistem Tipe Bilangan](#6-sistem-tipe-bilangan)
7. [Sistem Level Arithmetic](#7-sistem-level-arithmetic)
8. [Core Arithmetic — Spesifikasi Modul](#8-core-arithmetic--spesifikasi-modul)
9. [Seed-Based Generation System](#9-seed-based-generation-system)
10. [Layer Service & Blueprint](#10-layer-service--blueprint)
11. [Schemas (Kontrak JSON)](#11-schemas-kontrak-json)
12. [API Endpoint Specification](#12-api-endpoint-specification)
13. [Standar Kode & Konvensi](#13-standar-kode--konvensi)
14. [Error Handling](#14-error-handling)
15. [Pengujian (Testing Strategy)](#15-pengujian-testing-strategy)
16. [Environment & Konfigurasi](#16-environment--konfigurasi)
17. [Rencana Kerja (Roadmap)](#17-rencana-kerja-roadmap)
18. [Architecture Decision Records (ADR)](#18-architecture-decision-records-adr)

---

## 1. Ringkasan Proyek

**Python Math Engine** adalah *microservice* berbasis REST API yang berfungsi sebagai backend matematis untuk aplikasi **CBT (Computer Based Test)**. Sistem ini menghasilkan soal matematika yang *reproducible* (bisa diulang dengan seed yang sama), terstruktur per level, dan mendukung berbagai tipe bilangan.

### 1.1 Tanggung Jawab Utama

| Tanggung Jawab | Deskripsi |
|---|---|
| **Seed-Based Math Generation** | Angka soal yang sama dihasilkan ulang jika seed sama |
| **Level-Based Difficulty** | Parameter kesulitan berupa angka integer (Level 1–N) |
| **Number Type System** | Mendukung 12+ tipe bilangan matematika yang berbeda |
| **Precision Arithmetic** | Bebas floating-point error menggunakan `Fraction` dan `Decimal` |
| **Logic Blueprinting** | Urutan operasi sebagai kunci jawaban drag-and-drop |
| **Distractor Logic** | Jawaban salah berbasis miskonsepsi siswa per operasi |
| **AI Contextualization** | Soal cerita via LM Studio lokal |
| **Geometry Mesh Computing** | Koordinat 3D untuk renderer Three.js |

### 1.2 Batasan Sistem

- ✅ Stateless — setiap request berdiri sendiri
- ✅ Reproducible — seed yang sama → soal yang sama
- ✅ Mendukung operasi campuran multi-step
- ❌ Tidak menyimpan data soal ke database
- ❌ Tidak mengelola sesi siswa atau hasil ujian
- ❌ Tidak melakukan rendering visual (diserahkan ke React)

---

## 2. Konsep Inti: Level, Number Type & Seed

Ini adalah tiga pilar utama sistem generate soal di v2.

### 2.1 Level (Parameter Kesulitan)

Level adalah **integer** yang merepresentasikan kompleksitas soal secara menyeluruh. Level mengontrol:

- Rentang nilai angka yang digunakan
- Tipe bilangan yang diizinkan
- Jumlah operasi dalam soal campuran
- Kompleksitas struktur (misal: multi-step vs single-step)

```
Level 1  → Paling mudah  (bilangan cacah kecil, operasi tunggal)
Level 2  → Mudah
Level 3  → Sedang
Level 4  → Agak sulit
Level 5  → Sulit
Level 6  → Sangat sulit
Level 7  → Expert (operasi campuran kompleks, bilangan real)
...
Level N  → Dapat dikembangkan sesuai kebutuhan kurikulum
```

> **Desain Keputusan:** Menggunakan angka (bukan "easy/medium/hard") agar lebih granular, dapat dikembangkan tanpa mengubah API, dan mudah dipetakan ke jenjang kelas (Level 1 = Kelas 1 SD, dst).

### 2.2 Number Type (Tipe Bilangan)

Tipe bilangan adalah **jenis bilangan** yang digunakan sebagai operand dalam soal. Ini terpisah dari level — level mengontrol *kompleksitas*, number type mengontrol *jenis bilangan*.

### 2.3 Seed

Seed adalah **integer** yang menjadi kunci deterministik untuk PRNG (Pseudo-Random Number Generator). Dengan seed yang sama dan parameter yang sama, engine akan selalu menghasilkan soal yang identik.

```
seed=42, operation="addition", level=3, number_type="fraction"
→ Selalu menghasilkan: 3/7 + 5/14
```

---

## 3. Arsitektur Sistem

### 3.1 Diagram Alir Data

```
┌──────────────┐    POST /arithmetic/generate     ┌────────────────────────────┐
│   Laravel    │ ──────────────────────────────►  │    Python Math Engine      │
│  (Orkestr.)  │ ◄──────────────────────────────  │       (FastAPI)            │
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

### 3.2 Prinsip Arsitektur

1. **Seed-First** — SeedManager diinisialisasi sebelum generator apapun dipanggil
2. **Number Type sebagai Constraint** — setiap operasi menerima `NumberType` sebagai filter domain bilangan
3. **Pure Functions di Core** — tidak ada I/O, tidak ada side effect
4. **Level sebagai Config Bundle** — setiap level memetakan ke sebuah `LevelConfig` yang berisi semua parameter

---

## 4. Tech Stack & Dependensi

```toml
# requirements.txt

# Web Framework
fastapi==0.111.0
uvicorn[standard]==0.29.0

# Data Validation
pydantic==2.7.0
pydantic-settings==2.2.1

# Matematika — Presisi
sympy==1.12            # Simbolik: simplifikasi, primality check, faktorisasi
numpy==1.26.4          # Komputasi geometri & array

# Utilitas
python-dotenv==1.0.1
httpx==0.27.0          # Async HTTP untuk LM Studio

# requirements-dev.txt
pytest==8.2.0
pytest-asyncio==0.23.6
ruff==0.4.4
mypy==1.10.0
```

> **Catatan:** Library `fractions` dan `decimal` adalah bawaan Python stdlib — tidak perlu install tambahan.

---

## 5. Struktur Direktori (v2)

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
│   │   ├── number_types/                # ★ BARU: Definisi & validator tipe bilangan
│   │   │   ├── __init__.py
│   │   │   ├── registry.py              # Enum & mapping semua NumberType
│   │   │   ├── validators.py            # Fungsi cek: is_prime(), is_composite(), dll
│   │   │   └── generators.py           # Generator bilangan per tipe & level
│   │   │
│   │   ├── seed/                        # ★ BARU: Seed management
│   │   │   ├── __init__.py
│   │   │   └── manager.py              # SeedManager class (wrapper random)
│   │   │
│   │   ├── levels/                      # ★ BARU: Definisi konfigurasi per level
│   │   │   ├── __init__.py
│   │   │   └── config.py               # LevelConfig dataclass & registry level 1-7+
│   │   │
│   │   ├── arithmetic/                  # ★ DIRESTRUKTUR: Satu file per operasi
│   │   │   ├── __init__.py
│   │   │   ├── addition.py              # Penjumlahan
│   │   │   ├── subtraction.py          # Pengurangan
│   │   │   ├── multiplication.py       # Perkalian
│   │   │   ├── division.py             # Pembagian
│   │   │   ├── power.py                # Perpangkatan
│   │   │   ├── root.py                 # Penarikan akar
│   │   │   ├── modulo.py               # Operasi modulo / sisa bagi
│   │   │   ├── mixed_operations.py     # Operasi campuran multi-step
│   │   │   ├── number_properties.py    # FPB, KPK, faktor, kelipatan
│   │   │   └── comparison.py           # Perbandingan & urutan bilangan
│   │   │
│   │   ├── geometry/
│   │   │   ├── __init__.py
│   │   │   ├── shapes_2d.py
│   │   │   ├── shapes_3d.py
│   │   │   ├── mesh_generator.py
│   │   │   └── composite.py
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
│   │   ├── arithmetic_service.py        # Koordinasi core → blueprint
│   │   ├── geometry_service.py
│   │   ├── measurement_service.py
│   │   ├── algebra_service.py
│   │   ├── statistics_service.py
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
│       └── test_seed_reproducibility.py  # ★ Penting: test seed menghasilkan output sama
│
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## 6. Sistem Tipe Bilangan

### 6.1 Registry Tipe Bilangan

File: `app/core/number_types/registry.py`

```python
from enum import Enum

class NumberType(str, Enum):
    """
    Semua tipe bilangan yang didukung engine.
    Nilai string digunakan langsung sebagai parameter API.
    """
    # ── Bilangan berbasis himpunan ──────────────────────────────────────────
    NATURAL        = "natural"        # Bilangan asli: {1, 2, 3, ...}
    WHOLE          = "whole"          # Bilangan cacah: {0, 1, 2, 3, ...}
    INTEGER        = "integer"        # Bilangan bulat: {..., -2, -1, 0, 1, 2, ...}
    INTEGER_POS    = "integer_pos"    # Bilangan bulat positif: {1, 2, 3, ...}
    INTEGER_NEG    = "integer_neg"    # Bilangan bulat negatif: {..., -3, -2, -1}
    REAL           = "real"           # Bilangan real (mencakup semua di bawah)

    # ── Bilangan berbasis sifat ─────────────────────────────────────────────
    PRIME          = "prime"          # Bilangan prima: {2, 3, 5, 7, 11, ...}
    COMPOSITE      = "composite"      # Bilangan komposit: {4, 6, 8, 9, 10, ...}

    # ── Bilangan berbasis representasi ─────────────────────────────────────
    DECIMAL        = "decimal"        # Desimal: 1.5, 3.14, 0.25
    FRACTION       = "fraction"       # Pecahan biasa: 1/2, 3/4, 5/6
    MIXED_FRACTION = "mixed_fraction" # Pecahan campuran: 1½, 2¾, 3⅓
```

### 6.2 Definisi & Batasan per Tipe

| NumberType | Himpunan | Contoh Nilai | Negatif? | Nol? | Desimal? |
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
| `real` | ℝ (gabungan) | Semua di atas | ✅ | ✅ | ✅ |

### 6.3 Implementasi Generator per Tipe

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
    Menghasilkan satu bilangan sesuai tipe dan konfigurasi level.
    Selalu menggunakan `rng` (seeded) — tidak pernah memanggil random secara langsung.

    Args:
        number_type:  Tipe bilangan yang diinginkan
        level_config: Konfigurasi range dari level saat ini
        rng:          Instance random.Random yang sudah di-seed

    Returns:
        Bilangan sesuai tipe: int, float, atau Fraction
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
            return Fraction(numer, denom)  # Otomatis disederhanakan

        case NumberType.MIXED_FRACTION:
            whole_part = rng.randint(1, level_config.max_mixed_whole)
            denom = rng.choice(level_config.allowed_denominators)
            numer = rng.randint(1, denom - 1)
            return Fraction(whole_part * denom + numer, denom)

        case NumberType.REAL:
            # Pilih sub-tipe secara acak dari yang diizinkan level
            sub_type = rng.choice(level_config.real_sub_types)
            return generate_number(sub_type, level_config, rng)
```

### 6.4 Implementasi Validator

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
    """Pecahan biasa: 0 < f < 1"""
    return 0 < f < 1

def is_mixed_fraction(f: Fraction) -> bool:
    """Pecahan campuran: f > 1 dan bukan integer"""
    return f > 1 and f.denominator != 1

def classify_number(n) -> list[str]:
    """
    Mengklasifikasikan satu angka ke semua NumberType yang berlaku.
    Berguna untuk debugging dan validasi.

    Returns: list label yang berlaku, misal: ["natural", "whole", "integer_pos", "prime"]
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
    labels.append("real")  # Semua bilangan adalah real
    return labels
```

---

## 7. Sistem Level Arithmetic

### 7.1 LevelConfig Dataclass

File: `app/core/levels/config.py`

```python
from dataclasses import dataclass, field
from ..number_types.registry import NumberType

@dataclass(frozen=True)
class LevelConfig:
    """
    Bundel konfigurasi untuk satu level.
    Bersifat immutable (frozen=True) — tidak boleh diubah saat runtime.
    """
    level: int

    # ── Rentang nilai integer ───────────────────────────────────────────────
    min_value: int            # Nilai minimum operand integer
    max_value: int            # Nilai maksimum operand integer

    # ── Konfigurasi desimal ─────────────────────────────────────────────────
    min_decimal: float        # Nilai minimum untuk bilangan desimal
    max_decimal: float        # Nilai maksimum untuk bilangan desimal
    decimal_places: int       # Jumlah digit di belakang koma

    # ── Konfigurasi pecahan ─────────────────────────────────────────────────
    allowed_denominators: list[int]  # Penyebut yang diizinkan
    max_mixed_whole: int      # Bagian bulat maks untuk pecahan campuran

    # ── Konfigurasi operasi campuran ────────────────────────────────────────
    max_operations: int       # Jumlah operasi maks dalam soal campuran
    allow_parentheses: bool   # Apakah boleh ada tanda kurung

    # ── Konfigurasi akar & pangkat ──────────────────────────────────────────
    max_exponent: int         # Eksponen maksimum (misal: x² → max_exponent=2)
    allowed_roots: list[int]  # Jenis akar yang diizinkan (misal: [2, 3] = √ dan ∛)

    # ── NumberType yang valid untuk level ini ───────────────────────────────
    allowed_number_types: list[NumberType]

    # ── Sub-tipe untuk NumberType.REAL ─────────────────────────────────────
    real_sub_types: list[NumberType] = field(default_factory=list)
```

### 7.2 Registry Level (Level 1–7)

```python
# app/core/levels/config.py (lanjutan)

LEVEL_REGISTRY: dict[int, LevelConfig] = {

    1: LevelConfig(
        level=1,
        # Integer kecil saja
        min_value=1,            max_value=10,
        # Desimal tidak digunakan di level ini
        min_decimal=0.0,        max_decimal=0.0,    decimal_places=0,
        # Pecahan tidak digunakan
        allowed_denominators=[],                    max_mixed_whole=0,
        # Satu operasi, tanpa kurung
        max_operations=1,       allow_parentheses=False,
        # Pangkat & akar minimal
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
        max_exponent=2,         allowed_roots=[2],  # Akar kuadrat saja
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
    """Mengambil LevelConfig dari registry. Raise error jika level tidak tersedia."""
    if level not in LEVEL_REGISTRY:
        raise ValueError(
            f"Level {level} tidak tersedia. Level yang valid: {sorted(LEVEL_REGISTRY.keys())}"
        )
    return LEVEL_REGISTRY[level]
```

### 7.3 Matriks Level × Operasi

Tabel ini mendefinisikan operasi apa saja yang tersedia di setiap level:

| Operasi | L1 | L2 | L3 | L4 | L5 | L6 | L7 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Penjumlahan | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pengurangan | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Perkalian | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pembagian | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Perpangkatan | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Akar Kuadrat | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Akar Pangkat N | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Modulo | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| FPB / KPK | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Operasi Campuran | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Campuran + Kurung | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Bilangan Negatif | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Pecahan Campuran | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |

---

## 8. Core Arithmetic — Spesifikasi Modul

> **Aturan Global:** Semua fungsi di `core/arithmetic/` adalah **pure functions**. Menerima `rng: random.Random` dan `level_config: LevelConfig` sebagai parameter — tidak pernah memanggil `random` secara langsung.

### 8.1 `addition.py` — Penjumlahan

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
    Menghasilkan soal penjumlahan.

    Args:
        rng:           RNG yang sudah di-seed
        level_config:  Konfigurasi level aktif
        number_type:   Tipe bilangan operand
        operand_count: Jumlah operand (default 2, maks 5)

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
        - Hasil selalu bilangan yang "bersih" (tidak ada desimal berulang)
        - Untuk pecahan: penyebut hasil tidak melebihi allowed_denominators
        - operand_count dibatasi oleh level_config.max_operations + 1
    """
    ...

def _ensure_clean_result_fraction(operands: list[Fraction]) -> list[Fraction] | None:
    """
    Memvalidasi bahwa penjumlahan list pecahan menghasilkan pecahan sederhana.
    Return None jika tidak valid (trigger re-generate).
    """
    ...
```

**Aturan "Hasil Bersih" per NumberType:**

| NumberType | Syarat Hasil Bersih |
|---|---|
| `natural` / `whole` | Hasil adalah integer non-negatif |
| `integer` | Hasil adalah integer (boleh negatif) |
| `fraction` | Hasil sudah disederhanakan, penyebut ≤ 60 |
| `mixed_fraction` | Bagian pecahan sudah disederhanakan |
| `decimal` | Digit desimal ≤ `level_config.decimal_places` |

---

### 8.2 `subtraction.py` — Pengurangan

```python
def generate_subtraction(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    allow_negative_result: bool | None = None
) -> dict:
    """
    Menghasilkan soal pengurangan.

    Args:
        allow_negative_result: Jika None, otomatis mengikuti level_config.
                               Jika level < 4, hasil selalu ≥ 0.

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
        - Untuk level 1-3: operand_1 selalu ≥ operand_2 (hasil tidak negatif)
        - Untuk level 4+: boleh negatif jika number_type mendukung
    """
    ...
```

---

### 8.3 `multiplication.py` — Perkalian

```python
def generate_multiplication(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    operand_count: int = 2
) -> dict:
    """
    Menghasilkan soal perkalian.

    Returns:
        {
            "operands": ["1/2", "3/4"],
            "operation": "multiplication",
            "expression": "1/2 × 3/4",
            "result": "3/8",
            "result_type": "fraction",
            "steps": ["1/2 × 3/4 = (1×3)/(2×4) = 3/8"]
        }

    Constraint (khusus pecahan):
        - Hasil tidak boleh > level_config.max_value (untuk soal yang masuk akal)
        - Untuk perkalian dua pecahan: hasil otomatis disederhanakan
    """
    ...
```

---

### 8.4 `division.py` — Pembagian

```python
def generate_division(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    result_type: NumberType | None = None
) -> dict:
    """
    Menghasilkan soal pembagian dengan hasil yang selalu bersih.

    Strategy:
        Untuk memastikan hasil bersih, generate hasil (quotient) terlebih dahulu,
        lalu backward-compute dividend dari divisor × quotient.

    Args:
        result_type: Tipe bilangan hasil yang diinginkan.
                     Jika None, mengikuti number_type.

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
        - Pembagi (divisor) tidak pernah 0
        - Untuk level 1-3: hasil selalu integer positif (no remainders)
        - Untuk level 4+: hasil boleh pecahan jika number_type = fraction
    """
    ...

def _generate_clean_division_pair(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType
) -> tuple:
    """
    Backward strategy: pilih quotient dulu → kalikan dengan divisor → dapat dividend.
    Memastikan hasil selalu bersih.
    """
    ...
```

---

### 8.5 `power.py` — Perpangkatan

```python
def generate_power(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    exponent: int | None = None
) -> dict:
    """
    Menghasilkan soal perpangkatan: base^exponent.

    Args:
        exponent: Jika None, dipilih secara acak dari range [2, level_config.max_exponent]

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
        - Hasil tidak melebihi level_config.max_value × 100
        - Untuk pecahan: (a/b)^n — pembilang dan penyebut dihitung terpisah
        - Pangkat 0 hanya muncul di level 5+ (karena konsep x⁰ = 1 perlu dipahami dulu)
        - Pangkat negatif hanya di level 6+
    """
    ...
```

---

### 8.6 `root.py` — Penarikan Akar

```python
def generate_root(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    root_degree: int | None = None
) -> dict:
    """
    Menghasilkan soal penarikan akar: ⁿ√radicand.

    Strategy:
        Backward approach — pilih result (integer bersih) dulu,
        lalu hitung radicand = result^degree.

    Args:
        root_degree: Pangkat akar (2=kuadrat, 3=kubik, dst).
                     Jika None, dipilih dari level_config.allowed_roots.

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
        - Hasil SELALU integer bersih (backward generation menjamin ini)
        - root_degree 2 = akar kuadrat, 3 = akar kubik, dst
        - Akar kubik hanya muncul di level 4+ (sesuai LevelConfig.allowed_roots)
    """
    ...

def _generate_perfect_root(
    rng: random.Random,
    level_config: LevelConfig,
    degree: int
) -> tuple[int, int]:
    """
    Returns (radicand, result) dimana radicand = result^degree.
    result dipilih dari [2, int(level_config.max_value**(1/degree))].
    """
    ...
```

---

### 8.7 `modulo.py` — Operasi Modulo / Sisa Bagi

```python
def generate_modulo(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType
) -> dict:
    """
    Menghasilkan soal sisa bagi: dividend % divisor.

    Returns:
        {
            "operands": ["17", "5"],
            "operation": "modulo",
            "expression": "17 mod 5",
            "result": "2",
            "result_type": "whole",
            "steps": ["17 ÷ 5 = 3 sisa 2", "Jadi 17 mod 5 = 2"]
        }

    Constraint:
        - Hanya untuk NumberType integer (natural, whole, integer)
        - Divisor selalu ≥ 2
        - Sisa selalu < divisor (properti modulo)
        - Muncul mulai Level 3
    """
    ...
```

---

### 8.8 `number_properties.py` — FPB, KPK, Faktor, Kelipatan

```python
from sympy import gcd, lcm, factorint

def generate_gcd_problem(
    rng: random.Random,
    level_config: LevelConfig
) -> dict:
    """
    Menghasilkan soal FPB (Faktor Persekutuan Terbesar).

    Strategy:
        Pilih GCD target dulu, lalu buat dua angka yang keduanya merupakan
        kelipatan dari GCD target.

    Returns:
        {
            "operands": ["12", "18"],
            "operation": "gcd",
            "expression": "FPB(12, 18)",
            "result": "6",
            "steps": [
                "Faktor 12: 1, 2, 3, 4, 6, 12",
                "Faktor 18: 1, 2, 3, 6, 9, 18",
                "Faktor persekutuan: 1, 2, 3, 6",
                "FPB = 6"
            ]
        }
    """
    ...

def generate_lcm_problem(rng, level_config) -> dict:
    """Menghasilkan soal KPK (Kelipatan Persekutuan Terkecil)."""
    ...

def generate_factor_problem(rng, level_config) -> dict:
    """Menghasilkan soal faktorisasi prima."""
    ...

def generate_multiple_problem(rng, level_config) -> dict:
    """Menghasilkan soal kelipatan bilangan."""
    ...
```

---

### 8.9 `mixed_operations.py` — Operasi Campuran

```python
from dataclasses import dataclass
from typing import Literal

OperationName = Literal["addition", "subtraction", "multiplication", "division",
                        "power", "root", "modulo"]

@dataclass
class MixedStep:
    step_id: str            # "s1", "s2", dst
    operation: OperationName
    inputs: list[str]       # ID variabel atau ID step sebelumnya
    result: str             # Hasil step ini
    expression: str         # Representasi string step ini

def generate_mixed_operations(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType,
    operation_count: int | None = None,
    with_parentheses: bool | None = None
) -> dict:
    """
    Menghasilkan soal operasi campuran multi-step.

    Args:
        operation_count: Jumlah operasi. Jika None, dipilih dari
                         range [2, level_config.max_operations]
        with_parentheses: Jika None, mengikuti level_config.allow_parentheses.

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

    Strategi Generate:
        1. Pilih urutan operasi secara acak dari yang valid untuk level ini
        2. Generate intermediate result terlebih dahulu agar hasil akhir bersih
        3. Backward-compute semua operand
        4. Validasi tidak ada pembagian by zero atau akar dari negatif
    """
    ...

def _build_expression_tree(steps: list[MixedStep], with_parentheses: bool) -> str:
    """
    Membangun string ekspresi dari daftar steps, dengan atau tanpa tanda kurung.
    Memperhatikan BODMAS/PEMDAS untuk penempatan kurung yang benar.
    """
    ...
```

**Aturan Validasi Operasi Campuran:**

```
1. Tidak boleh ada pembagian by zero di langkah manapun
2. Tidak boleh ada akar dari bilangan negatif
3. Hasil intermediate tidak boleh melebihi level_config.max_value × 1000
4. Ekspresi akhir harus deterministic (urutan operasi sama → hasil sama)
5. Tanda kurung ditempatkan berdasarkan aturan BODMAS yang benar
```

---

### 8.10 `comparison.py` — Perbandingan & Urutan Bilangan

```python
def generate_comparison(
    rng: random.Random,
    level_config: LevelConfig,
    number_type: NumberType
) -> dict:
    """
    Menghasilkan soal perbandingan dua bilangan (>, <, =).

    Returns:
        {
            "operands": ["3/4", "2/3"],
            "operation": "comparison",
            "expression": "3/4 ___ 2/3",
            "result": ">",
            "steps": [
                "Samakan penyebut: 3/4 = 9/12, 2/3 = 8/12",
                "9/12 > 8/12",
                "Jadi 3/4 > 2/3"
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
    Menghasilkan soal mengurutkan bilangan.

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

## 9. Seed-Based Generation System

### 9.1 Filosofi Seed

Seed memungkinkan **reproducibility** — soal yang sama dihasilkan ulang kapanpun dengan seed yang sama, tanpa menyimpan soal ke database.

```
Input: seed=1234, operation="addition", level=3, number_type="fraction"
Output: Selalu menghasilkan ekspresi yang SAMA persis

→ Berguna untuk: retry soal, share soal ke siswa lain, audit, debugging
```

### 9.2 SeedManager

File: `app/core/seed/manager.py`

```python
import random
import hashlib
from dataclasses import dataclass

@dataclass(frozen=True)
class SeedContext:
    """Konteks lengkap yang membentuk seed unik per soal."""
    seed: int
    operation: str
    level: int
    number_type: str

class SeedManager:
    """
    Wrapper di atas random.Random untuk seed-based generation.
    Setiap instance bersifat independent — tidak ada shared state.
    """

    def __init__(self, context: SeedContext):
        self._context = context
        self._rng = random.Random()
        self._rng.seed(self._make_deterministic_seed(context))

    @property
    def rng(self) -> random.Random:
        """Instance RNG yang sudah di-seed. Gunakan ini untuk semua operasi random."""
        return self._rng

    @staticmethod
    def _make_deterministic_seed(ctx: SeedContext) -> int:
        """
        Menggabungkan semua parameter menjadi satu seed integer yang deterministik.

        Menggunakan hash SHA-256 untuk distribusi yang merata dan bebas collision.
        Format string: "seed:op:level:numtype"
        """
        raw = f"{ctx.seed}:{ctx.operation}:{ctx.level}:{ctx.number_type}"
        hash_bytes = hashlib.sha256(raw.encode()).digest()
        return int.from_bytes(hash_bytes[:8], byteorder="big")

    def get_context(self) -> SeedContext:
        return self._context
```

### 9.3 Integrasi Seed dalam Generator

Setiap fungsi generator **wajib** menerima `rng: random.Random` sebagai parameter, bukan memanggilnya secara global:

```python
# ✅ BENAR — Deterministik karena rng dikontrol dari luar
def generate_addition(rng: random.Random, level_config: LevelConfig, ...) -> dict:
    a = generate_number(number_type, level_config, rng)  # rng diteruskan ke bawah
    b = generate_number(number_type, level_config, rng)
    ...

# ❌ SALAH — Memanggil random langsung, tidak reproducible
def generate_addition(level_config: LevelConfig, ...) -> dict:
    a = random.randint(1, 100)   # ← tidak deterministik!
    ...
```

### 9.4 Alur Seed di Service Layer

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

    # 1. Buat SeedContext — kombinasi unik dari semua parameter
    ctx = SeedContext(seed=seed, operation=operation, level=level, number_type=number_type)

    # 2. Inisialisasi SeedManager — RNG di-seed di sini
    seed_manager = SeedManager(ctx)

    # 3. Ambil LevelConfig
    level_config = get_level_config(level)

    # 4. Jalankan generator dengan rng dari seed_manager
    raw_data = generate_addition(
        rng=seed_manager.rng,
        level_config=level_config,
        number_type=NumberType(number_type)
    )

    # 5. Bangun blueprint & distractor
    ...
```

### 9.5 Jaminan Reproducibility

Reproducibility dijamin oleh dua hal:

1. **Deterministik seed** — SHA-256 dari (seed + operation + level + number_type) → integer konsisten
2. **Urutan pemanggilan rng tetap** — setiap generator harus memanggil `rng` dalam urutan yang sama setiap kali dieksekusi (tidak boleh ada kondisi yang mengubah jumlah pemanggilan rng berdasarkan nilai intermediate)

```python
# ✅ BENAR — Urutan rng call selalu sama
a = rng.randint(1, 10)   # call ke-1
b = rng.randint(1, 10)   # call ke-2
result = a + b

# ❌ SALAH — Jumlah rng call berubah berdasarkan nilai
a = rng.randint(1, 10)
if a > 5:
    b = rng.randint(1, 20)   # call ke-2 HANYA jika a > 5 → tidak deterministik
```

---

## 10. Layer Service & Blueprint

### 10.1 `services/arithmetic_service.py`

Koordinator utama yang menggabungkan semua layer:

```python
async def generate_arithmetic_question(request: ArithmeticRequest) -> ArithmeticResponse:
    """
    Alur lengkap generate soal arithmetic:
    
    1. Resolve SeedContext & SeedManager
    2. Resolve LevelConfig
    3. Validasi NumberType vs Level (apakah tipe ini tersedia di level ini?)
    4. Panggil core generator sesuai operation
    5. Bangun blueprint via blueprint.py
    6. Bangun distractors via distractor.py
    7. (Opsional) Panggil AI storyteller
    8. Kembalikan ArithmeticResponse
    """
    ...

def _validate_number_type_for_level(number_type: NumberType, level_config: LevelConfig):
    """Validasi apakah number_type tersedia di level yang diminta."""
    if number_type not in level_config.allowed_number_types:
        raise InvalidNumberTypeForLevelError(
            f"NumberType '{number_type}' tidak tersedia di Level {level_config.level}. "
            f"Available: {[t.value for t in level_config.allowed_number_types]}"
        )
```

### 10.2 `services/blueprint.py`

```python
def build_arithmetic_blueprint(raw_data: dict, operation: str) -> list[dict]:
    """
    Mengubah raw_data dari core menjadi blueprint drag-and-drop.

    Format Blueprint Step:
    {
        "step": 1,
        "op": "addition",
        "op_symbol": "+",
        "inputs": ["v1", "v2"],
        "correct_result": "3/4",
        "result_type": "fraction",
        "hint": "Samakan penyebut terlebih dahulu"
    }
    """
    ...
```

### 10.3 `services/distractor.py`

```python
MISCONCEPTION_RULES: dict[str, list[callable]] = {
    "addition_fraction": [
        _add_numerators_and_denominators,   # 1/2 + 1/3 → 2/5
        _forget_simplify,                    # hasil tidak disederhanakan
        _use_wrong_lcd,                      # LCD salah hitung
    ],
    "subtraction_integer_neg": [
        _ignore_negative_sign,               # -5 - 3 → 2 (harusnya -8)
        _flip_sign,                          # -5 - 3 → 8
    ],
    "division_fraction": [
        _forget_reciprocal,                  # lupa membalik pecahan kedua
        _divide_numerators_separately,       # membagi pembilang & penyebut terpisah
    ],
    "power_fraction": [
        _only_power_numerator,               # (1/2)² → 1/2 (harusnya 1/4)
    ],
    "root": [
        _halve_radicand,                     # √144 → 72 (bagi 2 bukan akar)
        _subtract_degree_from_radicand,      # √144 → 142
    ],
    # ... dan seterusnya
}

def generate_distractors(
    correct_answer: str,
    operation: str,
    number_type: str,
    count: int = 3,
    rng: random.Random | None = None   # Opsional: bisa juga seed-based
) -> list[str]:
    """
    Menghasilkan `count` distractor berbasis miskonsepsi.
    Semua distractor dijamin berbeda dari correct_answer dan satu sama lain.
    """
    ...
```

---

## 11. Schemas (Kontrak JSON)

### 11.1 `schemas/request.py`

```python
from pydantic import BaseModel, Field, model_validator
from typing import Literal
from app.core.number_types.registry import NumberType
from app.core.levels.config import LEVEL_REGISTRY

ArithmeticOperation = Literal[
    "addition", "subtraction", "multiplication", "division",
    "power", "root", "modulo", "gcd", "lcm", "mixed",
    "comparison", "ordering", "factorization"
]

class ArithmeticRequest(BaseModel):
    # ── Parameter Wajib ──────────────────────────────────────────────────────
    seed: int = Field(..., description="Seed untuk reproducible generation")
    level: int = Field(..., ge=1, le=7, description="Level kesulitan (1–7)")
    operation: ArithmeticOperation = Field(..., description="Jenis operasi matematika")
    number_type: NumberType = Field(..., description="Tipe bilangan yang digunakan")

    # ── Parameter Opsional ───────────────────────────────────────────────────
    operand_count: int = Field(default=2, ge=2, le=5,
                               description="Jumlah operand (untuk penjumlahan/perkalian)")
    with_story: bool = Field(default=True, description="Generate soal cerita via LM Studio")
    with_distractors: bool = Field(default=True, description="Sertakan pilihan jawaban salah")
    distractor_count: int = Field(default=3, ge=2, le=4)
    theme: str = Field(default="general", description="Tema soal cerita")

    # ── Validasi Lintas Field ─────────────────────────────────────────────────
    @model_validator(mode="after")
    def validate_number_type_for_level(self):
        from app.core.levels.config import get_level_config
        cfg = get_level_config(self.level)
        if self.number_type not in cfg.allowed_number_types:
            raise ValueError(
                f"NumberType '{self.number_type}' tidak tersedia di Level {self.level}. "
                f"Gunakan: {[t.value for t in cfg.allowed_number_types]}"
            )
        return self
```

### 11.2 `schemas/response.py` — Struktur Lengkap

#### Response Soal Aritmetika Standar

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
    "story": "Budi memiliki 3/4 kg beras dan Susi memiliki 1/4 kg beras. Berapa total beras mereka?",
    "theme": "shopping"
  },
  "data": {
    "variables": [
      {"id": "v1", "label": "Beras Budi", "value": "3/4", "unit": "kg", "type": "fraction"},
      {"id": "v2", "label": "Beras Susi", "value": "1/4", "unit": "kg", "type": "fraction"}
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
        "hint": "Penyebut sudah sama, langsung jumlahkan pembilang"
      }
    ],
    "answer_choices": ["1", "4/8", "2/4", "1/2"],
    "correct_answer": "1",
    "answer_type": "whole"
  }
}
```

#### Response Soal Operasi Campuran

```json
{
  "status": "success",
  "meta": {
    "seed": 9999,
    "level": 5,
    "operation": "mixed",
    "number_type": "integer",
    "generated_at": "2025-01-15T10:30:00Z"
  },
  "context": {
    "story": "...",
    "theme": "general"
  },
  "data": {
    "variables": [
      {"id": "v1", "value": "12", "type": "natural"},
      {"id": "v2", "value": "4",  "type": "natural"},
      {"id": "v3", "value": "3",  "type": "natural"}
    ],
    "expression": "(12 + 4) × 3",
    "expression_latex": "(12 + 4) \\times 3",
    "blueprint": [
      {
        "step": 1,
        "op": "addition",
        "op_symbol": "+",
        "inputs": ["v1", "v2"],
        "correct_result": "16",
        "result_type": "natural",
        "hint": "Kerjakan yang di dalam kurung dulu"
      },
      {
        "step": 2,
        "op": "multiplication",
        "op_symbol": "×",
        "inputs": ["step_1", "v3"],
        "correct_result": "48",
        "result_type": "natural",
        "hint": null
      }
    ],
    "answer_choices": ["48", "45", "60", "39"],
    "correct_answer": "48",
    "answer_type": "natural"
  }
}
```

#### Response Error

```json
{
  "status": "error",
  "error_code": "INVALID_NUMBER_TYPE_FOR_LEVEL",
  "message": "NumberType 'mixed_fraction' tidak tersedia di Level 1. Gunakan: ['natural', 'whole']",
  "detail": {
    "seed": 1234,
    "level": 1,
    "number_type": "mixed_fraction",
    "available_types": ["natural", "whole"]
  }
}
```

---

## 12. API Endpoint Specification

### Base URL: `/api/v1`

| Method | Endpoint | Deskripsi |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/levels` | Daftar semua level beserta konfigurasinya |
| `GET` | `/levels/{level}` | Detail konfigurasi satu level |
| `GET` | `/number-types` | Daftar semua tipe bilangan yang didukung |
| `GET` | `/operations` | Daftar semua operasi yang didukung |
| `GET` | `/operations/{level}` | Operasi yang tersedia untuk level tertentu |
| `POST` | `/arithmetic/generate` | Generate soal aritmetika |
| `POST` | `/arithmetic/validate-params` | Validasi parameter tanpa generate soal |
| `POST` | `/geometry/generate` | Generate soal geometri |
| `POST` | `/measurement/generate` | Generate soal pengukuran |
| `POST` | `/algebra/generate` | Generate soal aljabar |
| `POST` | `/statistics/generate` | Generate soal statistik |
| `POST` | `/probability/generate` | Generate soal peluang |

### Contoh Request: Generate Soal

```bash
# Penjumlahan pecahan, level 3, seed 42
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

# Operasi campuran, level 5, bilangan integer
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
```

### Contoh Response: GET /levels

```json
{
  "levels": [
    {
      "level": 1,
      "label": "Level 1",
      "description": "Bilangan cacah kecil, operasi tunggal",
      "max_value": 10,
      "allowed_operations": ["addition", "subtraction"],
      "allowed_number_types": ["natural", "whole"]
    },
    {
      "level": 2,
      "label": "Level 2",
      "description": "Bilangan asli hingga 50, termasuk prima",
      "max_value": 50,
      "allowed_operations": ["addition", "subtraction", "multiplication", "division", "power", "root"],
      "allowed_number_types": ["natural", "whole", "prime"]
    }
  ]
}
```

---

## 13. Standar Kode & Konvensi

### 13.1 Naming Convention

| Jenis | Konvensi | Contoh |
|---|---|---|
| File & Folder | `snake_case` | `mixed_operations.py` |
| Class | `PascalCase` | `SeedManager`, `LevelConfig` |
| Fungsi & Variabel | `snake_case` | `generate_addition()` |
| Konstanta | `UPPER_SNAKE_CASE` | `LEVEL_REGISTRY` |
| Enum Value | `UPPER_SNAKE_CASE` | `NumberType.MIXED_FRACTION` |
| Endpoint | `kebab-case` | `/number-types` |

### 13.2 Aturan Wajib untuk Core Functions

```python
# ✅ Semua fungsi core HARUS:
# 1. Pure function (no side effects)
# 2. Menerima rng sebagai parameter
# 3. Menggunakan type hints
# 4. Memiliki docstring Google-style
# 5. Mengembalikan dict dengan key yang konsisten

def generate_addition(
    rng: random.Random,           # ← Wajib: RNG dari SeedManager
    level_config: LevelConfig,    # ← Wajib: konfigurasi level
    number_type: NumberType,      # ← Wajib: tipe bilangan
    operand_count: int = 2        # ← Opsional dengan default
) -> dict:                        # ← Selalu return dict
    ...

# ❌ Dilarang di core/:
# - import httpx, requests (I/O)
# - print(), logging.info() (side effects)
# - random.randint() langsung (harus lewat rng parameter)
# - global state apapun
```

### 13.3 Konvensi Key Dict Output

Semua fungsi generator **wajib** mengembalikan dict dengan key-key berikut (jika relevan):

```python
{
    "operands":         list[str],     # List operand sebagai string
    "operation":        str,           # Nama operasi
    "expression":       str,           # Ekspresi dalam teks biasa: "3/4 + 1/4"
    "expression_latex": str,           # Ekspresi LaTeX: "\\frac{3}{4} + \\frac{1}{4}"
    "result":           str,           # Hasil sebagai string
    "result_type":      str,           # NumberType dari hasil
    "steps":            list[str],     # Langkah penyelesaian
}
```

---

## 14. Error Handling

### 14.1 Exception Hierarchy

```python
# app/exceptions.py

class MathEngineError(Exception):
    """Base exception."""
    pass

# ── Level & Config ───────────────────────────────────────────────────────────
class InvalidLevelError(MathEngineError):
    """Level tidak tersedia."""
    pass

class InvalidNumberTypeForLevelError(MathEngineError):
    """NumberType tidak tersedia untuk level yang dipilih."""
    pass

class InvalidOperationForLevelError(MathEngineError):
    """Operasi tidak tersedia untuk level yang dipilih."""
    pass

# ── Generation ───────────────────────────────────────────────────────────────
class GenerationFailedError(MathEngineError):
    """Gagal generate angka yang valid setelah max_retries percobaan."""
    pass

class DivisionByZeroError(MathEngineError):
    """Hasil operasi menghasilkan pembagian by zero."""
    pass

class NegativeRadicandError(MathEngineError):
    """Mencoba mengambil akar dari bilangan negatif."""
    pass

# ── External ─────────────────────────────────────────────────────────────────
class LMStudioConnectionError(MathEngineError):
    """Gagal terhubung ke LM Studio."""
    pass
```

### 14.2 Retry Strategy untuk Generator

Beberapa generator mungkin gagal menghasilkan angka yang valid pada percobaan pertama (misal: tidak ada bilangan prima di range yang terlalu kecil). Gunakan retry loop dengan batas:

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
        f"Gagal generate soal valid setelah {MAX_GENERATION_RETRIES} percobaan. "
        f"Coba gunakan level atau number_type yang berbeda."
    )
```

---

## 15. Pengujian (Testing Strategy)

### 15.1 Struktur Test

```
tests/
├── unit/
│   ├── core/
│   │   ├── test_seed_manager.py        # ★ Prioritas tertinggi
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
    └── test_seed_reproducibility.py   # ★ Wajib: verifikasi seed bekerja
```

### 15.2 Test Wajib: Seed Reproducibility

```python
# tests/integration/test_seed_reproducibility.py

import pytest
from httpx import AsyncClient

class TestSeedReproducibility:

    @pytest.mark.asyncio
    async def test_same_seed_same_output(self, client: AsyncClient):
        """Dua request dengan seed & parameter sama HARUS menghasilkan output identik."""
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
        """Dua request dengan seed berbeda HARUS menghasilkan output berbeda."""
        base_params = {"level": 3, "operation": "addition",
                       "number_type": "fraction", "with_story": False}

        resp1 = await client.post("/api/v1/arithmetic/generate",
                                  json={**base_params, "seed": 1})
        resp2 = await client.post("/api/v1/arithmetic/generate",
                                  json={**base_params, "seed": 2})

        # Sangat kecil kemungkinan seed berbeda menghasilkan soal sama
        assert resp1.json()["data"]["expression"] != resp2.json()["data"]["expression"]

    @pytest.mark.asyncio
    async def test_seed_across_all_operations(self, client: AsyncClient):
        """Reproducibility berlaku untuk semua operasi."""
        operations = ["addition", "subtraction", "multiplication", "division",
                      "power", "root", "modulo"]
        for op in operations:
            params = {"seed": 1234, "level": 4, "operation": op,
                      "number_type": "natural", "with_story": False}
            r1 = await client.post("/api/v1/arithmetic/generate", json=params)
            r2 = await client.post("/api/v1/arithmetic/generate", json=params)
            assert r1.json()["data"]["result"] == r2.json()["data"]["result"], \
                f"Seed reproducibility gagal untuk operasi: {op}"
```

### 15.3 Test Wajib: Clean Result

```python
# tests/unit/core/test_division.py

class TestDivisionCleanResult:

    def test_integer_division_always_exact(self):
        """Pembagian integer harus selalu menghasilkan integer (no remainder)."""
        rng = random.Random(42)
        cfg = get_level_config(2)
        for _ in range(100):   # Test 100 kali
            result = generate_division(rng, cfg, NumberType.NATURAL)
            assert "." not in result["result"], \
                f"Hasil pembagian tidak bersih: {result['expression']} = {result['result']}"

    def test_fraction_result_is_simplified(self):
        """Pecahan hasil pembagian harus sudah disederhanakan."""
        rng = random.Random(99)
        cfg = get_level_config(3)
        for _ in range(50):
            result = generate_division(rng, cfg, NumberType.FRACTION)
            f = Fraction(result["result"])
            # Fraction() otomatis menyederhanakan, jadi cukup bandingkan string
            assert result["result"] == str(f), \
                f"Pecahan belum disederhanakan: {result['result']}"
```

---

## 16. Environment & Konfigurasi

### 16.1 File `.env.example`

```bash
# ── Server ───────────────────────────────────────────────────────────────────
APP_HOST=0.0.0.0
APP_PORT=8000
APP_ENV=development          # development | production

# ── LM Studio ────────────────────────────────────────────────────────────────
LM_STUDIO_URL=http://localhost:1234
LM_MODEL=local-model
LM_TIMEOUT_SECONDS=30

# ── Math Engine ───────────────────────────────────────────────────────────────
DEFAULT_LEVEL=3
DEFAULT_NUMBER_TYPE=natural
MAX_GENERATION_RETRIES=50    # Retry limit untuk generator
MAX_DISTRACTOR_COUNT=4
ENABLE_AI_STORY=true         # Set false untuk skip LM Studio (lebih cepat)

# ── Seed ─────────────────────────────────────────────────────────────────────
# Tidak ada konfigurasi seed — seed selalu dikirim per-request
```

### 16.2 `app/config.py`

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

## 17. Rencana Kerja (Roadmap)

### Fase 1 — Foundation & Infrastructure
**Target:** Boilerplate, seed system, level system, dan number type system berjalan.

- [ ] Init project & struktur direktori sesuai Section 5
- [ ] Setup `requirements.txt` dan virtual environment
- [ ] Implementasi `app/config.py` dan `app/exceptions.py`
- [ ] Implementasi `core/number_types/registry.py` (Enum NumberType)
- [ ] Implementasi `core/number_types/validators.py`
- [ ] Implementasi `core/levels/config.py` (LevelConfig + LEVEL_REGISTRY level 1–7)
- [ ] Implementasi `core/seed/manager.py` (SeedManager + SeedContext)
- [ ] Implementasi `core/number_types/generators.py`
- [ ] Unit test untuk seed manager (reproducibility test manual)
- [ ] `GET /health` dan `GET /levels` berfungsi

**Verifikasi Fase 1:**
```python
# Test manual reproducibility
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
assert n1 == n2, "Seed tidak bekerja!"
print(f"✅ Seed bekerja: {n1}")
```

---

### Fase 2 — Core Arithmetic (Operasi Dasar)
**Target:** Operasi addition, subtraction, multiplication, division siap untuk semua NumberType.

- [ ] `core/arithmetic/addition.py` — semua NumberType, semua level
- [ ] `core/arithmetic/subtraction.py`
- [ ] `core/arithmetic/multiplication.py`
- [ ] `core/arithmetic/division.py` (backward strategy)
- [ ] `services/blueprint.py` (format JSON blueprint)
- [ ] `services/distractor.py` (miskonsepsi dasar)
- [ ] `schemas/request.py` dan `schemas/response.py`
- [ ] `routers/arithmetic.py` — endpoint `/arithmetic/generate`
- [ ] Unit test per operasi (min. 50 kasus, pastikan hasil bersih)
- [ ] Integration test reproducibility untuk operasi dasar

---

### Fase 3 — Core Arithmetic (Operasi Lanjutan)
**Target:** Power, root, modulo, number properties, mixed operations.

- [ ] `core/arithmetic/power.py`
- [ ] `core/arithmetic/root.py` (backward strategy)
- [ ] `core/arithmetic/modulo.py`
- [ ] `core/arithmetic/number_properties.py` (FPB, KPK, faktor)
- [ ] `core/arithmetic/comparison.py`
- [ ] `core/arithmetic/mixed_operations.py` (BODMAS-aware)
- [ ] Distractor rules untuk semua operasi baru
- [ ] Test coverage ≥ 80% untuk semua file arithmetic

---

### Fase 4 — AI Storyteller Integration
**Target:** Soal cerita dihasilkan oleh LM Studio dengan fallback yang robust.

- [ ] Implementasi `services/ai_storyteller.py`
- [ ] Prompt template per domain & tema
- [ ] Fallback story generator (tanpa LM Studio)
- [ ] Integration ke arithmetic_service
- [ ] Test: storyteller aktif dan nonaktif

---

### Fase 5 — Domain Lain & Finalisasi
**Target:** Geometry, measurement, algebra, statistics, probability.

- [ ] Implementasi semua domain non-arithmetic (dengan seed & level system)
- [ ] `GET /operations/{level}` endpoint
- [ ] Finalisasi Swagger docs
- [ ] Performance test: setiap endpoint < 500ms (tanpa LM Studio)
- [ ] Load test: 50 concurrent requests tetap reproducible

---

## 18. Architecture Decision Records (ADR)

### ADR-001: Mengapa Level Berupa Integer, Bukan String?

**Keputusan:** Level menggunakan integer (1, 2, 3...) bukan string ("easy", "medium", "hard").

**Alasan:**
- Lebih granular — bisa ditambah level baru tanpa breaking change
- Mudah dipetakan ke jenjang kelas (Level 1 ≈ Kelas 1)
- Sorting dan range query lebih mudah (`level >= 3`)
- Dapat dikonfigurasi dinamis oleh admin tanpa mengubah kode

---

### ADR-002: Mengapa Seed di-hash dengan SHA-256?

**Keputusan:** Seed final = `SHA-256(f"{seed}:{operation}:{level}:{number_type}")[:8 bytes]`

**Alasan:**
- Seed yang sama dengan parameter berbeda menghasilkan RNG state yang berbeda
- Tanpa hashing: `seed=1, level=1` dan `seed=10, level=1` bisa terlalu dekat nilainya dan menghasilkan angka serupa
- SHA-256 memberikan distribusi yang merata dan bebas collision praktis

**Trade-off:** Sedikit overhead komputasi (~microseconds) — tidak signifikan.

---

### ADR-003: Mengapa Backward Generation untuk Division & Root?

**Keputusan:** Generator division dan root memilih hasil (quotient/root) terlebih dahulu, lalu menghitung mundur operandnya.

**Alasan:**
- Forward generation (pilih operand dulu) sering menghasilkan hasil "kotor" (3 ÷ 7 = 0.428...)
- Backward generation **menjamin 100%** hasil bersih tanpa retry berlebihan
- Lebih efisien: tidak perlu loop retry

**Contoh:**
```
Backward Division:
  1. Pilih quotient = 4 (random)
  2. Pilih divisor = 3 (random)
  3. Hitung dividend = 4 × 3 = 12
  4. Soal: 12 ÷ 3 = 4 ✅
```

---

### ADR-004: Mengapa NumberType Terpisah dari Level?

**Keputusan:** NumberType adalah parameter tersendiri, bukan bagian dari level.

**Alasan:**
- Fleksibilitas: guru bisa pilih "soal perkalian Level 5 dengan pecahan" secara eksplisit
- Level mengontrol **kompleksitas operasi**; NumberType mengontrol **jenis bilangan**
- Validasi tetap ada: tidak semua NumberType tersedia di semua level (via `allowed_number_types`)

---

### ADR-005: Mengapa `fractions.Fraction`, Bukan `float`?

**Keputusan:** Semua operasi pecahan menggunakan `fractions.Fraction` dari stdlib Python.

**Alasan:**
```python
# Masalah float
0.1 + 0.2 == 0.30000000000000004  # ← TIDAK BISA untuk soal

# Solusi Fraction
Fraction('1/10') + Fraction('2/10') == Fraction(3, 10)  # ← Tepat ✅
str(Fraction(3, 10))  # → "3/10"
```

**Trade-off:** Sedikit lebih lambat dari float — tidak signifikan untuk use case ini.

---

### ADR-006: Mengapa Hasil Selalu Disimpan sebagai String di JSON?

**Keputusan:** Field `result`, `operands`, dan `variables[].value` selalu berupa string dalam response JSON.

**Alasan:**
- JSON tidak memiliki tipe `Fraction`
- Menggunakan float `0.75` menghilangkan informasi pedagogis pecahan `3/4`
- String memungkinkan representasi: integer `"12"`, pecahan `"3/4"`, campuran `"1 3/4"`, desimal `"3.14"`
- Frontend bisa parse sesuai kebutuhan tampilan

---

*Dokumen ini adalah living document. Update setiap kali ada perubahan arsitektur atau keputusan desain baru.*

*Last updated: v2.0.0 — Tambahan: Seed System, Level Integer, Number Type Registry, Restruktur Arithmetic*
