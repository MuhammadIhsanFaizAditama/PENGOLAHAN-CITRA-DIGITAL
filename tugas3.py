import cv2
import numpy as np
import matplotlib.pyplot as plt

img_bgr = cv2.imread('sample\\6 Sept 2026 at 06_35(8).jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

rata2 = np.mean(img_gray)
kontras = np.std(img_gray)

print(f"Rata-rata Kecerahan: {rata2:.1f} | Kontras (Std Dev): {kontras:.1f}")
if rata2 < 90:
    print("Diagnosa: Citra Terlalu Gelap")
elif rata2 > 160:
    print("Diagnosa: Citra Terlalu Terang")
elif kontras < 40:
    print("Diagnosa: Kontras Rendah")
else:
    print("Diagnosa: Distribusi Piksel Normal/Cukup Baik")

plt.figure(figsize=(12, 4))

# Gambar Grayscale
plt.subplot(1, 3, 1)
plt.imshow(img_gray, cmap='gray')
plt.title('Citra Grayscale')
plt.axis('off')

# Histogram RGB
plt.subplot(1, 3, 2)
for i, col in enumerate(['r', 'g', 'b']):
    plt.plot(
        cv2.calcHist([img_rgb], [i], None, [256], [0, 256]),
        color=col,
        label=col.upper(),
    )
plt.title('Histogram Asli (RGB)')
plt.xlim([0, 256])
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(
    cv2.calcHist([img_gray], [0], None, [256], [0, 256]), color='black'
)
plt.title('Histogram Grayscale')
plt.xlim([0, 256])

plt.tight_layout()
plt.show()