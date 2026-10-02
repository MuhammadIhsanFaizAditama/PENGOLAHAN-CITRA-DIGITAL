#!/usr/bin/env python3
"""
pemrosesan_ijazah_cropped.py
Khusus untuk citra nomor ijazah yang SUDAH DI-CROP MANUAL.
Tugas:
1. Memproses 3 metode enhancement (Brightness, Contrast Stretching, Histogram Equalization).
2. Menampilkan visualisasi Citra vs Histogram (Sebelum & Sesudah).
3. Menguji hasil OCR untuk menentukan metode terbaik.
"""

import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

# ---------- 1. METODE ENHANCEMENT ----------
def apply_brightness_adjustment(gray, beta=40):
    """Metode 1: Brightness Adjustment (+40)"""
    return cv2.add(gray, beta)

def apply_contrast_stretching(gray):
    """Metode 2: Contrast Stretching (Min-Max Normalization 0-255)"""
    r_min, r_max = np.min(gray), np.max(gray)
    if r_max == r_min:
        return gray
    stretched = ((gray - r_min) / (r_max - r_min) * 255.0)
    return np.clip(stretched, 0, 255).astype(np.uint8)

def apply_histogram_equalization(gray):
    """Metode 3: Histogram Equalization"""
    return cv2.equalizeHist(gray)

# ---------- 2. OCR TESSERACT ----------
def run_ocr(gray_img):
    # Upscale 2x & Binarisasi Otsu untuk pembacaan OCR optimal
    resized = cv2.resize(gray_img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    _, bw = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    try:
        text = pytesseract.image_to_string(bw, lang="ind+eng", config="--psm 6")
    except:
        text = pytesseract.image_to_string(bw, config="--psm 6")
    return text.strip()

# ---------- 3. EKSEKUSI UTAMA ----------
def main():
    ap = argparse.ArgumentParser(description="Enhancement & OCR pada Gambar Nomor Ijazah Crop Manual")
    ap.add_argument("berkas", help="Path gambar hasil crop manual (.jpg / .png)")
    args = ap.parse_args()

    if not os.path.exists(args.berkas):
        raise SystemExit(f"File tidak ditemukan: {args.berkas}")

    # Baca gambar langsung dalam format Grayscale (karena sudah di-crop)
    img_gray = cv2.imread(args.berkas, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        raise SystemExit("Gagal membaca gambar.")

    # Terapkan Ketiga Metode Enhancement
    results = {
        "1. Sebelum (Asli Grayscale)": img_gray,
        "2. Brightness Adjustment": apply_brightness_adjustment(img_gray, beta=40),
        "3. Contrast Stretching": apply_contrast_stretching(img_gray),
        "4. Histogram Equalization": apply_histogram_equalization(img_gray)
    }

    # Plot Visualisasi: 4 Baris x 2 Kolom (Citra vs Histogram)
    fig, axes = plt.subplots(4, 2, figsize=(11, 9))
    fig.suptitle("Perbandingan Citra & Histogram Nomor Ijazah", fontsize=13)

    ocr_results = {}

    for idx, (title, img_proc) in enumerate(results.items()):
        # Jalankan OCR
        teks_ocr = run_ocr(img_proc)
        ocr_results[title] = teks_ocr

        # Plot Citra (Kolom Kiri)
        axes[idx, 0].imshow(img_proc, cmap='gray', vmin=0, vmax=255)
        axes[idx, 0].set_title(f"Citra: {title}", fontsize=10)
        axes[idx, 0].axis('off')

        # Plot Histogram (Kolom Kanan)
        axes[idx, 1].hist(img_proc.ravel(), bins=256, range=[0, 256], color='black', alpha=0.75)
        axes[idx, 1].set_title(f"Histogram: {title}", fontsize=10)
        axes[idx, 1].set_xlim([0, 256])

    plt.tight_layout()
    plt.show()

    # Cetak Hasil Perbandingan OCR ke Terminal
    print("\n" + "="*65)
    print(" HASIL PENGUJIAN OCR TESSERACT ")
    print("="*65)
    for title, teks in ocr_results.items():
        print(f"[{title}]")
        print(f"  Teks Terbaca : {teks if teks else '(Kosong / Tidak Terbaca)'}")
        print("-" * 65)

if __name__ == "__main__":
    main()  