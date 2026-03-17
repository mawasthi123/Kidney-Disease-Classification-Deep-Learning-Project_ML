#!/usr/bin/env bash
# 1. Run full pipeline (train model).
# 2. Copy trained model so the app uses it (Tumor will then be detected).
# 3. Create MLflow dummy run if needed.
# 4. Print how to start MLflow UI.
# From project root: bash scripts/train_and_use_model.sh
set -e
cd "$(dirname "$0")/.."
echo ">>> Running full pipeline (this may take several minutes)..."
# Use run_main.sh to avoid mutex/Abort trap on macOS
bash scripts/run_main.sh || python main.py
echo ">>> Copying trained model to model/model.h5 for the app..."
cp -f artifacts/training/model.h5 model/model.h5
echo ">>> Creating MLflow run so UI has data..."
python scripts/create_mlflow_dummy_run.py 2>/dev/null || true
echo ""
echo "Done. Next:"
echo "  1. Start MLflow UI:  python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns"
echo "     Then open: http://localhost:5001"
echo "  2. Restart the app (python app.py) and test with Tumor images from test_images/real_kidney_ct/"
