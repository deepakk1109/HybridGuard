"""
HybridGuard - FastAPI Application
Hybrid Cloud Fraud/Anomaly Detection Microservice
Runs on Red Hat OpenShift, integrates with AWS S3 + SNS (no CloudWatch).
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import logging


from model import predict
from aws_utils import upload_prediction, send_alert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hybridguard")

app = FastAPI(
    title="HybridGuard API",
    description="Hybrid Cloud (OpenShift + AWS) Fraud Detection Service",
    version="1.0.0",
)

# ---- Prometheus metrics ----
PREDICTIONS_TOTAL = Counter("predictions_total", "Total number of predictions made")
ANOMALIES_TOTAL = Counter("anomalies_total", "Total number of anomalies/fraud detected")
PREDICTION_LATENCY = Histogram("prediction_latency_seconds", "Time taken to run a prediction")

# Threshold above which we treat a prediction as fraud and trigger an alert
FRAUD_ALERT_THRESHOLD = 0.8


class PredictionRequest(BaseModel):
    features: list[float] = Field(
        ..., description="Numeric feature vector for the fraud model", min_length=1
    )


class PredictionResponse(BaseModel):
    fraud_probability: float
    is_fraud: bool
    s3_key: str


@app.get("/health")
def health():
    """Basic liveness/readiness check used by OpenShift probes."""
    return {"status": "ok", "platform": "OpenShift + AWS", "service": "HybridGuard"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(payload: PredictionRequest):
    """
    Run fraud/anomaly detection on the given feature vector.
    Steps:
      1. Run ONNX model inference
      2. Upload the prediction result to AWS S3
      3. If fraud probability crosses threshold, publish an AWS SNS alert
    """
    start = time.time()
    try:
        # ---- 🛠️ இன்புட்டை இங்கேயே 4D லிஸ்ட்டாக மாற்றுகிறோம் ----
        # வெளியிலிருந்து வரும் [5000.0, 1.0, 0.0, 23.5] ஐ [[[[5000.0, 1.0, 0.0, 23.5]]]] ஆக மாற்றுகிறது
        input_4d = [[[[float(x) for x in payload.features]]]]
        
        # 4D இன்புட்டை மாடலுக்கு அனுப்புகிறோம்
        result = predict(input_4d)
    except Exception as exc:
        logger.exception("Model inference failed")
        raise HTTPException(status_code=500, detail=f"Inference error: {exc}") from exc
    finally:
        PREDICTION_LATENCY.observe(time.time() - start)

    PREDICTIONS_TOTAL.inc()

    record = {
        "input_features": payload.features,
        "fraud_probability": result["fraud_probability"],
        "is_fraud": result["is_fraud"],
    }

    try:
        s3_key = upload_prediction(record)
    except Exception as exc:
        logger.exception("Failed to upload prediction to S3")
        s3_key = "upload-failed"

    if result["is_fraud"] or result["fraud_probability"] > FRAUD_ALERT_THRESHOLD:
        ANOMALIES_TOTAL.inc()
        try:
            send_alert(
                f"HybridGuard Alert: fraud_probability={result['fraud_probability']:.3f} "
                f"for input={payload.features}"
            )
        except Exception:
            logger.exception("Failed to send SNS alert")

    return PredictionResponse(
        fraud_probability=result["fraud_probability"],
        is_fraud=result["is_fraud"],
        s3_key=s3_key,
    )
# @app.post("/predict", response_model=PredictionResponse)
# async def predict_endpoint(payload: PredictionRequest):
#     """
#     Run fraud/anomaly detection on the given feature vector.
#     Steps:
#       1. Run ONNX model inference
#       2. Upload the prediction result to AWS S3
#       3. If fraud probability crosses threshold, publish an AWS SNS alert
#     """
#     start = time.time()
#     try:
#         result = predict(payload.features)
#     except Exception as exc:
#         logger.exception("Model inference failed")
#         raise HTTPException(status_code=500, detail=f"Inference error: {exc}") from exc
#     finally:
#         PREDICTION_LATENCY.observe(time.time() - start)

#     PREDICTIONS_TOTAL.inc()

#     record = {
#         "input_features": payload.features,
#         "fraud_probability": result["fraud_probability"],
#         "is_fraud": result["is_fraud"],
#     }

#     try:
#         s3_key = upload_prediction(record)
#     except Exception as exc:
#         logger.exception("Failed to upload prediction to S3")
#         s3_key = "upload-failed"

#     if result["is_fraud"] or result["fraud_probability"] > FRAUD_ALERT_THRESHOLD:
#         ANOMALIES_TOTAL.inc()
#         try:
#             send_alert(
#                 f"HybridGuard Alert: fraud_probability={result['fraud_probability']:.3f} "
#                 f"for input={payload.features}"
#             )
#         except Exception:
#             logger.exception("Failed to send SNS alert")

    # return PredictionResponse(
    #     fraud_probability=result["fraud_probability"],
    #     is_fraud=result["is_fraud"],
    #     s3_key=s3_key,
    # )


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    """Prometheus scrape endpoint."""
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
