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
                "Export your CreditGuard scikit-learn model to ONNX and place it here."
            )
        logger.info("Loading ONNX model from %s", MODEL_PATH)
        _session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    return _session


def predict(features: list[float]) -> dict:
    """
    Run inference on a single feature vector.

    Returns:
        {"fraud_probability": float, "is_fraud": bool}
    """
    session = _get_session()
    input_name = session.get_inputs()[0].name

    x = np.array([features], dtype=np.float32)
    outputs = session.run(None, {input_name: x})

    # Most sklearn-onnx classifiers return [labels, probabilities]
    # probabilities is usually a list of dicts like [{0: 0.9, 1: 0.1}]
    fraud_probability = 0.0
    try:
        proba = outputs[1]
        if isinstance(proba, list) and isinstance(proba[0], dict):
            fraud_probability = float(proba[0].get(1, 0.0))
        else:
            # fallback: assume proba is an array [[p0, p1]]
            fraud_probability = float(np.array(proba)[0][-1])
    except (IndexError, KeyError, TypeError):
        # fallback: use the raw label output as a 0/1 probability
        label = outputs[0][0]
        fraud_probability = float(label)

    return {
        "fraud_probability": round(fraud_probability, 4),
        "is_fraud": fraud_probability > 0.5,
    }
