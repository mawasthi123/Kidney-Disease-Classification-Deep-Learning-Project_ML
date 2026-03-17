# Project status – what’s done and what’s pending

## Done

| Area | Status |
|------|--------|
| **Repo** | Connected; structure and config reviewed |
| **Config** | `configuration.py`: EvaluationConfig uses `Path`; MLflow default `file:./mlruns` |
| **Prediction** | `prediction.py`: `compile=False`, returns `image` + `confidence`; `CLASS_NAMES` correct |
| **UI** | `templates/index.html`: shows Prediction + Confidence; no `res[1]` |
| **Params** | `params.yaml`: EPOCHS=5 for better training |
| **Data** | Stage 1 run: `artifacts/data_ingestion/kidney-ct-scan-image` (Normal/ + Tumor/) |
| **Test images** | 50 real images in `test_images/real_kidney_ct/` (25 Normal, 25 Tumor) |
| **Tests** | `tests/test_local.py` (config + prediction); config path fixed |
| **App** | Runs on 8080; GET / and POST /predict work |
| **MLflow UI** | Port **5001** (not 5000); `create_mlflow_dummy_run.py`; docs updated |
| **macOS crash** | Training/app abort with TensorFlow mutex; `run_train_in_docker.sh`, `run_app_in_docker.sh` to run in Docker |
| **Docker** | Dockerfile: Python 3.10 Bookworm, build deps (h5py/zoneinfo), pip timeout 300s; `run_train_in_docker.sh` for stages 2–4 |
| **Training** | `model_training.py`: compile() before fit() (Keras 3); `TrainingConfig` + `params_learning_rate` added |
| **Docs** | PROJECT_ANALYSIS_AND_ROADMAP, LOCAL_TESTING, FIX_MAIN_PY_ABORT, FIX_MLFLOW_AND_TUMOR, TRAIN_WITH_DOCKER, RUN_AND_TEST_RESULTS |

---

## Pending (for you to run/check)

| # | Item | How to do it |
|---|------|----------------|
| 1 | **Train model (Tumor detection)** | On macOS, stage 2 aborts; use Docker: `bash scripts/run_train_in_docker.sh` (first build 5–15 min, then training 10–20 min). |
| 2 | **Use new model in app** | After (1) finishes: `bash scripts/deploy_trained_model.sh` (or `cp artifacts/training/model.h5 model/model.h5`) then restart `python app.py`. |
| 3 | **Verify Tumor prediction** | Open http://localhost:8080, upload e.g. `test_images/real_kidney_ct/real_tumor_01.jpg`, click Predict → should show **Tumor** (and confidence). |
| 4 | **MLflow UI** | `python scripts/create_mlflow_dummy_run.py` then `python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns` → open http://localhost:5001. |
| 5 | **Optional: Docker build** | If `run_train_in_docker.sh` was never run to completion, run it once and wait for “All stages completed.” |

---

## Quick checklist

- [ ] Run `bash scripts/run_train_in_docker.sh` and wait until it finishes (no abort).
- [ ] Run `bash scripts/deploy_trained_model.sh` (or `cp artifacts/training/model.h5 model/model.h5`).
- [ ] Run app: on macOS use `bash scripts/run_app_in_docker.sh` (or `python app.py` on Linux); test at http://localhost:8080 with Normal and Tumor images.
- [ ] MLflow UI: run create dummy run + `mlflow ui` on port 5001; open http://localhost:5001.

---

## Current blockers / notes

- **macOS:** `python main.py` and `python app.py` abort (mutex lock failed / Abort trap: 6). Use Docker: training → `bash scripts/run_train_in_docker.sh`; app → `bash scripts/run_app_in_docker.sh`.
- **artifacts/training/model.h5:** Created only after a full Docker run finishes (stages 2→3→4); training ~10–20 min. Does not exist until Docker training (or a successful native run) completes. Until then, app uses existing `model/model.h5` (old model → often “Normal” only).
- **MLflow:** Use port **5001** and `--backend-store-uri file:./mlruns` so the UI is reachable.
- **Run to completion:** Run `bash scripts/run_train_in_docker.sh` in a terminal and wait for "All stages completed" before running the `cp` command.

---

## Where to look for help

- **Train with Docker:** `TRAIN_WITH_DOCKER.md`, `scripts/run_train_in_docker.sh`
- **Run app on macOS:** `scripts/run_app_in_docker.sh` (avoids TensorFlow mutex crash)
- **Main.py / stage 2 crash:** `FIX_MAIN_PY_ABORT.md`
- **MLflow + Tumor fix:** `FIX_MLFLOW_AND_TUMOR.md`
- **Local run/test:** `LOCAL_TESTING.md`, `PROJECT_ANALYSIS_AND_ROADMAP.md`
