import argparse
from pathlib import Path

from tugas6 import process_ijazah


def main():
    default_image = Path(__file__).parent / "Praktikum citra" / "01_HighQuality_Enhanced.jpg"
    parser = argparse.ArgumentParser(description="Analisis tanda tangan pada citra ijazah.")
    parser.add_argument(
        "image",
        nargs="?",
        type=Path,
        default=default_image,
        help="Path citra yang akan dianalisis.",
    )
    args = parser.parse_args()
    process_ijazah(str(args.image))


if __name__ == "__main__":
    main()