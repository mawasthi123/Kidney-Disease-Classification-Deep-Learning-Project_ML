# Local run – test output

Summary of running and testing the project locally.

---

## 1. Tests (`python tests/test_local.py`)

```
--- Local tests ---
[INFO] common: yaml file: config/config.yaml loaded successfully
[INFO] common: yaml file: params.yaml loaded successfully
[INFO] common: created directory at: artifacts
[PASS] Config load and EvaluationConfig Path types OK
[PASS] Prediction OK: {'image': 'Normal'}
--- All tests passed ---
```

---

## 2. Flask app

- **Start:** `python app.py` → server on `http://0.0.0.0:8080`
- **GET /**  
  - `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/`  
  - **Result:** `200`
- **POST /predict** (body: `{"image": "<base64 of inputImage.jpg>"}`)  
  - **Result:** `[{"image":"Normal"}]`

---

## 3. Changes made for local run

| Item | Change |
|------|--------|
| **requirements.txt** | `tensorflow==2.12.0` → `tensorflow>=2.12,<2.21` for install on current Python/macOS |
| **prediction.py** | `load_model(..., compile=False)` so legacy `model.h5` loads under Keras 3 |
| **configuration.py** | `path_of_model` and `training_data` passed as `Path(...)` in `get_evaluation_config()` |
| **tests/test_local.py** | Added; runs config + prediction tests; skips prediction if TensorFlow missing |
| **RUN_LOCAL.md** | Added; steps to install, test, run app, and call /predict |

---

## 4. Quick commands (from project root)

```bash
source .venv/bin/activate
python tests/test_local.py
python app.py
# In another terminal:
curl http://localhost:8080/
IMAGE_B64=$(base64 -i inputImage.jpg | tr -d '\n')
curl -s -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d "{\"image\": \"$IMAGE_B64\"}"
```
