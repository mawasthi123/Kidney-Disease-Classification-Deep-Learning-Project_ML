#!/usr/bin/env bash
# Run pipeline stages 2–4 (prepare base model, training, evaluation) in Docker.
# Use this when stage 2 aborts on macOS with "mutex lock failed".
# Requires: Docker. Stage 1 (data) must have run already on the host so artifacts/data_ingestion exists.
# From project root: bash scripts/run_train_in_docker.sh
set -e
cd "$(dirname "$0")/.."
if [ ! -d "artifacts/data_ingestion/kidney-ct-scan-image" ]; then
  echo "Run stage 1 first on the host: bash scripts/run_main.sh (will complete stage 1 only, then abort at 2)."
  echo "Or run full pipeline in Docker: docker run --rm -v \"$(pwd):/app\" -w /app \$(docker build -q .) python main_subprocess.py"
  exit 1
fi
echo "Building Docker image (first time can take 5–15 min due to TensorFlow)..."
IMAGE=$(docker build -q .)
echo "Running stages 2–4 in Docker (training may take 10–20 min)..."
docker run --rm -v "$(pwd):/app" -w /app "$IMAGE" python main_subprocess.py --from-stage 2
echo "Done. Copy model: cp artifacts/training/model.h5 model/model.h5"
