# Train the model with Docker (when stage 2 aborts on macOS)

Stage 1 (data ingestion) completed on your Mac. Stage 2 aborts with "mutex lock failed" when TensorFlow loads. Run **stages 2–4 in Docker** (Linux) so the model is trained and you get `artifacts/training/model.h5`.

---

## Prerequisites

- **Docker** installed and running.
- **Stage 1 already run** so `artifacts/data_ingestion/kidney-ct-scan-image` exists (you have this).

---

## Steps

From project root:

```bash
bash scripts/run_train_in_docker.sh
```

This will:

1. Build the Docker image (**first time can take 5–15 minutes** while TensorFlow downloads).
2. Run stages 2, 3, and 4 inside the container (prepare base model → training → evaluation; **training can take 10–20 minutes**).
3. Write `artifacts/training/model.h5` and `scores.json` into your project (via volume mount).

When it finishes:

```bash
cp artifacts/training/model.h5 model/model.h5
python app.py
```

Then open http://localhost:8080 and test with Tumor images; you should see **Tumor** when appropriate.

---

## If the script fails

Run manually:

```bash
docker build -t kidney .
docker run --rm -v "$(pwd):/app" -w /app kidney python main_subprocess.py --from-stage 2
cp artifacts/training/model.h5 model/model.h5
```
