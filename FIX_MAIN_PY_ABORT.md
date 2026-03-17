# Fix: `python main.py` → "mutex lock failed" / Abort trap: 6

This crash on macOS is often due to TensorFlow loading in the main process. Use the subprocess runner so the main process never imports TensorFlow.

---

## 1. Use subprocess runner (recommended)

From project root with venv activated:

```bash
bash scripts/run_main.sh
```

This runs **main_subprocess.py**, which executes each pipeline stage in a **separate Python process** (so the runner never imports TensorFlow and avoids the crash).

Or directly:

```bash
export TF_NUM_INTEROP_THREADS=1
export TF_NUM_INTRAOP_THREADS=1
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
python main_subprocess.py
```

---

## 2. Or try env vars with original main.py

```bash
export TF_NUM_INTEROP_THREADS=1
export TF_NUM_INTRAOP_THREADS=1
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
python main.py
```

---

## 3. After `main.py` finishes successfully

Then copy the trained model for the app:

```bash
cp artifacts/training/model.h5 model/model.h5
```

Restart the app (`python app.py`) and test again. **Only run the copy after `main.py` has completed**; if it aborts, `artifacts/training/model.h5` may be missing or old.

---

## 4. If stage 2 or 3 still aborts (TensorFlow in any process)

**Use Docker** so training runs on Linux and avoids the macOS crash:

```bash
# Stage 1 already ran on your Mac (data is in artifacts/data_ingestion). Run only stages 2–4 in Docker:
bash scripts/run_train_in_docker.sh
```

Then copy the model and restart the app:

```bash
cp artifacts/training/model.h5 model/model.h5
python app.py
```

- **Requires Docker.** The script mounts your project into the container so `artifacts/training/model.h5` is written on your Mac.
- To run **all 4 stages** in Docker (e.g. clean run):  
  `docker build -t kidney .` then  
  `docker run --rm -v "$(pwd):/app" -w /app kidney python main_subprocess.py`
