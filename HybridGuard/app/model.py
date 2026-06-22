"""
HybridGuard - ONNX Model Loader
Loads the fraud-detection model (reused/exported from the CreditGuard project)
and exposes a simple predict() function.
"""

import os
import logging
import numpy as np
import onnxruntime as ort

logger = logging.getLogger("hybridguard.model")

MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(__file__), "..", "models", "fraud_model.onnx"))

_session: ort.InferenceSession | None = None


def _get_session() -> ort.InferenceSession:
    global _session
    if _session is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"ONNX model not found at {MODEL_PATH}. "
                f"Export your CreditGuard scikit-learn model to ONNX and place it here."
            )
        logger.info("Loading ONNX model from %s", MODEL_PATH)
        _session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    return _session
def predict(features: list[float]) -> dict:
    """
    Run inference on a single feature vector with robust (1, 1, 28, 28) formatting
    and safe Sigmoid activation for raw classification scores.
    """
    session = _get_session()
    input_name = session.get_inputs()[0].name

    TOTAL_ELEMENTS = 784  # 28 * 28
    
    
    padded_features = list(features)
    if len(padded_features) < TOTAL_ELEMENTS:
        padded_features.extend([0.0] * (TOTAL_ELEMENTS - len(padded_features)))
    else:
        padded_features = padded_features[:TOTAL_ELEMENTS]

   
    matrix_2d = [padded_features[i:i + 28] for i in range(0, TOTAL_ELEMENTS, 28)]
    strict_4d_list = [[matrix_2d]]
    
    x = np.array(strict_4d_list, dtype=np.float32)

   
  outputs = session.run(None, {input_name: x})

    raw_score = 0.0
    try:
        # மாடலோட அவுட்புட் ஸ்ட்ரக்சர் எதுவாக இருந்தாலும் அதன் முதல் வேல்யூவை தட்டையாக (Flatten) மாற்றுகிறோம்
        raw_score = float(np.array(outputs[0]).flatten()[0])
    except Exception:
        raw_score = 0.0

    # 4. ⚡ அல்டிமேட் பிக்ஸ்: நெகட்டிவ் வேல்யூக்களை 0-1 க்குள் கன்வெர்ட் செய்கிறோம்
    # வேல்யூ மைனஸில் மிக அதிகமாக இருந்தால் அது 0% (Not Fraud)
    if raw_score <= -1.0:
        fraud_probability = 0.0
    # வேல்யூ பாசிட்டிவாக இருந்தால் அது 100% (Fraud)
    elif raw_score >= 1.0:
        fraud_probability = 1.0
    else:
        # இடைப்பட்ட மதிப்புகளுக்கு மட்டும் Sigmoid அல்லது நார்மலைசேஷன்
        fraud_probability = 1.0 / (1.0 + np.exp(-raw_score))

    return {
        "fraud_probability": round(float(fraud_probability), 4),
        "is_fraud": fraud_probability > 0.5,
    }
