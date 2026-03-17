"""
Copy real kidney CT images (Normal & Tumor) from the dataset into test_images.
Run from project root after data ingestion: python scripts/copy_real_test_images.py
"""
import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET = PROJECT_ROOT / "artifacts" / "data_ingestion" / "kidney-ct-scan-image"
OUTPUT_DIR = PROJECT_ROOT / "test_images" / "real_kidney_ct"
PER_CLASS = 25  # images per class (Normal, Tumor)


def main():
    if not DATASET.exists():
        print("Run data ingestion first: python src/cnnClassifier/pipeline/stage_01_data_ingestion.py")
        return
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for label in ["Normal", "Tumor"]:
        src_dir = DATASET / label
        if not src_dir.is_dir():
            print(f"Missing folder: {src_dir}")
            continue
        images = sorted(f for f in src_dir.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png"))[:PER_CLASS]
        prefix = "real_normal" if label == "Normal" else "real_tumor"
        for i, src in enumerate(images, 1):
            ext = src.suffix
            dest = OUTPUT_DIR / f"{prefix}_{i:02d}{ext}"
            shutil.copy2(src, dest)
        print(f"Copied {len(images)} {label} images -> {OUTPUT_DIR}")
    print(f"Done. Real test images in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
