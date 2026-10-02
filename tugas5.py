import cv2
import numpy as np
import pytesseract
import sys
from pathlib import Path

# Path Tesseract jika diperlukan (sesuaikan di OS Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def calc_accuracy(predicted, ground_truth):
    """Menghitung akurasi berbasis Character Error Rate (CER) / Match Rate"""
    if not predicted or not ground_truth:
        return 0.0
    
    # Hitung Levenshtein Distance sederhana untuk akurasi berbasis karakter
    import difflib
    matcher = difflib.SequenceMatcher(None, predicted.strip(), ground_truth.strip())
    return round(matcher.ratio() * 100, 2)

def count_correct_chars(predicted, ground_truth):
    """Menghitung berapa karakter yang cocok posisi/nilainya"""
    correct = 0
    min_len = min(len(predicted), len(ground_truth))
    for i in range(min_len):
        if predicted[i] == ground_truth[i]:
            correct += 1
    return correct

def run_experiment(image_path, ground_truth_text="Nomor ijazah: 571012022000056"):
    # 1. Load Citra Grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Gagal memuat citra dari path: {image_path}")
        return

    # 2. Terapkan Filter sesuai Tugas
    # A. Original
    img_original = img.copy()

    # B. Mean Filter (Average Blur)
    img_mean = cv2.blur(img, (3, 3))

    # C. Median Filter
    img_median = cv2.medianBlur(img, 3)

    # D. Gaussian Filter
    img_gaussian = cv2.GaussianBlur(img, (3, 3), 0)

    # E. Sharpening (Menggunakan Kernel Laplacian Unsharp Masking)
    kernel_sharpen = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]])
    img_sharpened = cv2.filter2D(img, -1, kernel_sharpen)

    methods = {
        "Original": img_original,
        "Mean Filter": img_mean,
        "Median Filter": img_median,
        "Gaussian Filter": img_gaussian,
        "Sharpening": img_sharpened
    }

    # Konfigurasi Tesseract OCR
    custom_config = r'--oem 3 --psm 6'

    # Display Tabel Hasil
    print("=" * 75)
    print("HASIL PENGUJJIAN FILTERING, NOISE REDUCTION, SHARPENING & OCR TESSERACT")
    print("=" * 75)
    print(f"{'Metode':<18} | {'Hasil OCR':<30} | {'Karakter Benar':<14} | {'Akurasi (%)':<10}")
    print("-" * 75)

    for name, processed_img in methods.items():
        # OCR Processing
        ocr_result = pytesseract.image_to_string(processed_img, config=custom_config).strip()
        ocr_clean = ocr_result.replace('\n', ' ')
        
        # Hitung Karakter Benar dan Akurasi
        correct_count = count_correct_chars(ocr_clean, ground_truth_text)
        accuracy = calc_accuracy(ocr_clean, ground_truth_text)
        
        # Tampilkan dalam format tabel
        print(f"{name:<18} | {ocr_clean:<30} | {correct_count:<14} | {accuracy:<10.2f}%")
        
        # Opsional: Simpan citra hasil filter ke folder
        out_dir = Path("hasil_filtering")
        out_dir.mkdir(exist_ok=True)
        cv2.imwrite(str(out_dir / f"{name.lower().replace(' ', '_')}.jpg"), processed_img)

    print("=" * 75)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_experiment(sys.argv[1])
    else:
        # Ganti dengan path citra Anda untuk pengujian lokal
        run_experiment('./tugas 4/04_HighNoise.jpg')