# Hasil Analisis Metode Enhancement Berdasarkan Character Error Rate (CER)

## 1. Tujuan Evaluasi

Evaluasi ini bertujuan menentukan metode enhancement yang paling efektif untuk membaca nomor ijazah menggunakan Optical Character Recognition (OCR). Tiga metode yang dibandingkan adalah **Unsharp Masking**, **CLAHE**, dan **Otsu Thresholding**. Penilaian didasarkan pada Character Error Rate (CER), dengan nomor referensi `571012022000056`.

Data yang dianalisis berasal dari sembilan pengujian citra ijazah dengan kondisi berbeda, sebagaimana tercatat pada berkas `analisis.md`.

## 2. Hasil Pengujian

Pada seluruh sembilan citra uji, ketiga metode menghasilkan teks nomor ijazah yang sama dengan nomor referensi, yaitu `571012022000056`. Setiap hasil pengujian mencatat CER sebesar `0.0`.

| No. | Kondisi citra | Unsharp Masking (CER) | CLAHE (CER) | Otsu Thresholding (CER) |
|---:|---|---:|---:|---:|
| 1 | High Quality Enhanced | 0.0 | 0.0 | 0.0 |
| 2 | Low Contrast | 0.0 | 0.0 | 0.0 |
| 3 | Blurred | 0.0 | 0.0 | 0.0 |
| 4 | High Noise | 0.0 | 0.0 | 0.0 |
| 5 | Low Resolution (Upsampled) | 0.0 | 0.0 | 0.0 |
| 6 | Faded / Underexposed | 0.0 | 0.0 | 0.0 |
| 7 | Color Shift / Warm Tint | 0.0 | 0.0 | 0.0 |
| 8 | JPEG Compression Artifacts | 0.0 | 0.0 | 0.0 |
| 9 | Combined Degradation | 0.0 | 0.0 | 0.0 |
| **Rata-rata CER** | **9 citra** | **0.0000** | **0.0000** | **0.0000** |

## 3. Interpretasi CER

Character Error Rate dihitung menggunakan:

\[
CER = \frac{S + D + I}{N}
\]

dengan:
- \(S\): jumlah karakter yang disubstitusi;
- \(D\): jumlah karakter yang dihapus;
- \(I\): jumlah karakter yang disisipkan;
- \(N\): jumlah karakter pada teks referensi.

CER `0.0` berarti tidak ditemukan kesalahan karakter pada hasil OCR dibandingkan dengan nomor referensi. Karena ketiga metode membaca nomor dengan benar pada seluruh sembilan citra, nilai CER masing-masing metode tetap nol pada data pengujian ini.

## 4. Metode Enhancement Mana yang Paling Efektif?

**Berdasarkan nilai CER pada hasil pengujian yang tersedia, tidak ada satu metode yang dapat dinyatakan lebih unggul daripada metode lainnya.** Unsharp Masking, CLAHE, dan Otsu Thresholding memperoleh hasil yang setara: rata-rata CER `0.0000` dan seluruh nomor terbaca tepat.

Dengan demikian:
- **Unsharp Masking:** efektif pada dataset ini, dengan CER nol.
- **CLAHE:** efektif pada dataset ini, dengan CER nol.
- **Otsu Thresholding:** efektif pada dataset ini, dengan CER nol.

Kesimpulan yang tepat adalah bahwa **ketiga metode sama efektifnya menurut metrik CER pada sembilan citra yang diuji**. Memilih salah satunya sebagai metode terbaik tanpa metrik pembeda tambahan tidak didukung oleh hasil tersebut.

## 5. Pembahasan dan Keterbatasan

Hasil yang sama pada semua metode menunjukkan bahwa tugas OCR ini berhasil untuk nomor ijazah yang diuji. Namun, hasil tersebut tidak otomatis membuktikan bahwa ketiga metode akan sama baiknya pada semua ijazah, format nomor, resolusi, atau kondisi degradasi lain.

Ada beberapa batasan yang perlu diperhatikan:

1. **Skor CER mengalami efek plafon kinerja.** Karena seluruh metode mencapai CER nol, metrik ini tidak dapat membedakan performa relatif mereka pada dataset ini.
2. **Jumlah data terbatas.** Kesimpulan hanya berlaku pada sembilan citra yang tercatat.
3. **Satu nomor referensi digunakan.** Semua pengujian membandingkan hasil terhadap nomor `571012022000056`; pengujian dengan nomor dan tata letak yang lebih beragam diperlukan untuk menilai generalisasi.
4. **CER hanya mengukur kesalahan teks.** CER tidak menilai waktu proses, kestabilan hasil, kualitas visual, atau kebutuhan komputasi.
5. **Tidak ada bukti keunggulan statistik.** Karena nilai CER identik, hasil ini tidak mendukung klaim bahwa salah satu metode secara statistik lebih baik.

## 6. Rekomendasi Evaluasi Lanjutan

Untuk membedakan ketiga metode secara lebih meyakinkan, penelitian berikutnya dapat:
- menambah jumlah citra dan variasi nomor ijazah;
- memasukkan kondisi yang lebih ekstrem, misalnya karakter sangat pudar atau terpotong;
- melaporkan jumlah citra dengan CER nol, rata-rata CER, median CER, serta distribusi CER per kondisi;
- mencatat waktu pemrosesan untuk setiap metode sebagai metrik tambahan;
- menjaga ROI, konfigurasi OCR, dan prosedur evaluasi tetap konsisten agar perbandingan adil.

Jika pengujian tambahan menghasilkan CER yang berbeda, metode dengan **rata-rata CER terendah pada dataset uji yang representatif** dapat dipilih sebagai metode paling akurat untuk tujuan tersebut.

## 7. Kesimpulan

Berdasarkan sembilan hasil pengujian dalam `analisis.md`, **Unsharp Masking, CLAHE, dan Otsu Thresholding sama-sama memperoleh CER sebesar 0.0 pada setiap citra**. Oleh sebab itu, tidak ada pemenang tunggal berdasarkan CER. Ketiganya mencapai akurasi karakter sempurna pada data yang dilaporkan, sehingga dibutuhkan data uji yang lebih beragam atau metrik tambahan untuk menentukan metode yang paling efektif secara keseluruhan.
