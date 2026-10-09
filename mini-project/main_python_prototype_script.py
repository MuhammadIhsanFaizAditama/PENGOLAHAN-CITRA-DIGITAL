"""Prototype verifikasi nomor ijazah dan indikasi keberadaan tanda tangan.

Catatan: deteksi tanda tangan di sini hanya heuristik berbasis piksel foreground,
bukan autentikasi tanda tangan atau bukti keaslian ijazah.
"""
from __future__ import annotations

import argparse
import os
import re

import cv2
import Levenshtein
import pandas as pd
import pytesseract

# ROI format: (x, y, width, height). Sesuaikan jika resolusi/layout gambar berbeda.
OCR_ROI_BBOX = (550, 2253, 457, 72)
SIGNATURE_ROI_BBOX = (2120, 1521, 943, 641)


def load_and_preprocess(image_path: str):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(
            f"Gambar tidak ditemukan atau tidak dapat dibaca: {image_path}\n"
            "Periksa path gambar dan pastikan file tersedia."
        )
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.GaussianBlur(gray, (3, 3), 0)
    return image, gray, denoised


def crop_roi(image, bbox, label: str):
    x, y, w, h = bbox
    height, width = image.shape[:2]
    if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
        raise ValueError(
            f"{label} {bbox} berada di luar citra berukuran {width}x{height}. "
            "Koordinat ROI pada script perlu disesuaikan dengan gambar ini."
        )
    roi = image[y:y + h, x:x + w]
    if roi.size == 0:
        raise ValueError(f"{label} kosong. Periksa koordinat ROI.")
    return roi


def enhance_unsharp_mask(gray_roi):
    blurred = cv2.GaussianBlur(gray_roi, (5, 5), 1.0)
    return cv2.addWeighted(gray_roi, 1.5, blurred, -0.5, 0)


def enhance_clahe(gray_roi):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray_roi)


def enhance_otsu(gray_roi):
    _, binary = cv2.threshold(
        gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return binary


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text.upper()).strip()


def calculate_cer(reference_text: str, hypothesis_text: str) -> float:
    reference = normalize_text(reference_text)
    hypothesis = normalize_text(hypothesis_text)
    if not reference:
        raise ValueError("Nomor referensi kosong; CER tidak dapat dihitung.")
    return Levenshtein.distance(reference, hypothesis) / len(reference)


def parse_number(text: str) -> str:
    cleaned = normalize_text(text)
    # Nomor pada contoh ini berupa angka saja; pola umum juga mengizinkan huruf/hyphen.
    match = re.search(r"[A-Z0-9-]+", cleaned)
    return match.group(0) if match else cleaned


def process_ocr_branch(roi, reference_text: str | None = None):
    methods = {
        "Unsharp Masking": enhance_unsharp_mask(roi),
        "CLAHE": enhance_clahe(roi),
        "Otsu Thresholding": enhance_otsu(roi),
    }
    tess_config = (
        "--oem 3 --psm 7 "
        "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    )
    rows = []
    for method, enhanced in methods.items():
        raw_text = pytesseract.image_to_string(enhanced, config=tess_config).strip()
        extracted = parse_number(raw_text)
        cer = calculate_cer(reference_text, extracted) if reference_text else None
        rows.append({
            "Metode": method,
            "Hasil OCR": extracted,
            "CER": cer,
        })
    report = pd.DataFrame(rows)
    if reference_text and not report.empty:
        best_idx = report["CER"].astype(float).idxmin()
        best_text = report.loc[best_idx, "Hasil OCR"]
    else:
        best_text = report.iloc[0]["Hasil OCR"] if not report.empty else ""
    return best_text, report


def process_signature_branch(roi, min_pixel_threshold: int = 1500):
    adaptive = cv2.adaptiveThreshold(
        roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 15, 8
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel)
    foreground_pixels = int(cv2.countNonZero(closed))
    status = "PRESENT" if foreground_pixels >= min_pixel_threshold else "NOT PRESENT"
    return status, foreground_pixels


def run_pipeline(image_path: str, reference_number: str | None):
    print("=" * 64)
    print(f"MEMPROSES CITRA: {os.path.basename(image_path)}")
    print("=" * 64)
    _, _, denoised = load_and_preprocess(image_path)
    roi_ocr = crop_roi(denoised, OCR_ROI_BBOX, "ROI nomor ijazah")
    roi_signature = crop_roi(denoised, SIGNATURE_ROI_BBOX, "ROI tanda tangan")

    detected_number, cer_report = process_ocr_branch(roi_ocr, reference_number)
    signature_status, foreground_pixels = process_signature_branch(roi_signature)

    print("\n[HASIL OUTPUT VERIFIKASI]")
    print(f"Nomor ijazah       : {detected_number or '[TIDAK TERBACA]'}")
    print(f"Indikasi tanda tangan: {signature_status}")
    print(f"Piksel foreground  : {foreground_pixels}")
    print("\n[EVALUASI METODE OCR]")
    print(cer_report.to_string(index=False))
    if reference_number:
        best = cer_report.loc[cer_report["CER"].astype(float).idxmin()]
        print(f"\nCER terendah: {best['Metode']} (CER={best['CER']:.4f})")
        tied = cer_report[cer_report["CER"].astype(float) == float(best["CER"])]
        if len(tied) > 1:
            print("Catatan: beberapa metode memiliki CER sama; hasil ini belum menunjukkan pemenang tunggal.")
    else:
        print("CER tidak dihitung karena --ref tidak diberikan.")
    print("\nPeringatan: PRESENT hanya menunjukkan cukup banyak piksel foreground pada ROI, bukan validasi keaslian tanda tangan/ijazah.")


def main():
    parser = argparse.ArgumentParser(
        description="Prototype OCR nomor ijazah dan deteksi indikatif tanda tangan."
    )
    parser.add_argument("--image", required=True, help="Path citra ijazah.")
    parser.add_argument("--ref", default=None, help="Nomor ijazah acuan (ground truth) untuk menghitung CER.")
    args = parser.parse_args()
    run_pipeline(args.image, args.ref)


if __name__ == "__main__":
    main()
