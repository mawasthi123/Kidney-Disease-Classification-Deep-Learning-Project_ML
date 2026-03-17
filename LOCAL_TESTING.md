# Local testing only (no AWS / EC2 / ECR)

Use this guide to run and test everything **locally**. AWS (EC2, ECR, GitHub Actions CD) is **skipped**; you can add it later.

---

## Quick fix and test (two things)

**1. Prediction + Confidence in the app**

- Start app: `python app.py` → open **http://localhost:8080**
- Upload an image (e.g. from `test_images/real_kidney_ct/`) → click **Predict**
- You should see **Prediction: Normal** or **Prediction: Tumor** and **Confidence: XX%**
- If it always shows Normal, retrain and replace the model: run `python main.py`, then `cp artifacts/training/model.h5 model/model.h5`, restart the app.

**2. MLflow UI**

- Create a run (so the UI has something to show):  
  `python scripts/create_mlflow_dummy_run.py`  
  (If it says "Install...", run: `pip install mlflow opentelemetry-api opentelemetry-sdk cachetools`)
- Start the UI (use port **5001**; 5000 is often taken by macOS AirPlay):  
  `python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns`
- Open **http://localhost:5001** in your browser.

Or run once: `python scripts/setup_mlflow_and_test.py` — it creates the dummy run and prints these commands.

---

## Requirements (already in requirements.txt)

All needed for local run and MLflow UI:

- **App:** Flask, Flask-Cors, tensorflow, python-box, PyYAML, ensure, joblib
- **Pipeline:** gdown, dvc, mlflow, pandas, numpy, etc.
- **No AWS SDK or ECR-specific deps** are required for local testing.

If something fails to install, relax the version (e.g. `tensorflow>=2.12,<2.21` is already in place).

---

## 1. Environment

```bash
cd /path/to/Kidney-Disease-Classification-Deep-Learning-Project-main
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2. Run tests

```bash
python tests/test_local.py
```

You should see: config PASS, prediction PASS (if `model/model.h5` exists).

---

## 3. Run the Flask app

```bash
python app.py
```

- Open **http://localhost:8080**
- Upload an image from `test_images/real_kidney_ct/` (e.g. `real_normal_01.jpg` or `real_tumor_01.jpg`)
- Click **Predict** and check Normal/Tumor

---

## 4. Run pipeline and log to MLflow (local)

MLflow tracking is set to **local** by default (`file:./mlruns`). No Dagshub or AWS needed.

**Option A – Full pipeline (data already present):**

```bash
python main.py
```

This runs: data ingestion → prepare base model → training → evaluation. The **evaluation** stage writes `scores.json` and **logs to MLflow** (./mlruns).

**Option B – Only evaluation** (if you already have `artifacts/training/model.h5` and `artifacts/data_ingestion/kidney-ct-scan-image`):

```bash
python src/cnnClassifier/pipeline/stage_04_model_evaluation.py
```

**Optional – use a different local folder for MLflow:**

```bash
export MLFLOW_TRACKING_URI=file:./my_mlruns
python main.py
```

---

## 5. MLflow UI (local)

Use this so the UI is reachable at **http://localhost:5000** (and from other devices on your network if needed):

```bash
# From project root. Use port 5001 (5000 is often used by macOS AirPlay).
python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns
```

Then open **http://localhost:5001** in your browser.

- If you have no runs yet, create a dummy run so the UI has something to show:
  ```bash
  python scripts/create_mlflow_dummy_run.py
  ```
- After running the full pipeline (`python main.py`), the evaluation stage will log real runs (params + metrics) to `./mlruns`.

---

## 6. Prediction always shows "Normal"?

- The app shows **Prediction** and **Confidence** for each upload. If the current model almost always predicts "Normal", it was likely trained with very few epochs (e.g. 1).
- **Fix:** Retrain with more epochs: in `params.yaml` set `EPOCHS: 5` (or higher), then run `python main.py`. After it finishes, copy the new model so the app uses it:
  ```bash
  cp artifacts/training/model.h5 model/model.h5
  ```
- Then restart the app and test again with images from `test_images/real_kidney_ct/` (e.g. `real_tumor_01.jpg`).

---

## 7. Quick checklist (local only)

| Step | Command / action |
|------|------------------|
| Install | `pip install -r requirements.txt` |
| Tests | `python tests/test_local.py` |
| App | `python app.py` → http://localhost:8080 → Upload → Predict |
| Pipeline | `python main.py` (optional; needs data in `artifacts/`) |
| MLflow UI | `python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns` → http://localhost:5001 |

---

## Skipped for now (can add later)

- **Docker** build/run
- **GitHub Actions** (CI/CD)
- **AWS:** ECR, EC2, self-hosted runner

Requirements are correct for local run and MLflow; no changes needed for “local-only” mode.
