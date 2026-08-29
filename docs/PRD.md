# Product Requirements Document (PRD)

## Python Math Engine — Deterministic Maths Microservice untuk CBT

> **Versi:** 1.0.0 | **Status:** Draft | **Tanggal:** 29 Agt 2026
> **Repo:** github.com/teguhpermadi/Python-Math-Engine (branch `main`, commit `ebbe7b7`)

---

## Daftar Isi

1. [Ringkasan Produk](#1-ringkasan-produk)
2. [Tujuan & Sasaran](#2-tujuan--sasaran-produk)
3. [Persona & Pengguna](#3-persona--pengguna)
4. [Arsitektur Sistem](#4-arsitektur-sistem)
5. [Teknologi & Dependensi](#5-teknologi--dependensi)
6. [Struktur Direktori](#6-struktur-direktori)
7. [Konsep Inti](#7-konsep-inti)
8. [Fungsionalitas (FR)](#8-fungsionalitas-functional-requirements)
9. [Workflow Proses](#9-workflow-proses)
10. [Antarmuka API](#10-antarmuka-api-api-specification)
11. [Data Contract / Skema](#11-data-contract--skema-respons)
12. [Persyaratan Non-Fungsional](#12-persyaratan-non-fungsional)
13. [Penanganan Error](#13-strategi-penanganan-error)
14. [Strategi Pengujian](#14-strategi-pengujian)
15. [Konteks & Roadmap](#15-konteks-pengembangan--roadmap)
16. [Batasan Produk](#16-batasan-constraints--batas-produk)

---

## 1. Ringkasan Produk

**Python Math Engine** adalah **mikroservis REST API** sebagai *backend matematika deterministik* untuk aplikasi **CBT (Computer-Based Test / Ujian Berbasis Komputer)** dan platform latihan soal. Sistem ini menghasilkan soal matematika yang **reproducible** (seed sama → soal sama), terstruktur per level, dan mendukung berbagai tipe bilangan serta domain matematika.

### 1.1 Tanggung Jawab Utama

| Tanggung Jawab | Deskripsi |
|---|---|
| **Seed-Based Generation** | Seed + parameter sama → soal identik |
| **Level-Based Difficulty** | Kesulitan bilangan bulat (Level 1–7) |
| **Multi-Domain** | Aritmatika, Geometri (2D/3D), Pengukuran, Aljabar, Statistik, Sudut |
| **Number Type System** | Natural, whole, integer, desimal, pecahan, dll. |
| **Precision Arithmetic** | `Fraction` & `Decimal`, bebas floating-point errors |
| **Blueprint Logic** | Urutan langkah operasi sebagai kunci jawaban drag-and-drop |
| **Distractor Logic** | Opsi salah berdasar miskonsepsi siswa per operasi |
| **AI Contextualization** | Soal cerita via LM Studio lokal (OpenAI-compatible) |
| **Visualization-Ready** | Data mesh 3D & koordinat 2D untuk renderer (Three.js / R3F) |

### 1.2 Ringkasan Singkat

- **Jenis:** Mikroservis backend (API-only, tanpa UI/rendering).
- **Framework:** FastAPI (Python 3.11+). **Versi terpasang:** `2.0.0`.
- **Pre-render:** mengembalikan data mentah (mesh, koordinat, LaTeX) untuk frontend.
- **Stateless:** setiap permintaan berdiri sendiri; tidak menyimpan ke database.

---

## 2. Tujuan & Sasaran

### 2.1 Tujuan Produk

1. Generator soal **konsisten & adil** untuk ujian CBT (variasi via seed, setara level).
2. **Reproducibility** untuk verifikasi, audit, dan variasi terkendali.
3. Mesin inti **independen dari tampilan**, dipakai ulang oleh berbagai frontend.
4. Soal berbasis **miskonsepsi (distractor)** agar penilaian lebih bermakna.

### 2.2 Sasaran Pengukuran (Goals)

| ID | Sasaran | Ukuran Keberhasilan |
|---|---|---|
| G1 | Semua domain inti menghasilkan soal valid | `/generate` mengembalikan `200` pada param valid |
| G2 | Reproducibility mutlak | Panggilan berulang (seed & param sama) → payload identik |
| G3 | Cakupan tipe bilangan | ≥ 10 tipe bilangan didukung & tervalidasi |
| G4 | Cakupan bentuk geometri | ≥ 40 ragam bentuk 2D & 3D |
| G5 | Kualitas distractor | Distractor per 6 domain spesifik |

---

## 3. Persona & Pengguna

| Persona | Deskripsi | Kebutuhan |
|---|---|---|
| **Frontend Developer** | Membangun UI latihan/ujian (React) | API stabil, data siap-render (mesh, LaTeX, koordinat) |
| **Guru / Penyusun Soal** | Menyusun paket ujian | Paket campuran multi-domain, kontrol level |
| **Siswa** | Mengerjakan soal | Soal bervariasi, distractor masuk akal, soal cerita |
| **Tim QA** | Memvalidasi kebenaran | Reproducibility, test suite formal, dokumentasi |

> **Catatan:** Produk tidak menangani sesi siswa, penyimpanan hasil, maupun autentikasi — mesin generasi murni.

---

## 4. Arsitektur Sistem

```
   Frontend (React / R3F)
         │  HTTP (JSON)
         ▼
   Router (app/routers)  ──►  Schemas (Pydantic validasi)
         │
         ▼
   Services (app/services) ─ blueprint • distractor • ai_storyteller • net
         │
         ▼
   Core (app/core) ─ aritm • geom • aljabar • pengukuran • statistik • seed • levels • number_types
```

### 4.1 Alur Data Permintaan-Respons

1. **Router** menerima HTTP request & memvalidasi via **Schema (Pydantic)**.
2. Router memanggil **Service** terkait.
3. **Service** membentuk `SeedContext` → `SeedManager` (RNG deterministik) → `LevelConfig`.
4. Service memanggil **Core generator** → data soal mentah (operand, ekspresi, dimensi, hasil).
5. Service membangun **Blueprint**, **variabel**, **distractor**, opsional **soal cerita (AI)**.
6. Service menyusun **response** terstruktur & mengembalikannya via router.
7. **Error handler** mengubah `MathEngineError` menjadi respons JSON standar.

---

## 5. Teknologi & Dependensi

Dari `requirements.txt`:

| Library | Versi | Fungsi |
|---|---|---|
| fastapi[standard] | 0.111.0 | Framework web & ASGI |
| uvicorn[standard] | 0.29.0 | Server ASGI |
| pydantic | 2.7.0 | Validasi model & schemas |
| pydantic-settings | 2.2.1 | Konfigurasi env |
| sympy | 1.12 | Bilangan prima, simbolik |
| numpy | 1.26.4 | Komputasi numerik |
| python-dotenv | 1.0.1 | Baca file `.env` |
| httpx | 0.27.0 | HTTP client async (LM Studio) |

**Tooling (requirements-dev):** `pytest` (suite formal), `TestClient`.

---
---

## 6. Struktur Direktori

Struktur sumber kode (tanpa `node_modules`, `.git`, `__pycache__`, `.pytest_cache`):

```
math-engine/
├── app/
│   ├── main.py                    # FastAPI app, CORS, error handler, mount router
│   ├── config.py                  # Settings (env-based)
│   ├── exceptions.py              # MathEngineError + subclass
│   ├── core/
│   │   ├── arithmetic/            # addition, subtraction, multiplication, division,
│   │   │                         # power, root, modulo, comparison, mixed_operations,
│   │   │                         # number_properties, utils
│   │   ├── algebra/linear.py      # persamaan linear ax + b = c
│   │   ├── geometry/              # angles, lines, mesh, shapes, voxel
│   │   ├── levels/config.py       # LEVEL_REGISTRY (1–7)
│   │   ├── measurement/           # generator, units
│   │   ├── number_types/          # registry, generators, validators
│   │   ├── seed/manager.py        # SeedManager & SeedContext
│   │   └── statistics/calculators.py
│   ├── routers/                   # arithmetic, geometry, measurement, algebra,
│   │                             # statistics, angles, exam
│   ├── schemas/                   # request.py, response.py
│   └── services/                  # *service.py, blueprint, distractor,
│                                 # ai_storyteller, net_service
├── tests/
│   ├── test_api.py                # smoke test API
│   ├── integration/               # endpoint tests (angles, geometry, seed, final)
│   └── unit/                      # core & service unit tests
├── verify_*.py                    # verifikasi mandiri (advanced, arithmetic, core, latex)
├── docs/                          # folder dokumentasi (PRD ini)
├── python-math-engine-TRD-*.md    # dokumen TRD v2 / v2.1
├── geometry_interactive_analysis.md
├── requirements.txt / requirements-dev.txt
├── .env / .env.example
└── README.md
```

---

## 7. Konsep Inti (Core Concepts)

Tiga pilar utama sistem generasi soal.

### 7.1 Level (Parameter Kesulitan)

`LevelConfig` membundel konfigurasi per level (immutable, `frozen=True`):

- Rentang nilai integer (`min_value`–`max_value`)
- Rentang desimal & jumlah desimal (`min_decimal`–`max_decimal`, `decimal_places`)
- Penyebut pecahan yang diizinkan (`allowed_denominators`), maks bagian bulat campuran
- Maks operasi campuran (`max_operations`), izin tanda kurung (`allow_parentheses`)
- Eksponen & jenis akar (`max_exponent`, `allowed_roots`)
- **Tipe bilangan yang diizinkan** (`allowed_number_types`)
- Sub-tipe untuk `REAL` (`real_sub_types`)

Ringkasan 7 level:

| Level | Rentang Integer | Desimal | Pkebilangan | Operasi Maks | Kurung |
|---|---|---|---|---|---|
| 1 | 1–10 | – | natural, whole | 1 | ✗ |
| 2 | 1–50 | – | + prime | 1 | ✗ |
| 3 | 1–100 | 0.1–9.9 | + decimal, fraction | 2 | ✗ |
| 4 | 1–500 | 0.01–99.99 | + integer, integer_neg, mixed_fraction, composite | 2 | ✓ |
| 5 | 1–1000 | 0.001–999.999 | + real | 3 | ✓ |
| 6 | 1–10k | 0.0001–9999.9999 | real, integer_neg | 4 | ✓ |
| 7 | 1–100k | 0.00001–99999.99999 | real, integer_neg | 5 | ✓ |

### 7.2 Number Type (Tipe Bilangan)

Didefinisikan di `app/core/number_types/registry.py` (enum `NumberType`):

- Berbasis himpunan: `natural`, `whole`, `integer`, `integer_pos`, `integer_neg`, `real`
- Berbasis sifat: `prime`, `composite`
- Berbasis representasi: `decimal`, `fraction`, `mixed_fraction`

Generator di `generators.py` menghasilkan bilangan sesuai tipe & level. Validator di `validators.py` (mis. `classify_number`, `is_prime`, `is_mixed_fraction`).

### 7.3 Seed-Based Generation (Determinisme)

`SeedManager` membungkus `random.Random`:

- `SeedContext`: `{seed, operation, level, number_type}` — konteks pembentuk seed unik.
- Seed deterministik dihitung dengan **SHA-256** dari string `seed:operation:level:number_type`, diambil 8 byte pertama sebagai integer.
- Semua generator (core, distractor, story) memakai RNG ber-seed yang sama → **reproducible**.

---

## 8. Fungsionalitas (Functional Requirements)

### FR-01 — Aritmatika (Arithmetic)
Generate soal operasi aritmatika deterministik.

- **Operasi:** `addition`, `subtraction`, `multiplication`, `division`, `power`, `root`, `modulo`, `gcd`, `lcm`, `factorization`, `comparison`, `ordering`, `mixed`.
- Input: `seed`, `level` (1–7), `operation`, `number_type`, `operand_count` (2–6), `allowed_operations`, `with_story`, `with_distractors`, `distractor_count`, `theme`.
- Output: ekspresi, LaTeX, variabel, blueprint, pilihan jawaban, jawaban benar, tipe jawaban.
- Validasi: `number_type` harus valid di level (kecuali `gcd`/`lcm`/`modulo`/`factorization`).

### FR-02 — Geometri (Geometry)
Generate soal geometri 2D & 3D beserta data mesh untuk rendering.

- **2D:** square, rectangle, circle, ellipse, triangle & varian (right/equilateral/isosceles/scalene/acute/obtuse), parallelogram, trapezoid (right/isosceles), kite, rhombus, pentagon, hexagon, octagon.
- **3D:** cube, block, pyramid, prism, sphere, cylinder, cone, hemisphere, frustum, torus, ellipsoid, tetrahedron, hollow_sphere, octahedron, dodecahedron, icosahedron, triangular/parallelogram/trapezoidal/rhombus/kite prism, rectangular/right_triangular pyramid, dan **voxel_group**.
- `GET /shapes` mencantumkan semua bentuk per dimensi.
- Data respons: `mesh` (vertices+faces), `dimensions`, `perimeter`, `angles`, `area`, `volume`; untuk `voxel_group` juga `voxels` + `multiview_challenge` (4 opsi sudut pandang A–D).
- Bentuk dipilih otomatis (berdasar level/dimensi) atau via parameter `shape`/`sides`. Ketidakcocokan `shape` vs `dimension` ditolak.

### FR-03 — Jaring-jaring Bangun Ruang (Net Generator)
Generate pola jaring-jaring **valid** & **invalid** untuk latihan SD.

- **Bangun:** `cube` (11 pola valid), `block`, `triangular_prism`, `rectangular_pyramid`, `cylinder`, `cone`.
- `POST /nets/generate` menerima `shape`, `seed`, `is_valid`; output `shape`, `name_id`, `is_valid`, `pattern_name`, `grid_size`, `faces`, `error_reason`.
- `GET /nets/shapes` mencantumkan bangun yang didukung.

### FR-04 — Pengukuran (Measurement)
Generate soal konversi satuan (panjang km–mm, massa kg–mg, waktu jam/menit/detik).

- Tabel konversi metrik; konversi via satuan dasar.
- Input: `seed`, `level`, `with_story`, `with_distractors`, `distractor_count`.
- Output: ekspresi konversi, hasil, pilihan jawaban, detail satuan.

### FR-05 — Aljabar (Algebra)
Generate soal persamaan linear satu variabel `ax + b = c`.

- Nilai `x` dibuat dulu agar hasil selalu bulat; `a = 1..(level+2)`, `b = 0..(level*10)`.
- Input: `seed`, `level`, `with_distractors`, `distractor_count`.
- Output: ekspresi, blueprint langkah, jawaban benar, pilihan jawaban.

### FR-06 — Statistik (Statistics)
Generate soal menghitung ukuran pemusatan data.

- Membangun dataset acak (`5` s/d `10 + level` nilai); menghitung **mean**, **median**, **mode**.
- Target pertanyaan dipilih acak di antara ketiganya.
- Input: `seed`, `level`, `with_distractors`, `distractor_count`.
- Output: dataset, ekspresi, hasil-hasil (mean/median/mode), jawaban benar, pilihan jawaban.

### FR-07 — Sudut & Garis (Lines & Angles)
Generate soal sudut penyiku, pelurus, dan hubungan sudut pada garis sejajar.

- **Jenis:** `complementary` (x + y = 90°), `supplementary` (x + y = 180°), `parallel_lines` (level ≥ 4; sehadap, dalam/luar berseberangan, dalam sepihak).
- Output mencakup `drawing_data` (koordinat gambar 2D), ekspresi, jawaban, pilihan.

### FR-08 — Generasi Paket Ujian (Exam)
Generate paket soal campuran antar-domain dalam satu permintaan.

- Input: `master_seed` + `requirements[]` (objek berisi `domain`, `level`, dan parameter domain-spesifik seperti `operation`, `shape`, `number_type`, `with_story`, `dimension`).
- **Sub-seed deterministik** per soal: `sha256("{master_seed}:{index}:{domain}") mod 10^9`.
- Output: `master_seed`, `total_questions`, daftar `questions` dengan `id`, `domain`, `content`.
- Domain didukung: `arithmetic`, `geometry`, `measurement`, `algebra`, `statistics`, `angles`.

### FR-09 — AI Storyteller (Soal Cerita)
Generate soal cerita kontekstual via LM Studio (OpenAI-compatible).

- Jika `with_story=True`, service memanggil LM Studio (`/chat/completions`) dengan prompt bahasa Indonesia bertema.
- Jika AI gagal/tidak tersedia, digunakan **fallback template** tema (buah, luar angkasa, sekolah, general) berbasis RNG.
- Konfigurasi: `LM_STUDIO_URL`, `LM_TIMEOUT_SECONDS`, `ENABLE_AI_STORY`.

### FR-10 — Distractor (Opsi Jawaban Salah)
Generate pilihan salah masuk akal berdasar **domain**:

- **arithmetic:** off-by-one, ±0.1, manipulasi pembilang/penyebut.
- **geometry:** luas vs keliling, radius vs diameter, kuadrat vs kubus, ×1.5.
- **algebra:** tanda salah, off-by-one, lupa membagi koefisien.
- **angles:** tertukar komplementer↔supplementer, offset ±5/±10.
- **measurement:** konversi terbalik, faktor-10/100, nilai asli.
- **statistics:** tertukar mean↔median/mode, pembulatan salah.

Distractor diacak deterministik & dijamin **tidak memuat jawaban benar**.

### FR-11 — Blueprint (Kunci Jawaban Drag-and-Drop)
Konversi data soal menjadi urutan langkah untuk mode jawaban drag-and-drop.

- `BlueprintStep`: `step`, `op`, `op_symbol`, `inputs`, `correct_result`, `result_type`, `hint`.
- Simbol operasi: `+`, `-`, `×`, `÷`, `mod`, `^`, `√`.
- Mendukung multi-langkah (mis. `mixed_operations`) jika core menyediakan `steps`.

### FR-12 — Endpoint Utilitas & Health
- `GET /` — status/layanan (`status: online`, versi).
- `GET /health` — health check sederhana (`status: ok`).

---

## 9. Workflow Proses

### 9.1 Workflow Generasi Soal Tunggal (mis. Aritmatika)

```
Klien klaim seed & parameter (level, number_type, operation)
        │
        ▼
┌─ POST /api/v1/arithmetic/generate
│  Router validasi schema (ArithmeticRequest)
│        │
│        ▼
│  Service: build SeedContext(seed, operation, level, number_type)
│       → SeedManager → rng deterministik (SHA-256)
│       → get_level_config(level)
│       → validasi number_type vs level
│        │
│        ▼
│  Core generator (addition/subtraction/...) → raw_data
│        │
│        ▼
│  build_blueprint(raw) + build_variables(raw)
│        │
│        ▼
│  Distractor (opsional) → rng.shuffle(choices)
│        │
│        ▼
│  AI Storyteller (opsional, with_story=True) → story / fallback
│        │
│        ▼
│  Susun ArithmeticResponse → kirim balik
└─────────────────────────────────────────────▶ JSON 200
```

### 9.2 Workflow Generasi Paket Ujian (Exam)

```
POST /api/v1/exam/generate { master_seed, requirements[] }
        │
        ▼
Loop tiap requirement i (0..n-1):
  │  sub_seed = sha256(f"{master_seed}:{i}:{domain}") % 10^9
  │
  ├─ domain=arithmetic → generate_arithmetic_question(sub_seed, ...)
  ├─ domain=geometry   → generate_geometry_question(...)
  ├─ domain=measurement→ generate_measurement_question(...)
  ├─ domain=algebra    → generate_algebra_question(...)
  ├─ domain=statistics → generate_statistics_question(...)
  └─ domain=angles     → generate_angle_question(...)
        │
        ▼
Gabungkan → { master_seed, total_questions, questions[] } → JSON 200
```

### 9.3 Workflow AI Storyteller (dengan dengan/ tanpa AI)

```
with_story=True → Service panggil ai_storyteller.generate_story(...)
        │
        ├─ LM Studio tersedia → OpenAI chat → teks soal cerita
        └─ Gagal / timeout → _generate_fallback_story(template tema, RNG)
```

### 9.4 Workflow Jaring-jaring Bangun Ruang

```
POST /api/v1/geometry/nets/generate { shape, seed, is_valid }
        │
        ▼
random.Random(seed) → pola sesuai is_valid
        │
        ├─ is_valid=True  → pilih pola benar (mis. 11 pola kubus)
        └─ is_valid=False → pola salah + error_reason (penjelasan pedagogis)
        │
        ▼
Susun faces (koordinat, warna, label) → JSON 200
```

### 9.5 Workflow Voxel Group (Geometri 3D Modular)

```
shape=voxel_group → create_voxel_group_data(rng, jml, warna)
        │  (mulai di grid 8x8x8, tumbuh terhubung acak)
        ▼
generate_voxel_group_mesh → vertices+faces (center bounding-box)
        │
        ▼
generate_voxel_group_options → 4 opsi sudut pandang (A–D):
        │   1 benar, 1 warna diacak, 2 bentuk lain
        ▼
Susun data voxels + multiview_challenge → JSON 200
```

---

## 10. Antarmuka API (API Specification)

Semua endpoint berada di bawah prefix `/api/v1`. Dokumentasi interaktif di `http://localhost:8000/docs` (Swagger UI).

### 10.1 Daftar Endpoint

| Metode | Path | Deskripsi |
|---|---|---|
| GET | `/` | Status root aplikasi |
| GET | `/health` | Health check |
| POST | `/arithmetic/generate` | Generate soal aritmatika (FR-01) |
| GET | `/arithmetic/levels/{level}` | Info konfigurasi level aritmatika |
| GET | `/geometry/shapes` | Daftar bentuk 2D/3D (FR-02) |
| POST | `/geometry/generate` | Generate soal geometri (FR-02) |
| GET | `/geometry/nets/shapes` | Daftar bangun yang didukung jaring-jaring (FR-03) |
| POST | `/geometry/nets/generate` | Generate jaring-jaring valid/invalid (FR-03) |
| POST | `/measurement/generate` | Generate soal konversi satuan (FR-04) |
| POST | `/algebra/generate` | Generate soal aljabar (FR-05) |
| POST | `/statistics/generate` | Generate soal statistik (FR-06) |
| POST | `/angles/generate` | Generate soal sudut & garis (FR-07) |
| POST | `/exam/generate` | Generate paket ujian campuran (FR-08) |

### 10.2 Metode Panggilan

#### Server

```bash
fastapi dev app/main.py        # atau: uvicorn app.main:app --reload
```

#### Contoh: Aritmatika

```bash
curl -X POST http://localhost:8000/api/v1/arithmetic/generate \
  -H "Content-Type: application/json" \
  -d '{"seed": 42, "level": 1, "operation": "addition", "number_type": "natural"}'
```

#### Contoh: Paket Ujian

```bash
curl -X POST http://localhost:8000/api/v1/exam/generate \
  -H "Content-Type: application/json" \
  -d '{"master_seed": 2024, "requirements": [
       {"domain":"arithmetic","operation":"addition","level":1},
       {"domain":"geometry","shape":"cube","level":2},
       {"domain":"algebra","level":3}
  ]}'
```

### 10.3 Ringkasan Parameter Umum

| Parameter | Tipe | Keterangan |
|---|---|---|
| `seed` / `master_seed` | int | Seed deterministik |
| `level` | int (1–7) | Tingkat kesulitan |
| `with_story` | bool | Aktifkan soal cerita AI |
| `with_distractors` | bool | Sertakan pilihan salah |
| `distractor_count` | int (2–4) | Jumlah distractor |
| `number_type` | string | Tipe bilangan (khusus aritmatika) |
| `operation` | string | Jenis operasi (khusus aritmatika) |
| `shape` / `sides` / `dimension` | — | Parameter khusus geometri |
| `type` | string | Khusus angles |
| `requirements[]` | array | Khusus exam |

### 10.4 CORS

CORS dikonfigurasi untuk mengizinkan semua origin (`*`), semua metode, semua header (untuk development). Untuk produksi, batasi origin ke domain frontend (mis. `http://localhost:5173`).

---

## 11. Data Contract / Skema Respons

### 11.1 Skema Umum (Arithmetic — formal di `schemas/response.py`)

```json
{
  "status": "success",
  "meta": {
    "seed": 42,
    "level": 1,
    "operation": "addition",
    "number_type": "natural",
    "generated_at": "2026-08-29T..."
  },
  "context": {
    "story": "Budi memiliki 5 apel, lalu ... (Opsional, null jika tanpa cerita)",
    "theme": "general"
  },
  "data": {
    "variables": [ {"id":"v1","value":"5","value_latex":"5","type":"unknown"} ],
    "expression": "5 + 3",
    "expression_latex": "5 + 3",
    "blueprint": [
      {"step":1,"op":"addition","op_symbol":"+","inputs":["v1","v2"],
       "correct_result":"8","result_type":"int","hint":null}
    ],
    "answer_choices": ["8", "6", "9", "7"],
    "answer_choices_latex": ["8", "6", "9", "7"],
    "correct_answer": "8",
    "correct_answer_latex": "8",
    "answer_type": "int"
  }
}
```

### 11.2 Skema Geometri (ilustratif)

```json
{
  "status": "success",
  "meta": { "seed": 42, "level": 3, "operation": "geometry", "shape": "cube", "dimension": "3D" },
  "context": { "story": null, "theme": "general" },
  "data": {
    "expression": "Hitung volume kubus dengan sisi 4",
    "expression_latex": "Hitung volume kubus dengan sisi 4",
    "answer_choices": ["64", "16", "48", "24"],
    "correct_answer": "64",
    "mesh": { "vertices": [...] , "faces": [...] },
    "dimensions": { "side": 4 },
    "perimeter": null,
    "angles": null,
    "area": null,
    "volume": 64.0
  }
}
```

### 11.3 Skema Paket Ujian (Exam)

```json
{
  "master_seed": 2024,
  "total_questions": 3,
  "questions": [
    { "id": 1, "domain": "arithmetic", "content": { ...payload aritmatika... } },
    { "id": 2, "domain": "geometry",   "content": { ...payload geometri... } },
    { "id": 3, "domain": "algebra",    "content": { ...payload aljabar... } }
  ]
}
```

### 11.4 Skema Jaring-jaring (Net)

```json
{
  "shape": "cube",
  "name_id": "Kubus",
  "is_valid": true,
  "pattern_name": "Pola 1-4-1 (Tipe A - Salib Standard)",
  "grid_size": { "rows": 3, "cols": 4 },
  "error_reason": null,
  "faces": [ { "id": 0, "label": "Tutup", "x": 1, "y": 0, "color": "#FF6B6B" } ]
}
```

---

## 12. Persyaratan Non-Fungsional (NFR)

| Kategori | Persyaratan |
|---|---|
| **Determinisme** | Output harus identik untuk `(seed, level, operation, number_type)` yang sama |
| **Kecepatan** | Tanpa AI, respons cepat (generasi murni dalam memori; tidak ada I/O DB) |
| **Statelessness** | Tidak ada state antar-request; cocok untuk horizontal scaling |
| **Presisi** | Penggunaan `Fraction`/`Decimal` untuk menghindari error floating-point |
| **Portabilitas** | Lintas-platform (Windows/Linux/macOS); Python 3.11+ |
| **Dokumentasi** | Swagger UI otomatis dari FastAPI (`/docs`) |
| **Konfigurasi** | Via env vars (`.env`); lihat `config.py` |
| **Keamanan** | Belum ada autentikasi/otorisasi (khusus internal/dev) |

---

## 13. Strategi Penanganan Error

### 13.1 Error Model

Basis exception: `MathEngineError` dengan atribut `message` + `error_code`. Ditangani global di `main.py` menjadi respons JSON:

```json
{ "status": "error", "error_code": "<CODE>", "message": "<pesan>" }
```

### 13.2 Daftar Kode Error (dari `app/exceptions.py`)

| Kelas | `error_code` | Konteks |
|---|---|---|
| (basis) | `INTERNAL_ERROR` | Error umum |
| `InvalidLevelError` | `INVALID_LEVEL` | Level tidak tersedia (di luar 1–7) |
| `InvalidNumberTypeForLevelError` | `INVALID_NUMBER_TYPE_FOR_LEVEL` | Tipe bilangan tak valid di level tsb |
| `InvalidOperationForLevelError` | `INVALID_OPERATION_FOR_LEVEL` | Operasi tak valid di level tsb |
| `GenerationFailedError` | `GENERATION_FAILED` | Gagal menghasilkan soal |
| `DivisionByZeroError` | `DIVISION_BY_ZERO` | Pembagian dengan nol |
| `NegativeRadicandError` | `NEGATIVE_RADICAND` | Akar dari bilangan negatif |
| `LMStudioConnectionError` | `LM_STUDIO_CONNECTION_ERROR` | Gagal terhubung LM Studio |

### 13.3 Perilaku HTTP

- Error bisnis (`MathEngineError`) → **400 Bad Request** dengan struktur di atas.
- Error validasi Pydantic → 422 (bawaan FastAPI).
- Error tak dikenal pada runtime → 500 (Internal Server Error).

---

## 14. Strategi Pengujian

### 14.1 Menjalankan Test Suite

```bash
pytest
```

### 14.2 Lingkup Tes (struktur `tests/`)

- **Unit — core (`tests/unit/core/`):**
  - `test_level_config.py` — validasi level registry.
  - `test_number_type_generators.py` — generator tipe bilangan.
  - `test_seed_manager.py` — determinisme & pembentukan seed.
- **Unit — services (`tests/unit/services/`):**
  - `test_blueprint.py` — pembangunan blueprint.
  - `test_distractor.py` — logika distractor.
  - `test_net_service.py` — generator jaring-jaring.
- **Integration (`tests/integration/`):**
  - `test_angles_endpoint.py` — endpoint sudut.
  - `test_geometry_endpoint.py` — endpoint geometri.
  - `test_seed_reproducibility.py` — konsistensi seed.
  - `test_final.py` — end-to-end akhir.
- **API smoke (`tests/test_api.py`):**
  - Aritmatika, geometri, paket ujian, nets (valid/invalid), voxel group, & reproducibility.

### 14.3 Contoh Kasus yang Diuji

1. `POST /arithmetic/generate` mengembalikan `data.expression`.
2. `POST /geometry/generate` (cube) mengembalikan `data.mesh`.
3. Reproducibility paket ujian: dua panggilan identik → payload sama persis.
4. Net valid: `is_valid=True`, `error_reason=None`, 6 faces; net invalid: `is_valid=False` + `error_reason` string.
5. Voxel group: `mesh.vertices > 0`, `voxels > 0`, `multiview_challenge` punya 4 opsi & label benar di A–D.

---

## 15. Konteks Pengembangan & Roadmap

### 15.1 Riwayat Komit (konteks pembangunan berjenjang)

1. **Aritmatika dasar** — addition, multiplication, division, mixed ops + LaTeX.
2. **Geometri 2D & 3D** — primitif & mesh utilities.
3. **Geometri API** — endpoint shape listing & generasi.
4. **19 bangun 3D baru** — cylinder, cone, sphere, ellipsoid, tetrahedron, octahedron, dodecahedron, icosahedron, + varian prisma/limas.
5. **Jaring-jaring** — valid & invalid (kubus, balok, prisma segitiga, limas segiempat, tabung, kerucut) untuk anak SD.
6. **Analisis R3F** — studi implementasi 3D React Three Fiber.
7. **Voxel group API** — generator voxel 3D modular & multiview challenge.
8. **Modul statistik, geometri, sudut, aljabar, pengukuran + router & service** (commit `ebbe7b7`, terkini).

### 15.2 Roadmap Potensial (saran lanjutan)

- Autentikasi & manajemen sesi/uji.
- Penyimpanan/audit hasil.
- Integrasi renderer frontend resmi (React Three Fiber).
- Ekspansi domain: trigonometri, probabilitas, kalkulus dasar.
- Peningkatan kualitas soal cerita (prompt tuning LM Studio).
- Pipeline CI/CD & kontainerisasi (Dockerfile pernah ada, dihapus — perlu ditinjau ulang).

---

## 16. Batasan (Constraints) & Batas Produk

### 16.1 Yang Dikerjakan (In-Scope)

- Generasi soal aritmatika, geometri (2D/3D), pengukuran, aljabar, statistik, sudut.
- Paket ujian campuran deterministik.
- Jaring-jaring bangun ruang (valid/invalid).
- Data mesh / koordinat siap-render.
- Distractor berbasis miskonsepsi.
- Soal cerita AI (dengan fallback).

### 16.2 Yang DI LUAR Cakupan (Out-of-Scope)

- ❌ Penyimpanan data / query database.
- ❌ Manajemen sesi siswa & pelaporan hasil ujian.
- ❌ Visualisasi/rendering (delegasi ke frontend).
- ❌ Autentikasi, otorisasi, user management.
- ❌ Penjadwalan ujian & throttling.

### 16.3 Batasan Teknis Saat Ini

- Penyajian soal cerita saat ini bergantung pada ketersediaan **LM Studio**; jika tidak tersedia, digunakan template fallback.
- Konfigurasi CORS terbuka (`*`) — perlu dikunci untuk produksi.
- Belum terdapat Dockerfile aktif pada commit terkini.

---

## Lampiran: Referensi File Kunci

| File | Peran |
|---|---|
| `app/main.py` | Bootstrap aplikasi, CORS, error handler, mounting routers |
| `app/config.py` | Konfigurasi env |
| `app/core/seed/manager.py` | Determinisme seed |
| `app/core/levels/config.py` | Level registry (1–7) |
| `app/core/number_types/registry.py` | Enumerasi tipe bilangan |
| `app/services/*.py` | Logika domain (arit/geom/meas/algebra/stat/angle/exam) |
| `app/services/blueprint.py` | Kunci jawaban langkah |
| `app/services/distractor.py` | Distractor per domain |
| `app/services/net_service.py` | Generator jaring-jaring |
| `app/services/ai_storyteller.py` | Soal cerita AI & fallback |
| `app/schemas/*.py` | Kontrak request/response |
| `README.md` | Petunjuk cepat instalasi & penggunaan |
| `python-math-engine-TRD-v2.1.md` | Document teknis (TRD) detail |

---

*Dokumen ini disusun berdasarkan inspeksi penuh terhadap repositori `Python-Math-Engine` (commit `ebbe7b7`) pada tanggal 29 Agustus 2026.*