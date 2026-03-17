#!/usr/bin/env bash
# Run MLflow UI on port 5001 (5000 often used by macOS AirPlay).
# From project root: bash scripts/run_mlflow_ui.sh
# Then open: http://localhost:5001
cd "$(dirname "$0")/.."
mkdir -p mlruns
exec python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri "$(pwd)/mlruns"
