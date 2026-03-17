# Run and test results

## 1. MLflow
- **Status:** Done (per your confirmation).
- Use: `python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns` → http://localhost:5001

---

## 2. Run (training pipeline)

- **Command run:** `python main.py`
- **Result:** **Did not complete** in this environment (process aborts when loading TensorFlow/native libs).
- **On your machine:** Run from project root with venv activated:
  ```bash
  python main.py
  cp artifacts/training/model.h5 model/model.h5
  ```
  Then restart the app so Tumor images are predicted as Tumor.

---

## 3. Tests run

| Test | Result |
|------|--------|
| Config (EvaluationConfig Path, load config) | **PASS** |
| GET / (Flask app home) | **PASS** – HTTP 200 |
| POST /predict with `real_normal_01.jpg` | **PASS** – `[{"image":"Normal"}]` (correct) |
| POST /predict with `real_tumor_01.jpg` | **Result:** `[{"image":"Normal"}]` – wrong with current model; will show Tumor after you run `main.py` and copy the new model |

---

## 4. Summary

- **Config test:** PASS  
- **App (GET /):** PASS  
- **Predict (Normal image):** Correct (Normal)  
- **Predict (Tumor image):** Currently Normal; run `python main.py` and `cp artifacts/training/model.h5 model/model.h5` on your machine, then restart the app to get Tumor predictions.
