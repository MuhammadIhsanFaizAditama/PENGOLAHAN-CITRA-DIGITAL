# Cara Menjalankan Program Tugas 6

Program ini memeriksa keberadaan tanda tangan pada citra ijazah menggunakan OpenCV. Jalankan launcher Python dengan perintah `py`.

## Persiapan

1. Pastikan Python sudah terpasang dan perintah `py` dapat digunakan di Command Prompt atau PowerShell.
2. Buka terminal di folder proyek.
3. Pasang dependensi dari `requirements.txt`:

   ```powershell
   py -m pip install -r requirements.txt
   ```

## Menjalankan

Jalankan tanpa argumen untuk memproses citra default:

```powershell
py run.py
```

Untuk memilih citra lain, berikan lokasi file sebagai argumen. Gunakan tanda kutip jika path mengandung spasi:

```powershell
py run.py ".\Praktikum citra\09_CombinedDegradation.jpg"
```

Hasil analisis untuk area tanda tangan rektor dan dekan akan ditampilkan di terminal. Alternatifnya, script utama dapat dijalankan langsung dengan `py tugas6.py` dan path citra opsional.
