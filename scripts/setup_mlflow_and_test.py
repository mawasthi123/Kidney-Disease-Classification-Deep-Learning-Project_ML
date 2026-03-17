"""
1. Create MLflow dummy run (so UI has something to show).
2. Print exact commands to run MLflow UI and test app + prediction.

Run from project root: python scripts/setup_mlflow_and_test.py
"""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)
sys.path.insert(0, REPO_ROOT)


def create_mlflow_run():
    try:
        import mlflow
    except ImportError as e:
        print("Install MLflow deps: pip install mlflow opentelemetry-api opentelemetry-sdk cachetools")
        raise SystemExit(1) from e
    os.makedirs("mlruns", exist_ok=True)
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("kidney-classification")
    with mlflow.start_run(run_name="dummy-run"):
        mlflow.log_param("EPOCHS", 5)
        mlflow.log_param("BATCH_SIZE", 16)
        mlflow.log_metric("loss", 0.48)
        mlflow.log_metric("accuracy", 0.85)
    print("Created dummy run in ./mlruns")


def main():
    print("--- MLflow setup ---")
    create_mlflow_run()
    print()
    print("--- 1. Start MLflow UI (run this in a terminal) ---")
    print("  python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns")
    print("  Then open: http://localhost:5001")
    print()
    print("--- 2. Prediction & Confidence in the app ---")
    print("  Start app: python app.py")
    print("  Open: http://localhost:8080")
    print("  Upload an image from test_images/real_kidney_ct/ and click Predict.")
    print("  You should see 'Prediction: Normal' or 'Prediction: Tumor' and 'Confidence: XX%'.")
    print()
    print("--- 3. If prediction is always Normal, retrain then replace model ---")
    print("  python main.py")
    print("  cp artifacts/training/model.h5 model/model.h5")
    print("  Restart app and test again.")


if __name__ == "__main__":
    main()
