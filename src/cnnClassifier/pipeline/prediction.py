import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Must match training: flow_from_directory sorts classes alphabetically -> Normal=0, Tumor=1
CLASS_NAMES = ["Normal", "Tumor"]


class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        # compile=False for legacy .h5 (Keras 3)
        model = load_model(os.path.join("model", "model.h5"), compile=False)
        test_image = image.load_img(self.filename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        proba = model.predict(test_image, verbose=0)[0]
        pred_idx = int(np.argmax(proba))
        prediction = CLASS_NAMES[pred_idx]
        confidence = float(proba[pred_idx])
        return [{"image": prediction, "confidence": round(confidence, 4)}]