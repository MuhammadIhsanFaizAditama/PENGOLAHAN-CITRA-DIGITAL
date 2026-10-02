import cv2
import numpy as np
import os
import sys  

def fix_orientation(image):
    h, w = image.shape[:2]
    if w > h:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return image

def analyze_signature(roi_image, label="Signature Region"):
    gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)

    _, thresh_global = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    _, thresh_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    thresh_adaptive = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 15, 8
    )

    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    img_open = cv2.morphologyEx(thresh_otsu, cv2.MORPH_OPEN, kernel_open)

    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_morph = cv2.morphologyEx(img_open, cv2.MORPH_CLOSE, kernel_close)

    fg_global = cv2.countNonZero(thresh_global)
    fg_otsu = cv2.countNonZero(thresh_otsu)
    fg_adaptive = cv2.countNonZero(thresh_adaptive)
    fg_morph = cv2.countNonZero(img_morph)

    THRESHOLD_PIXELS = 650
    status = "SIGNATURE PRESENT" if fg_morph >= THRESHOLD_PIXELS else "SIGNATURE ABSENT"

    print(f"=== ANALISIS ROI: {label} ===")
    print(f"Piksel Foreground (Global Thresh)   : {fg_global} px")
    print(f"Piksel Foreground (Otsu Thresh)     : {fg_otsu} px")
    print(f"Piksel Foreground (Adaptive Thresh) : {fg_adaptive} px")
    print(f"Piksel Foreground (Morphology Final): {fg_morph} px")
    print(f"Status Keberadaan Tanda Tangan      : {status}\n")

def process_ijazah(image_path):
    print("=" * 60)
    print(f"MEMPROSES CITRA: {os.path.basename(image_path)}")
    print("=" * 60)

    img = cv2.imread(image_path)
    if img is None:
        print(f"Gagal memuat citra dari path: {image_path}")
        return

    img_upright = fix_orientation(img)
    h, w = img_upright.shape[:2]

    roi_rektor = img_upright[int(h*0.65):int(h*0.90), int(w*0.10):int(w*0.48)]
    roi_dekan = img_upright[int(h*0.65):int(h*0.90), int(w*0.58):int(w*0.95)]

    analyze_signature(roi_rektor, label="Tanda Tangan Rektor")
    analyze_signature(roi_dekan, label="Tanda Tangan Dekan")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = r".\Praktikum citra\01_HighQuality_Enhanced.jpg"
        
    process_ijazah(input_path)