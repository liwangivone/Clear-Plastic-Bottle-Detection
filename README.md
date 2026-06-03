# Clear Plastic Bottle Trash Detection — Web App

> Segmentasi botol plastik bening menggunakan Canny Edge Detection + Watershed Algorithm

---

## Struktur Folder

```
my_project/
├── main.py               ← Flask app (entry point)
├── preprocessing.py      ← CLAHE, Blur, Normalize
├── segmentation.py       ← Canny + Watershed + Overlay
├── utils.py              ← Load, save, validate image
├── evaluate.py           ← Statistik segmentasi
├── requirements.txt
├── templates/
│   └── index.html        ← Halaman utama
├── static/
│   ├── style.css
│   └── app.js
├── dataset/
│   ├── raw/              ← Gambar upload disimpan di sini
│   └── ground_truth/
└── results/              ← Gambar hasil segmentasi
```

---

## Setup & Menjalankan

### 1. Buat virtual environment (opsional tapi disarankan)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan server
```bash
python main.py
```

### 4. Buka browser
```
http://localhost:5000
```

---

## Alur Pipeline

```
Upload Gambar (JPG/PNG/BMP)
        ↓
  Preprocessing
  - CLAHE (normalisasi kontras)
  - Gaussian Blur 5×5 (reduksi noise)
  - Normalize 0–255
        ↓
  Canny Edge Detection
  - Low threshold  : 30
  - High threshold : 100
        ↓
  Watershed Segmentation
  - Otsu thresholding
  - Morphological open + close
  - Distance transform
  - Connected components → markers
  - Watershed transform
        ↓
  Overlay Visualisasi
  - Cyan  = tepi Canny
  - Merah = batas Watershed
        ↓
  Hasil ditampilkan + Statistik
```

---

## Author
**Ivone Liwang** · 1076012527103  
IMT – Full Stack Development · Digital Image Processing
