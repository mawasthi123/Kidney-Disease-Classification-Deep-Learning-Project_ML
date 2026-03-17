"""
Local tests: config load + prediction pipeline.
Run from project root: python tests/test_local.py
"""
import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_config():
    """Load configuration and check evaluation config has Path types."""
    from cnnClassifier.config.configuration import ConfigurationManager
    from pathlib import Path
    cm = ConfigurationManager()
    ec = cm.get_evaluation_config()
    assert isinstance(ec.path_of_model, Path), "path_of_model should be Path"
    assert isinstance(ec.training_data, Path), "training_data should be Path"
    print("[PASS] Config load and EvaluationConfig Path types OK")


def test_prediction():
    """Run prediction on inputImage.jpg if model and image exist."""
    try:
        from cnnClassifier.pipeline.prediction import PredictionPipeline
    except ImportError as e:
        print(f"[SKIP] Prediction (TensorFlow not installed): {e}")
        return
    model_path = os.path.join("model", "model.h5")
    image_path = "inputImage.jpg"
    if not os.path.isfile(model_path):
        print("[SKIP] model/model.h5 not found")
        return
    if not os.path.isfile(image_path):
        print("[SKIP] inputImage.jpg not found")
        return
    pipe = PredictionPipeline(image_path)
    result = pipe.predict()
    assert isinstance(result, list) and len(result) >= 1
    assert "image" in result[0]
    assert result[0]["image"] in ("Normal", "Tumor")
    print(f"[PASS] Prediction OK: {result[0]}")


if __name__ == "__main__":
    print("--- Local tests ---")
    test_config()
    test_prediction()
    print("--- All tests passed ---")
