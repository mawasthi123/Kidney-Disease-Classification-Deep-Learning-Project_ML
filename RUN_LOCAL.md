# Run & Test Locally

## 1. One-time setup

```bash
cd /path/to/Kidney-Disease-Classification-Deep-Learning-Project-main

# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies (TensorFlow may take a few minutes)
pip install -r requirements.txt
```

If `tensorflow` install fails (e.g. on Apple Silicon or Python 3.10+), the app and prediction test will be skipped until TensorFlow is installed. Config test will still run.

## 2. Run tests

From project root:

```bash
source .venv/bin/activate
python tests/test_local.py
```

- **Config test:** Loads `config/config.yaml` and `params.yaml`, checks `EvaluationConfig` uses `Path` types.
- **Prediction test:** Runs model on `inputImage.jpg` if `model/model.h5` and TensorFlow are present.

## 3. Run the Flask app

```bash
source .venv/bin/activate
python app.py
```

Then open **http://localhost:8080** in a browser: upload an image and click Predict.

## 4. Test /predict with curl (app must be running)

Encode a test image to base64 and POST:

```bash
# With a test image (e.g. inputImage.jpg)
IMAGE_B64=$(base64 -i inputImage.jpg | tr -d '\n')
curl -s -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$IMAGE_B64\"}"
```

Expected response: `[{"image": "Normal"}]` or `[{"image": "Tumor"}]`.

**Note:** If you use TensorFlow 2.13+ (Keras 3), the app loads the legacy `model.h5` with `compile=False` to avoid deserialization errors.

## 5. Optional: full pipeline (training)

```bash
source .venv/bin/activate
python main.py
```

Requires network (downloads data from Google Drive). Writes to `artifacts/` and `scores.json`. To use the new model in the app, copy:

```bash
cp artifacts/training/model.h5 model/model.h5
```

## Quick checklist

| Step              | Command / action                    |
|-------------------|-------------------------------------|
| Install deps      | `pip install -r requirements.txt`   |
| Run tests         | `python tests/test_local.py`        |
| Start app         | `python app.py`                     |
| Open UI           | http://localhost:8080               |
| Test /predict     | curl POST with base64 image (see above) |
