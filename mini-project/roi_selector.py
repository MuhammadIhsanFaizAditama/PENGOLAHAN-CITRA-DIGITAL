"""
roi_selector.py
Klik dua titik pada gambar:
1. Sudut kiri atas ROI
2. Sudut kanan bawah ROI
Tekan R untuk mengulang, Enter untuk menyimpan/menampilkan koordinat, Esc untuk keluar.
"""
import argparse
import cv2


points = []
display_image = None


def on_mouse(event, x, y, flags, param):
    global points, display_image
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        if len(points) > 2:
            points = [(x, y)]

        if len(points) == 2:
            (x1, y1), (x2, y2) = points
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))
            cv2.rectangle(display_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        elif len(points) == 1:
            cv2.circle(display_image, (x, y), 5, (0, 0, 255), -1)


def main():
    global display_image, points

    parser = argparse.ArgumentParser(description="Pilih ROI dengan klik mouse.")
    parser.add_argument("--image", required=True, help="Path gambar ijazah.")
    args = parser.parse_args()

    image = cv2.imread(args.image)
    if image is None:
        raise FileNotFoundError(f"Tidak dapat membaca gambar: {args.image}")

    display_image = image.copy()
    original = image.copy()
    window = "ROI Selector - klik kiri atas lalu kanan bawah"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window, on_mouse)

    print("Klik sudut kiri-atas dan kanan-bawah area ROI.")
    print("Tekan R untuk reset, Enter untuk mencetak koordinat, Esc untuk keluar.")

    while True:
        cv2.imshow(window, display_image)
        key = cv2.waitKey(20) & 0xFF

        if key in (13, 10):  # Enter
            if len(points) == 2:
                (x1, y1), (x2, y2) = points
                x = min(x1, x2)
                y = min(y1, y2)
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                print(f"ROI untuk CLI: {x},{y},{width},{height}")
                print(f"ROI Python: ({x}, {y}, {width}, {height})")
                roi = original[y:y + height, x:x + width]
                cv2.imshow("Hasil ROI", roi)
            else:
                print("Pilih dua titik terlebih dahulu.")
        elif key in (ord("r"), ord("R")):
            points = []
            display_image = original.copy()
            print("Pilihan ROI direset.")
        elif key == 27:  # Esc
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
