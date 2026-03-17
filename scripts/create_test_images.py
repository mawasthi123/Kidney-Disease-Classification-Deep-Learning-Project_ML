"""
Create 50 test images (224x224 JPEG) for prediction testing.
Run from project root: python scripts/create_test_images.py
"""
import os
from pathlib import Path

# Use PIL if available, else skip (user can run after pip install Pillow)
try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Install Pillow: pip install Pillow")
    raise

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "test_images"
SIZE = (224, 224)  # model input size
NUM_IMAGES = 50


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    for i in range(1, NUM_IMAGES + 1):
        # Slight variation per image so they're not identical
        arr = np.clip(np.random.rand(224, 224, 3) * 200 + 20, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)
        path = OUTPUT_DIR / f"test_image_{i:02d}.jpg"
        img.save(path, "JPEG", quality=85)
    print(f"Created {NUM_IMAGES} test images in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
