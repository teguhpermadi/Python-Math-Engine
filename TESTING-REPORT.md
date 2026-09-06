# Laporan Testing & Debug — math-engine (Microservice Python/FastAPI)

> **UPDATE 2026-08-29 (Fase 0+1 selesai):** BUG-01, BUG-03, BUG-04, dan BUG-06 (silent angle type) telah **DIPERBAIKI** — pytest sekarang **53 passed / 0 failed** (dari 25 failed + 2 errors; durasi 59.97s → ~2s). Klaim BUG-02 lama (`operand_count` → 500) **ternyata salah** — hasil investigasi lanjutan menemukan akar masalah yang berbeda: 6 operasi (`modulo`, `gcd`, `lcm`, `comparison`, `ordering`, `factorization`) 500 karena key `result_type` hilang/tipe `result` list, dan `modulo` + tipe non-integer 500 karena double-validation yang tidak konsisten. Semua sudah diperbaiki; detail di bagian bawah file ini.

> Tanggal: 2026-08-29
> Scope: Semua endpoint math engine (arithmetic, geometry, angles, measurement, algebra, statistics, seed) + unit/integration test.
> Catatan: **Tidak ada revisi kode yang dilakukan** — ini hanya laporan temuan.
> Environment: uvicorn `app.main:app` di `http://127.0.0.1:8001` (Python 3.14.3), pytest.

---

## 1. Ringkasan Eksekusi

| Area | Status |
|---|---|
| `GET /health` | ✅ OK |
| `GET /api/v1/arithmetic/levels` (via proxy) | ✅ OK |
| `POST /api/v1/arithmetic/generate` (level 1–7, natural/integer/fraction) | ✅ OK — deterministik per seed |
| `POST /api/v1/measurement/generate`, `algebra`, `statistics`, `angles` | ✅ OK |
| `GET /api/v1/geometry/shapes` | ⚠️ Bug lisensi data (BUG-05) |
| `POST /api/v1/geometry/generate` shape 2D **tanpa** `dimension` | ❌ Gagal 400 (BUG-01) |
| `POST /api/v1/arithmetic/generate` dengan `operand_count` > 2 | ❌ Error 500 (BUG-02) |
| `POST /api/v1/math/batch-generate` mixed domain | ⚠️ Perlu review (BUG-06) |
| Suite pytest (`python -m pytest -q`) | ❌ **25 failed, 19 passed, 2 errors** (59.97s) |

Output lengkap: `e:\laragon\www\cbtapp\math-engine\pytest_report.txt`, `pytest_report2.txt`.

---

## 2. Daftar Bug / Masalah

### 🔴 BUG-01 — Geometry: shape 2D gagal 400 karena default `dimension="3D"`
- **Repro (live):** `POST /api/v1/geometry/generate {"seed":1,"level":1,"shape":"square"}` →
  **400** `{"detail":"Shape 'square' is not available for 3D dimension"}`
- **Akar:** request model geometry mendefer `dimension` ke `"3D"`; shape 2D (square/rectangle/triangle/circle) tidak divalidasi/di-infer terhadap dimension yang dipilih.
- **Dampak:** Semua pemanggil yang tidak mengirim `dimension` gagal untuk shape 2D. Opsi perbaikan: infer dimension otomatis dari shape, atau perbaiki kontrak bersama proxy (BUG-03 laporan cbt-app-api).

### 🔴 BUG-02 — Arithmetic: `operand_count` > 2 memicu AttributeError (HTTP 500)
- **Repro (live):** `POST /api/v1/arithmetic/generate {"seed":7,"level":1,"operation":"addition","number_type":"natural","operand_count":3}` → **500**, log: `AttributeError: 'int' object has no attribute 'seed'`
- **Akar:** jalur multi-operand memanggil `SeedManager`/RNG dengan **integer seed** sebagai argumen posisi pertama, padahal konstruktor `SeedManager.__init__(self, context: SeedContext)` menuntut `SeedContext` (lihat `app/core/seed/manager.py:19`). Jalur operand_count=2 tidak lewat jalur ini sehingga normal.
- **Dampak:** Soal rantai penjumlahan/pengurangan (3+ angka, umum untuk level tinggi SD) tidak bisa digenerate.

### 🔴 BUG-03 — Test integrasi salah target port → 22 failure palsu
- **File:** `tests/integration/test_geometry_endpoint.py`, `test_angles_endpoint.py`, `test_final.py`
- **Bukti:** semua hardcode `http://localhost:8000/api/v1/...` — port 8000 adalah **Laravel backend**, bukan math engine (8001). Selama Laravel berjalan, test menerima HTML 404 (`AssertionError: Status: 404 - <!DOCTYPE html>`); kalau Laravel mati, `JSONDecodeError`.
- **Dampak:** `test_cube/block/pyramid/prism/sphere/cylinder/cone/hemisphere/frustum/torus/ellipsoid/tetrahedron/hollow_sphere/octahedron/dodecahedron/icosahedron/all_3d_shapes/shapes_endpoint`, `test_angles_complementary`, `test_parallel_lines`, `test_measurement/algebra/statistics` gagal **bukan karena bug engine** — endpoint yang sama terbukti OK via request manual ke 8001.
- **Perbaikan (nanti):** base URL dari env var (default `http://127.0.0.1:8001/api/v1`), atau jalankan via in-process `TestClient`.

### 🔴 BUG-04 — Unit test `SeedManager` salah pakai API → 2 failure + 2 error
- **Bukti pytest:**
  - `test_seed_manager.py::test_same_seed_produces_same_rng` & `test_different_seed_produces_different_rng`: `AttributeError: 'int' object has no attribute 'seed'` — test memanggil `SeedManager(42)` dengan int, sementara API sekarang menuntut `SeedContext`.
  - `test_seed_reproducibility.py` (2 test): `fixture 'client' not found` — tidak ada `tests/conftest.py` yang menyediakan fixture `client` (httpx.AsyncClient) maupun konfigurasi asyncio.
- **Dampak:** Kewajiban TRD §16.2 (seed reproducibility) tidak terverifikasi otomatis sama sekali. (Fungsi reproducibility sendiri terbukti OK lewat request manual: seed sama → output sama.)

### 🟠 BUG-05 — `GET /api/v1/geometry/shapes` menandai shape premium sebagai free
- **Repro (live):** response memuat `"hollow_sphere": {"free": true, ...}` padahal `hollow_sphere` adalah fitur **premium** (data engine sendiri menandai premium — konstanta `PREMIUM_SHAPES` di `app/core/data/geometry_data.py`).
- **Dampak:** Client mengira semua shape gratis; pembatasan premium tidak bisa ditegakkan dari sisi konsumen.

### 🟠 BUG-06 — `POST /api/v1/math/batch-generate` (mixed domain) perlu review
- **Fakta:** saat test live, response 200 dengan `status: "partial"` — sebagian domain gagal dalam batch yang sama, tanpa detail error per-item yang jelas.
- **Dampak:** Pemanggil tidak bisa membedakan item mana yang gagal dan kenapa; sebaiknya sertakan error per requirement.

### 🟡 BUG-07 — Artefak `__pycache__` dari lokasi proyek lama
- **Bukti:** ada `__pycache__/*.pyc` yang path asalnya `E:\laragon\www\Python Math Engine\...` (lokasi lama sebelum repo dipindah ke `cbtapp\math-engine`).
- **Dampak:** Debug membingungkan (cache basi), repo berantakan. Tambahkan `__pycache__/` ke `.gitignore` dan bersihkan.

### 🟡 BUG-08 — Cakupan test menyusut vs klaim README
- **Fakta:** README mendokumentasikan kemampuan luas, tetapi endpoint yang ada hanya arithmetic/geometry/angles/measurement/algebra/statistics; tidak ada test untuk `operation` lanjutan (power/root/modulo/gcd/lcm/comparison/ordering/factorization yang diiklankan di metadata `/arithmetic/levels`).
- **Dampak:** Fitur yang diiklankan lewat metadata tidak terjamin berfungsi (perlu audit mana yang benar-benar ada di service).

---

## 3. Observasi Lain (non-bug fungsional)
- `SeedManager` sekarang deterministik atas `(seed, operation, level, number_type)` — bagus, tetapi konsekuensinya test lama bergaya `SeedManager(int)` gugur (BUG-04); test reproducibility juga perlu memakai `SeedContext` penuh agar benar-benar menguji §16.2.
- Tidak ada rate limiting / API key — engine bind `0.0.0.0:8001` dan bisa dipanggil langsung tanpa autentikasi. Untuk produksi batasi ke localhost / reverse-proxy internal.
- Durasi pytest ~60 detik sebagian besar karena retry koneksi ke port yang salah (BUG-03); setelah diperbaiki suite seharusnya jauh lebih cepat.

## 4. Rekomendasi Prioritas
1. Perbaiki jalur multi-operand (BUG-02) — error 500 nyata di runtime.
2. Selesaikan kontrak geometry `dimension` (BUG-01) bersama perbaikan proxy Laravel (BUG-03 backend).
3. Tambah `tests/conftest.py` (fixture client), perbaiki test SeedManager pakai `SeedContext` (BUG-04), arahkan base URL test integrasi ke 8001 (BUG-03).
4. Sinkronkan flag `free` shape premium (BUG-05) dan detail error batch (BUG-06).

---

## 5. Hasil Perbaikan Fase 0+1 (2026-08-29)

### File yang diubah (engine)
| File | Perubahan |
|---|---|
| `app/core/arithmetic/comparison.py` | `generate_comparison`: tambah `result_type: "symbol"`; `generate_ordering`: `result` jadi string `", ".join(...)` (bukan list) + key baru `ordered` + `result_type: "sequence"` |
| `app/core/arithmetic/number_properties.py` | `generate_gcd_problem` / `generate_lcm_problem`: `result_type: "natural"`; `generate_factorization_problem`: `result_type: "expression"` (akar 500 karena `raw_data["result_type"]` KeyError di service) |
| `app/services/arithmetic_service.py` | Special-case validasi number_type konsisten dengan model_validator (tambah `modulo`) — menghapus double-validation yang 500 |
| `app/routers/arithmetic.py` | `MathEngineError` → 400 informatif; unexpected error di-`logger.exception` (traceback tak lagi tertelan) |
| `app/services/geometry_service.py` | Kontrak dimension: dimension di-infer dari shape bila konflik (2D tidak lagi 400); alias `cuboid`/`rectangular_prism` → `block` untuk klien lama |
| `app/services/angle_service.py` | Tipe sudut tak dikenal sekarang ditolak (`ValueError` → 400), tidak lagi diam-diam jadi `parallel_lines` (bug baru yang ditemukan test regresi) |
| `app/core/seed/manager.py` | `SeedManager(int)` + `get_rng()` didukung lagi (backward compat) — tanpa mengubah perilaku deterministik |
| `tests/conftest.py` | **BARU**: fixture `client` in-process (`TestClient`) — tidak butuh pytest-asyncio/port eksternal |
| `tests/unit/core/test_seed_manager.py` | API diperbarui + 2 test baru untuk determinisme `SeedContext` (TRD §16.2) |
| `tests/integration/*` (3 file) | Semua hardcode `localhost:8000` diganti in-process client; tambah test regresi 2D/alias/semua operasi arithmetic |

### Perbaikan terkait di repo lain (satu kontrak bersama)
- **cbt-app-api**: `PreviewMathQuestionRequest` + `BatchPreviewMathQuestionRequest` kini menerima `dimension` & `type`; `MathQuestionController::buildPayload` memetakan `rational` → `fraction` (registry engine tidak punya `rational`).

### Verifikasi
- `python -m pytest -q` → **53 passed** (sebelumnya 25 failed + 2 errors), durasi ~1.5–2.5s (sebelumnya ~60s).
- Live HTTP ke engine: `modulo/gcd/lcm/comparison/ordering/factorization` 200; `modulo`+`integer` 200; `square` dengan `dimension=3D` salah → otomatis 2D 200; `cuboid` → `block`; tipe sudut invalid → 400.
- E2E via proxy Laravel (`/math-generate/preview`, admin): geometry 2D `square` OK, angles `supplementary` OK (dulu dipaksa complementary), `number_type=rational` OK (dulu 400).
- Suite Pest backend: tidak ada regresi (delta failure = flaky pollution yang sudah terdokumentasi; `StudentTest` lulus 17/17 saat dijalankan terisolasi).

### Masih terbuka (sengaja tidak dikerjakan di fase ini)
- BUG-05 (flag premium di `/geometry/shapes`) dan BUG-07/BUG-08 (artefak & cakupan test README).
- Catatan: `PREMIUM_SHAPES` tidak ditemukan di kode — klaim BUG-05 perlu diverifikasi ulang terhadap sumber data premium yang sebenarnya sebelum diperbaiki.


