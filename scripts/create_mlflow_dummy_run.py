"""
Create a dummy MLflow run so the UI has something to show at http://localhost:5000.
Run from project root: python scripts/create_mlflow_dummy_run.py
Then run: mlflow ui --host 0.0.0.0 --port 5000 --backend-store-uri file:./mlruns
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    try:
        import mlflow
    except ImportError as e:
        print("Install: pip install mlflow opentelemetry-api opentelemetry-sdk cachetools")
        raise SystemExit(1) from e
    os.makedirs("mlruns", exist_ok=True)
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("kidney-classification")
    with mlflow.start_run(run_name="dummy-run"):
        mlflow.log_param("EPOCHS", 5)
        mlflow.log_param("BATCH_SIZE", 16)
        mlflow.log_metric("loss", 0.5)
        mlflow.log_metric("accuracy", 0.85)
    print("Dummy run created in ./mlruns")
    print("Start UI: python -m mlflow ui --host 127.0.0.1 --port 5001 --backend-store-uri file:./mlruns")
    print("Then open: http://localhost:5001")

if __name__ == "__main__":
    main()
