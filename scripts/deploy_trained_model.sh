#!/usr/bin/env bash
# Run after Docker training completes. Copies the new model into place for the app.
# Usage: bash scripts/deploy_trained_model.sh
set -e
cd "$(dirname "$0")/.."
SRC="artifacts/training/model.h5"
DEST="model/model.h5"
if [ ! -f "$SRC" ]; then
  echo "No trained model found at $SRC"
  echo "Run: bash scripts/run_train_in_docker.sh and wait for 'All stages completed'"
  exit 1
fi
cp "$SRC" "$DEST"
echo "Copied $SRC -> $DEST"
echo "Restart the app (python app.py) and test at http://localhost:8080"
