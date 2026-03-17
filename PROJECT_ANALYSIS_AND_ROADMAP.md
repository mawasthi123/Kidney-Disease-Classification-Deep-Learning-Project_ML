# Kidney Disease Classification – Project Analysis & DevOps Roadmap

**Role:** Senior DevOps Engineer  
**Purpose:** Full analysis, run/test plan, and completion checklist for the MLOps assignment.

**Scope for now:** Test and run **locally** (app, pipeline, tests, MLflow UI). **AWS (EC2, ECR, GitHub Actions CD) is skipped**; see `LOCAL_TESTING.md` for local-only steps.

---

## 1. Project Overview

| Item | Detail |
|------|--------|
| **Repo** | Kidney-Disease-Classification-Deep-Learning-Project (MLflow + DVC) |
| **Remote** | `origin` → https://github.com/mawasthi123/Kidney-Disease-Classification-Deep-Learning-Project_ML.git |
| **Stack** | Python 3.8, TensorFlow 2.12, Flask, DVC, MLflow, Docker, GitHub Actions → AWS (ECR + EC2) |
| **App** | Flask app on port **8080**: UI upload → base64 image → `/predict` → CNN (VGG16-based) → Normal/Tumor |

---

## 2. Repository Structure

```
.
├── app.py                    # Flask entry: /, /train, /predict
├── main.py                   # Runs full pipeline (data → base model → training → evaluation)
├── requirements.txt          # Python deps (tensorflow, flask, dvc, mlflow, gdown, etc.)
├── setup.py                  # Package cnnClassifier (src layout)
├── config/
│   └── config.yaml           # Artifacts paths, data URL, model paths
├── params.yaml               # Training params (EPOCHS=1, BATCH_SIZE=16, IMAGE_SIZE, etc.)
├── dvc.yaml                  # DVC pipeline: data_ingestion → prepare_base_model → training → evaluation
├── dvc.lock                  # Locked pipeline state
├── Dockerfile                # python:3.8-slim, COPY ., pip install, CMD app.py
├── model/
│   └── model.h5              # Trained model (used by app predict) — PRESENT
├── templates/
│   └── index.html            # Upload + Predict UI, calls /predict with base64
├── research/                 # Jupyter notebooks (01–04 + trials)
├── src/cnnClassifier/
│   ├── __init__.py           # Logger setup
│   ├── constants/            # CONFIG_FILE_PATH, PARAMS_FILE_PATH
│   ├── entity/               # DataIngestionConfig, PrepareBaseModelConfig, TrainingConfig, EvaluationConfig
│   ├── config/configuration.py  # ConfigurationManager → get_*_config()
│   ├── utils/common.py       # read_yaml, create_directories, save_json, decodeImage, etc.
│   ├── components/           # DataIngestion, PrepareBaseModel, ModelTrainer, Evaluation (MLflow)
│   └── pipeline/             # stage_01–04_*.py, prediction.py (PredictionPipeline)
└── .github/workflows/
    └── main.yaml             # CI (lint/tests) → build & push to ECR → CD (self-hosted: pull & run container)
```

**Important paths:**

- **Config:** `config/config.yaml`, `params.yaml`
- **App model:** `model/model.h5` (hardcoded in `prediction.py`)
- **Pipeline outputs:** `artifacts/data_ingestion/`, `artifacts/prepare_base_model/`, `artifacts/training/model.h5`
- **Scores:** `scores.json` (loss, accuracy from evaluation stage)
- **Logs:** `logs/running_logs.log`

---

## 3. Dependency & Config Summary

### 3.1 requirements.txt

- **tensorflow==2.12.0**, pandas, numpy, scipy, matplotlib, seaborn  
- **dvc**, **mlflow==2.2.2**, notebook  
- python-box==6.0.2, **pyYAML**, tqdm, ensure==1.0.2, joblib, types-PyYAML  
- **Flask**, **Flask-Cors**  
- **gdown** (Google Drive download for data)  
- **-e .** (install cnnClassifier from setup.py)

**Note (TensorFlow):** `tensorflow==2.12.0` may not be available on all platforms (e.g. Python 3.9+ or macOS ARM). If install fails, use `tensorflow>=2.13,<2.14` (or latest 2.x) and re-run `pip install -r requirements.txt` after relaxing the version in `requirements.txt`.

### 3.2 config/config.yaml

- `artifacts_root: artifacts`
- **data_ingestion:** Google Drive URL, `artifacts/data_ingestion/data.zip`, unzip → `artifacts/data_ingestion` (expects `kidney-ct-scan-image` after unzip)
- **prepare_base_model:** base_model.h5, base_model_updated.h5 under `artifacts/prepare_base_model`
- **training:** `artifacts/training/model.h5`

### 3.3 params.yaml

- IMAGE_SIZE: [224,224,3], BATCH_SIZE: 16, EPOCHS: 1, CLASSES: 2, AUGMENTATION: True, WEIGHTS: imagenet, LEARNING_RATE: 0.01

### 3.4 Data source

- **data_ingestion** uses **gdown** with `source_URL` from config (Google Drive file ID from URL).  
- DVC expects output: `artifacts/data_ingestion/kidney-ct-scan-image` (directory with train/validation structure).

---

## 4. Pipeline (DVC + main.py)

| Stage | Script | Deps | Outputs |
|-------|--------|------|--------|
| data_ingestion | stage_01_data_ingestion.py | config, script | artifacts/data_ingestion/kidney-ct-scan-image |
| prepare_base_model | stage_02_prepare_base_model.py | config, script, params | artifacts/prepare_base_model |
| training | stage_03_model_training.py | config, data, prepare_base_model, params | artifacts/training/model.h5 |
| evaluation | stage_04_model_evaluation.py | config, data, model.h5, params | scores.json (metrics) |

- **Run full pipeline:** `python main.py` or `dvc repro`
- **App “Train” route:** calls `python main.py` (no DVC repro by default)

---

## 5. Application (app.py)

- **Port:** 8080 (host 0.0.0.0 for AWS)
- **Routes:**
  - `GET /` → `templates/index.html`
  - `GET/POST /train` → runs `python main.py` → returns "Training done successfully!"
  - `POST /predict` → body `{"image": "<base64>"}` → decode to `inputImage.jpg` → `PredictionPipeline.predict()` → `model/model.h5` → Normal/Tumor
- **Prediction:** Uses `model/model.h5` only (not `artifacts/training/model.h5`). For consistency after training, either copy trained model to `model/model.h5` or point prediction to `artifacts/training/model.h5`.

---

## 6. CI/CD (.github/workflows/main.yaml)

- **Trigger:** push to `main`, ignore README.md
- **Jobs:**
  1. **integration:** checkout → “Lint code” → “Run unit tests” (placeholders: echo only)
  2. **build-and-push-ecr-image:** checkout → configure AWS → ECR login → docker build & push (IMAGE_TAG: latest)
  3. **Continuous-Deployment:** **self-hosted** runner → checkout → AWS config → ECR login → docker pull → docker run -d -p 8080:8080 (name=cnncls)

**Secrets required:**  
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `ECR_REPOSITORY_NAME`, `AWS_ECR_LOGIN_URI` (e.g. `566373416292.dkr.ecr.us-east-1.amazonaws.com`).

**Note:** CD uses `AWS_ECR_LOGIN_URI` and `ECR_REPOSITORY_NAME`; build uses `steps.login-ecr.outputs.registry` + `ECR_REPOSITORY_NAME`. Ensure ECR repo exists and URI format matches.

---

## 7. Issues & Fixes Identified

| # | Issue | Severity | Fix |
|---|--------|----------|-----|
| 1 | `get_evaluation_config()` passes `path_of_model` and `training_data` as str; `EvaluationConfig` expects `Path` | Medium | Use `Path(...)` in configuration.py for both (done in repo). |
| 2 | No real lint/unit tests in GitHub Actions | Low | Add pytest and a minimal test; optionally ruff/black. |
| 3 | App uses `model/model.h5`; pipeline writes `artifacts/training/model.h5` | Low | After `main.py`/DVC, copy `artifacts/training/model.h5` → `model/model.h5` or make prediction path configurable. |
| 4 | index.html predict URL: `value="../predict"` | Low | Relative URL can break depending on deployment; ensure same origin or use `/predict`. |
| 5 | README export of MLflow/Dagshub credentials | Security | Do not commit real credentials; use GitHub secrets / env in runner. |

---

## 8. Roadmap: Check, Test, Run, Complete

### Phase A – Environment & Dependencies

1. **Python 3.8**
   - Create venv: `python3.8 -m venv venv` (or conda `conda create -n cnncls python=3.8 -y`).
   - Activate: `source venv/bin/activate` or `conda activate cnncls`.

2. **Install**
   - `pip install -r requirements.txt`  
   - Resolve any platform-specific issues (e.g. TensorFlow on Apple Silicon: use `tensorflow-metal` or run on x86/CI).

3. **Editable package**
   - Ensure `pip install -e .` runs (setup.py, src layout).  
   - From repo root: `python -c "from cnnClassifier import logger; print('ok')"`.

### Phase B – Config & Code Fixes

4. **EvaluationConfig types**
   - In `src/cnnClassifier/config/configuration.py`, ensure `path_of_model` and `training_data` are `Path(...)` when building `EvaluationConfig` (see fixes below).

5. **Optional: model path**
   - Either copy `artifacts/training/model.h5` → `model/model.h5` after training, or add a config key for “prediction model path” and use it in `prediction.py`.

### Phase C – Pipeline Run (Full Training)

6. **Run DVC pipeline**
   - `dvc repro` (or `python main.py`).  
   - Requires network for data_ingestion (Google Drive).  
   - Produces: `artifacts/data_ingestion/kidney-ct-scan-image`, `artifacts/prepare_base_model`, `artifacts/training/model.h5`, `scores.json`.

7. **If only testing app (no training)**
   - Use existing `model/model.h5` and skip pipeline; run app only.

### Phase D – Application Run & Test

8. **Start app**
   - `python app.py`  
   - App listens on `http://0.0.0.0:8080`.

9. **Manual test**
   - Open `http://localhost:8080`.  
   - Upload a kidney CT image → Predict.  
   - Expect JSON with `"image": "Normal"` or `"Tumor"`.

10. **Optional: /train**
    - Call GET/POST `/train` only if you want to run full pipeline from the app (slow; use for integration test).

### Phase E – Docker

11. **Build & run locally**
    - `docker build -t kidney-cnn .`  
    - `docker run -p 8080:8080 kidney-cnn`  
    - Test `http://localhost:8080` and `/predict` as above.

### Phase F – CI/CD (skipped for local-only)

12. **GitHub Actions / AWS (EC2, ECR)** – **Skipped** for now. When you need it: set repo secrets, push to `main`, configure self-hosted runner for CD.

13. **Optional: real tests**
    - Local tests in `tests/test_local.py`; for CI add `pytest` and run in workflow.

### Phase G – Sign-off

14. **Checklist (local focus; AWS skipped)**
    - [x] Venv/conda + `pip install -r requirements.txt` + `pip install -e .` succeed.  
    - [x] `from cnnClassifier import logger` works.  
    - [x] Config/entity Path fix applied and evaluation stage runs.  
    - [x] Either pipeline runs (`dvc repro` or `python main.py`) or app runs with existing `model/model.h5`.  
    - [x] `python app.py` → UI loads, upload + predict returns Normal/Tumor.  
    - [x] **MLflow UI:** evaluation logs to `file:./mlruns`; run `mlflow ui` → http://localhost:5000 to view runs.  
    - [ ] Docker build & run (optional; skipped for local-only).  
    - [ ] GitHub Actions / EC2 / ECR (skipped for local-only).

---

## Completion status (as per assignment)

| Phase | Item | Status |
|-------|------|--------|
| **A** | Python venv created (`.venv`) | Done |
| **A** | `pip install -r requirements.txt` (TensorFlow relaxed to `>=2.12,<2.21`) | Done |
| **A** | Editable package `pip install -e .`, import `cnnClassifier` | Done |
| **B** | EvaluationConfig: `path_of_model` & `training_data` as `Path` in configuration.py | Done |
| **B** | Prediction: `load_model(..., compile=False)` for Keras 3 compatibility | Done |
| **C** | Data ingestion run: dataset downloaded & extracted to `artifacts/data_ingestion/kidney-ct-scan-image` | Done |
| **C** | Full pipeline (prepare_base_model → training → evaluation) | Not run (app uses existing `model/model.h5`) |
| **D** | App runs: `python app.py` on port 8080 | Done |
| **D** | Manual test: GET / → 200, POST /predict → Normal or Tumor | Done |
| **D** | Local tests: `tests/test_local.py` (config + prediction) | Done |
| **D** | Real test images: 25 Normal + 25 Tumor in `test_images/real_kidney_ct/` | Done |
| **D** | MLflow: evaluation logs to local `./mlruns`; `mlflow ui` for testing | Done (default `file:./mlruns`) |
| **E** | Docker build & run locally | Skipped (local-only) |
| **F** | GitHub Actions / EC2 / ECR | Skipped (local-only) |

**Extra deliverables:** `RUN_LOCAL.md`, `LOCAL_TEST_OUTPUT.md`, `LOCAL_TESTING.md` (local + MLflow, no AWS), `scripts/create_test_images.py`, `scripts/copy_real_test_images.py`, `test_images/README.md`.

---

## 9. Run & Test (Quick) – local only, no AWS

1. **Create venv and install:**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run tests:** `python tests/test_local.py`
3. **Run app:** `python app.py` → open http://localhost:8080 → Upload image → Predict.
4. **Optional full pipeline:** `python main.py` (writes to `artifacts/` and logs to MLflow).
5. **MLflow UI:** `mlflow ui` → open http://localhost:5000 to view experiments/runs (local store `./mlruns`).

See **LOCAL_TESTING.md** for the full local-only flow (AWS/EC2/ECR skipped).

---

## 10. Quick Commands Reference

```bash
# Environment
conda create -n cnncls python=3.8 -y && conda activate cnncls
# or: python3.8 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Package check
python -c "from cnnClassifier import logger; print('ok')"

# Full pipeline
python main.py
# or
dvc repro

# App
python app.py
# then open http://localhost:8080

# Docker
docker build -t kidney-cnn .
docker run -p 8080:8080 kidney-cnn

# MLflow UI (optional)
mlflow ui
```

---

## 11. Summary

- **App:** Flask on 8080, uses `model/model.h5` for `/predict`; `/train` runs `main.py`.  
- **Pipeline:** DVC 4-stage (data → base model → training → evaluation); data from Google Drive via gdown. Evaluation logs to **MLflow** (local `./mlruns` by default).  
- **Local testing:** Run app, run `tests/test_local.py`, run pipeline (optional), run `mlflow ui` to view runs. No AWS required; see **LOCAL_TESTING.md**.  
- **Deploy (later):** Docker → ECR and CD on EC2 are skipped for now; requirements are correct for local use.
