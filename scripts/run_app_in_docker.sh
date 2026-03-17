#!/usr/bin/env bash
# Run the Flask app in Docker (avoids "mutex lock failed" / Abort trap: 6 on macOS).
# From project root: bash scripts/run_app_in_docker.sh
# Then open http://localhost:8080
set -e
cd "$(dirname "$0")/.."
if [ ! -f "model/model.h5" ]; then
  echo "No model at model/model.h5. Run training first, then: bash scripts/deploy_trained_model.sh"
  exit 1
fi
echo "Building Docker image (if needed)..."
IMAGE=$(docker build -q .)
echo "Starting app at http://localhost:8080 ..."
docker run --rm -p 8080:8080 -v "$(pwd):/app" -w /app "$IMAGE" python3 app.py
