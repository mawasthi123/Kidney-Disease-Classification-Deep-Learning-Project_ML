# Test images

## Real kidney CT images (Normal & Tumor)

**Folder:** `test_images/real_kidney_ct/`

- **25 Normal:** `real_normal_01.jpg` … `real_normal_25.jpg` (true label: Normal)
- **25 Tumor:** `real_tumor_01.jpg` … `real_tumor_25.jpg` (true label: Tumor)

Use these to test the model and compare prediction vs actual label. Run the app, open http://localhost:8080, **Upload** any file from this folder, then **Predict**.

**Regenerate:** After running data ingestion (`python src/cnnClassifier/pipeline/stage_01_data_ingestion.py`), run `python scripts/copy_real_test_images.py`.

---

## Synthetic images (optional)

**Files:** `test_image_01.jpg` … `test_image_50.jpg` (random 224×224 JPEGs for UI/API testing).

**Regenerate:** `python scripts/create_test_images.py`.
