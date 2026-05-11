# Rencana Implementasi: Tambahan 2D Shapes

## Ringkasan
Menambahkan 15 bangun datar (2D) baru ke modul geometri, meliputi segitiga (berbagai jenis), segiempat (berbagai jenis), oval, dan poligon beraturan.

---

## 1. File: `app/core/geometry/shapes.py`

### Fungsi baru yang ditambahkan (setelah `generate_triangle`):

| Fungsi | Shape | Key Dimensions | Rumus Luas | Rumus Keliling |
|--------|-------|----------------|------------|----------------|
| `generate_right_triangle` | Segitiga Siku-siku | base, height, hypotenuse | ½·b·h | b+h+√(b²+h²) |
| `generate_equilateral_triangle` | Segitiga Sama Sisi | side, height | (√3/4)·s² | 3s |
| `generate_isosceles_triangle` | Segitiga Sama Kaki | base, leg, height | ½·b·√(l²-(b/2)²) | 2l+b |
| `generate_scalene_triangle` | Segitiga Sembarang | side_a,b,c | Heron: √(s(s-a)(s-b)(s-c)) | a+b+c |
| `generate_acute_triangle` | Segitiga Lancip | side_a,b,c | Heron (validasi sudut <90°) | a+b+c |
| `generate_obtuse_triangle` | Segitiga Tumpul | side_a,b,c | Heron (validasi sudut >90°) | a+b+c |
| `generate_parallelogram` | Jajargenjang | base, side, height | a·t | 2(a+s) |
| `generate_right_trapezoid` | Trapesium Siku-siku | base_a,b, height, slant | ½·(a+b)·t | a+b+t+m |
| `generate_isosceles_trapezoid` | Trapesium Sama Kaki | base_a,b, leg, height | ½·(a+b)·√(l²-((b-a)/2)²) | a+b+2l |
| `generate_kite` | Layang-layang | diagonal_1,2, intersection | ½·d₁·d₂ | 2(s₁+s₂) |
| `generate_rhombus` | Belah Ketupat | diagonal_1,2, side | ½·d₁·d₂ | 4·√((d₁/2)²+(d₂/2)²) |
| `generate_ellipse` | Oval/Elips | semi_major, semi_minor | π·a·b | π·[3(a+b)-√((3a+b)(a+3b))] |
| `generate_pentagon` | Segi Lima | side | ¼√(5(5+2√5))·s² | 5s |
| `generate_hexagon` | Segi Enam | side | (3√3/2)·s² | 6s |
| `generate_octagon` | Segi Delapan | side | 2(1+√2)·s² | 8s |

### Fungsi helper baru:
- `_classify_triangle_sides(a, b, c)` — klasifikasi segitiga berdasarkan sisi (acute/right/obtuse)
- `_generate_triangle_by_type(rng, config, target_type)` — generate sisi segitiga sesuai tipe

---

## 2. File: `app/core/geometry/mesh.py`

### Fungsi mesh 2D baru untuk visualisasi:

| Fungsi Mesh | Output (vertices) |
|-------------|-------------------|
| `generate_triangle_2d_mesh(x1,y1, x2,y2, x3,y3)` | 3 vertex, 1 face |
| `generate_equilateral_triangle_mesh(side)` | Segitiga sama sisi di bidang z=0 |
| `generate_parallelogram_mesh(base, side, height)` | 4 vertex, 2 faces |
| `generate_trapezoid_mesh(a, b, h)` | Trapesium 4 vertex, 2 faces |
| `generate_kite_mesh(d1, d2, p)` | Layang-layang 4 vertex, 2 faces |
| `generate_rhombus_mesh(d1, d2)` | Belah ketupat 4 vertex, 2 faces |
| `generate_ellipse_mesh(a, b, segments=32)` | Oval dengan N-gon |
| `generate_regular_polygon_2d_mesh(n, side)` | Poligon beraturan N vertex, N-2 faces |

---

## 3. File: `app/services/geometry_service.py`

### Perubahan:
1. **Update import** — tambah semua fungsi baru dari `shapes.py` dan `mesh.py`
2. **`get_available_shapes()`** — perluas daftar 2D:

```python
"2D": [
    "square", "rectangle", "circle", "ellipse",
    "right_triangle", "equilateral_triangle", "isosceles_triangle",
    "scalene_triangle", "acute_triangle", "obtuse_triangle",
    "parallelogram", "right_trapezoid", "isosceles_trapezoid",
    "kite", "rhombus",
    "pentagon", "hexagon", "octagon"
]
```

3. **`generate_geometry_question()`** — tambah blok `elif` untuk setiap shape baru
4. **Level unlocking** — shape sederhana (segitiga, jajargenjang) di level 1-2, oval/polygon di level 3+

---

## 4. File: `app/core/geometry/__init__.py`
- Tidak perlu perubahan (tetap kosong)

---

## Catatan Implementasi
- Fungsi `generate_triangle()` yang sudah ada dipertahankan untuk backward compatibility
- Validasi triangle inequality untuk semua segitiga (a+b>c, a+c>b, b+c>a)
- Semua mesh 2D menggunakan koordinat (x, y) pada bidang z=0
- Nilai float dibulatkan ke 2 desimal untuk menghindari floating point issues
