# Fix: MLflow UI access + Tumor detection (always Normal)

Do these steps **on your machine** (from project root, with venv activated).

---

## 1. MLflow UI not accessible

**Use port 5001** (port 5000 is often used by macOS AirPlay).

```bash
# Create a run so the UI has something to show
python scripts/create_mlflow_dummy_run.py

# Start MLflow UI
python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns
```

Then open **http://localhost:5001** in your browser.

- If you get "Install...", run: `pip install mlflow opentelemetry-api opentelemetry-sdk cachetools`
- Or run: `bash scripts/run_mlflow_ui.sh` (same command, port 5001)

---

## 2. Prediction always "Normal" – train and use new model

The app uses `model/model.h5`. If that model was trained with 1 epoch, it will predict Normal for almost everything. **Train a new model and copy it** so the app uses it:

```bash
# Run full pipeline (downloads data if needed, trains for 5 epochs). Takes several minutes.
python main.py

# Use the new model in the app
cp artifacts/training/model.h5 model/model.h5
```

Then **restart the app** (`python app.py`) and test again with images from `test_images/real_kidney_ct/` (e.g. `real_tumor_01.jpg`). You should see **Tumor** when the image is a tumor.

**One-shot script (same as above):**

```bash
bash scripts/train_and_use_model.sh
```

After it finishes, start MLflow UI (step 1) and restart the app.

---

## 3. Summary

| Issue | Fix |
|-------|-----|
| MLflow UI not accessible | Use **port 5001** and **127.0.0.1**: `python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns` → open http://localhost:5001 |
| Always "Normal" | Run `python main.py`, then `cp artifacts/training/model.h5 model/model.h5`, restart app |
