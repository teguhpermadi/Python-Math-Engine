# 🐞 Laporan Bug & Temuan Testing — math-engine (Python FastAPI)

- **Tanggal testing:** 29 Agustus 2026
- **Server:** `uvicorn app.main:app --host=0.0.0.0 --port=8001` (Python 3.14.3)
- **Metode:** uji endpoint HTTP langsung (arithmetic semua operasi, geometry, measurement, algebra, statistics, angles, batch-generate), reproducibility seed, dan `python -m pytest`.
- **Hasil pytest:** `25 failed, 19 passed, 2 warnings, 2 errors in 59.97s` — detail di `pytest_report.txt` / `pytest_report2.txt`.

---

## 🔴 HIGH

### MF-1 — Geometry: shape 2D selalu gagal karena default `dimension="3D"`
**File:** `app/routers/geometry.py` (request model, default `dimension`) / service geometry

```
POST /api/v1/geometry/generate  {"seed":1,"level":1,"shape":"square"}
→ 400 {"detail":"Shape 'square' is not available for 3D dimension"}
```
Tanpa parameter `dimension`, semua shape 2D (square, rectangle, triangle, circle) ditolak. Klien yang tidak mengetahui parameter ini (termasuk proxy Laravel yang default-nya 3D) selalu gagal untuk 2D. Minimalnya kirim `dimension: "2D"` untuk shape 2D — atau (lebih baik) inferensi dimension dari daftar shape, karena `GET /geometry/shapes` sudah tahu shape mana 2D/3D.

**Bukti HTTP (semua 400 dengan pesan yang sama):** square, rectangle, triangle, circle → 400; cube/cuboid/sphere/cylinder/cone/… → 200 OK.

---

### MF-2 — Seluruh test integrasi menunjuk ke port yang salah (8000 = Laravel, bukan 8001)
**File:**
- `tests/integration/test_geometry_endpoint.py` → `BASE_URL = "http://localhost:8000/api/v1/geometry"`
- `tests/integration/test_angles_endpoint.py` → `http://localhost:8000/api/v1/angles/generate`
- `tests/integration/test_final.py` → `http://localhost:8000/api/v1/{measurement|algebra|statistics}/generate`

Port 8000 adalah server Laravel PHP (`php -S 127.0.0.1:8000`), sehingga test mendapat **halaman HTML 404** → `assert 404 == 200`, `json.decoder.JSONDecodeError`, `AssertionError: Status: 404 - <!DOCTYPE html>` (23 test gagal dengan pola ini). Test integrasi seharusnya menunjuk `http://127.0.0.1:8001` (bisa dibuat konfigurable via env, mis. `MATH_ENGINE_TEST_URL`).

---

## 🟠 MEDIUM

### MF-3 — Test unit & integrasi seed memanggil API `SeedManager` yang sudah tidak ada
**File:** `tests/unit/core/test_seed_manager.py` vs `app/core/seed/manager.py`

Test memanggil `SeedManager(42)` (int) + `sm.get_rng()`. Implementasi sekarang: `SeedManager(SeedContext(seed, operation, level, number_type))` dan hanya punya property `.rng` (tanpa `get_rng()`).
- `tests/unit/core/test_seed_manager.py::test_same_seed_produces_same_rng` & `test_different_seed_produces_different_rng` → `TypeError: 'int' object has no attribute 'seed'` (2 failure).
- `tests/integration/test_seed_reproducibility.py` memakai fixture `client: AsyncClient` yang **tidak didefinisikan manapun** (tidak ada `tests/conftest.py`; asumsinya dibuat untuk httpx ASGI in-process) → 2 ERROR `fixture 'client' not found`.

Padahal **seed reproducibility adalah requirement TRD 16.2 (MANDATORY)** — saat ini requirement wajib tersebut tidak ter-cover test sama sekali. Test perlu di-update ke API baru (`SeedContext`) dan conftest dengan fixture client (ASGITransport atau URL 8001).

---

## 🟡 LOW

### MF-4 — Parameter `angle_type` diam-diam diabaikan
**File:** `app/routers/angles.py` (`AngleRequest` hanya punya field `type`)
```
POST /api/v1/angles/generate {"seed":5,"level":2,"angle_type":"supplementary"}
→ 200 OK, meta.type = "supplementary"?? → TIDAK; hasil tetap tipe default tanpa error
```
Terbukti: mengirim `angle_type` (bukan `type`) tidak menghasilkan error maupun efek — pydantic mengabaikan field asing. Klien salah nama field mendapat soal dengan tipe yang salah secara diam-diam. Disarankan `model_config = ConfigDict(extra="forbid")` pada request model agar salah nama field = 422.

### MF-5 — Artefak `__pycache__` basi dari lokasi lama repo
`math-engine/tests/**/__pycache__` berisi bytecode dengan path sumber `E:\laragon\www\Python Math Engine\...` (folder lama). Menandakan penyalinan folder tanpa pembersihan; risiko kebingungan import/coverage. Hapus `__pycache__` dan tambahkan ke `.gitignore`.

### MF-6 — CORS: `allow_origins=["*"]` + `allow_credentials=True`
**File:** `app/main.py` baris 16–22. Kombinasi ini tidak valid per spec CORS (browser menolak kredensial pada origin wildcard). Saat ini tidak berdampak karena engine hanya dipanggil server-to-server oleh Laravel, tapi menjadi masalah jika engine pernah dipanggil langsung dari browser. Ganti dengan daftar origin eksplisit.

### MF-7 — `/api/v1/ping` tidak ada (hanya `/health`)
Tools/eksternal yang menguji `/api/v1/ping` mendapat 404. Tambahkan ping kompatibel atau dokumentasikan bahwa health-check resmi adalah `/health`.

---

## ✅ Yang teruji dan BERFUNGSI
- `GET /health` → 200 OK.
- `POST /api/v1/arithmetic/generate` — seluruh operasi (addition, subtraction, multiplication, division, power, root, modulo, gcd, lcm, mixed, comparison, ordering, factorization) OK; natural & fraction OK; level 1–7 OK.
- `measurement/generate`, `algebra/generate`, `statistics/generate`, `angles/generate` (dengan field `type` yang benar) OK.
- `POST /api/v1/batch/generate` (master_seed + multi-domain requirements) OK — 3 domain × 3 soal.
- `GET /api/v1/geometry/shapes` OK (daftar 2D/3D lengkap).
- Determinisme: seed sama → output sama (dicek via HTTP untuk arithmetic fraction & natural) — fungsional di runtime, hanya test-nya yang rusak (MF-2/MF-3).
