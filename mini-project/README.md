# Prototype Verifikasi Ijazah Otomatis

Prototype CLI Python untuk membaca nomor ijazah dengan Tesseract OCR, membandingkan tiga strategi prapemrosesan (Unsharp Masking, CLAHE, dan Otsu Thresholding) berdasarkan Character Error Rate (CER), serta memperkirakan keberadaan tanda tangan berdasarkan jumlah piksel foreground pada ROI.

> **Batasan penting:** deteksi `PRESENT` hanya merupakan heuristik berbasis piksel di area yang dipilih. Ini bukan autentikasi tanda tangan, verifikasi identitas penandatangan, ataupun bukti keaslian ijazah.

## Struktur repositori

```text
diploma-verification-prototype/
├── main_python_prototype_script.py
├── roi_selector.py
├── hasil.md
├── README.md
├── requirements.txt
└── .gitignore
```

Folder `assets` dan `outputs` sudah dihapus. Laporan hasil evaluasi tersedia di `hasil.md`.

## Prasyarat

- Python 3.10 atau lebih baru.
- Tesseract OCR terpasang sebagai aplikasi sistem.
- Gambar uji tersedia pada path yang diberikan.

### Instalasi di Windows

1. Instal Tesseract OCR dan pastikan `tesseract.exe` tersedia di PATH. Jika belum, tambahkan lokasi instalasi Tesseract ke PATH Windows.
2. Buka terminal pada folder project.
3. Buat dan aktifkan virtual environment (opsional tetapi disarankan):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Instal dependency:

```powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

## Menjalankan program

Jalankan dari direktori akar project. Contoh sesuai lokasi citra praktikum:

```powershell
py main_python_prototype_script.py --image ".\Praktikum citra\02_LowContrast.jpg" --ref "571012022000056"
```

- `--image`: lokasi file gambar ijazah.
- `--ref`: nomor ijazah yang benar sebagai ground truth untuk menghitung CER.

Jika hanya ingin menjalankan OCR tanpa menghitung CER, hilangkan argumen `--ref`.

## Catatan penting mengenai ROI

Koordinat ROI nomor dan tanda tangan diatur pada bagian atas `main_python_prototype_script.py`:

```python
OCR_ROI_BBOX = (550, 2253, 457, 72)
SIGNATURE_ROI_BBOX = (2120, 1521, 943, 641)
```

Formatnya `(x, y, lebar, tinggi)`. Koordinat ini harus sesuai dengan resolusi dan tata letak gambar. Jika muncul pesan ROI berada di luar citra atau hasil OCR tidak tepat, pilih ulang area menggunakan selector:

```powershell
py roi_selector.py --image "image.png"
```

Klik sudut kiri atas dan kanan bawah area yang ingin dipotong, lalu tekan Enter untuk mencetak koordinat. Catat koordinat ROI nomor dan ROI tanda tangan secara terpisah, kemudian ubah nilai pada script utama.

## Metode yang digunakan

1. **Preprocessing:** konversi grayscale dan Gaussian Blur ringan.
2. **Unsharp Masking:** menajamkan detail dengan menambahkan selisih antara citra asli dan citra blur.
3. **CLAHE:** meningkatkan kontras lokal dengan membatasi amplifikasi histogram.
4. **Otsu Thresholding:** mengubah citra grayscale menjadi citra biner menggunakan ambang global otomatis.
5. **Evaluasi OCR:** Tesseract membaca ROI untuk setiap metode; CER dihitung dari jarak Levenshtein dibagi jumlah karakter referensi.
6. **Deteksi indikatif tanda tangan:** adaptive thresholding, morphological closing, lalu menghitung piksel foreground.

## Hasil analisis

Lihat [`hasil.md`](hasil.md). Berdasarkan sembilan hasil uji yang tercatat di `analisis.md`, ketiga metode sama-sama memperoleh CER 0.0 untuk setiap gambar. Dengan data tersebut, tidak ada satu metode yang dapat dinyatakan lebih unggul hanya berdasarkan CER.

## Privasi dan etika

Ijazah memuat data pribadi. Gunakan gambar yang mendapat izin, samarkan informasi yang tidak dibutuhkan, dan jangan unggah ijazah asli ke repositori publik.
