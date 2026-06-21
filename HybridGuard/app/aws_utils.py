"""
HybridGuard - AWS Integration Layer
Uses boto3 to talk to S3 (storage) and SNS (alerts).
CloudWatch is intentionally NOT used to avoid AWS Free Tier billing risk -
Prometheus + Grafana (built into OpenShift) handle monitoring instead.
"""

import os
import json
import logging
from datetime import datetime

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger("hybridguard.aws")

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
S3_BUCKET = os.getenv("S3_BUCKET", "hybridguard-deepak")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "")

# boto3 will automatically pick up AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
# from environment variables (injected via OpenShift Secret) or from
# the default credentials chain - never hardcode keys here.
s3_client = boto3.client("s3", region_name=AWS_REGION)
sns_client = boto3.client("sns", region_name=AWS_REGION)


def upload_prediction(data: dict) -> str:
    """
    Upload a prediction record to S3 under predictions/<timestamp>.json
    Returns the S3 object key.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    key = f"predictions/{timestamp}.json"

    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=json.dumps(data, default=str),
            ContentType="application/json",
        )
        logger.info("Uploaded prediction to s3://%s/%s", S3_BUCKET, key)
    except (BotoCoreError, ClientError):
        logger.exception("S3 upload failed")
        raise

    return key


def send_alert(message: str) -> None:
    """
    Publish an alert message to the configured SNS topic.
    Subscribers (e.g. your email) will receive it instantly.
    """
    if not SNS_TOPIC_ARN:
        logger.warning("SNS_TOPIC_ARN not configured - skipping alert: %s", message)
        return

    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="HybridGuard Alert - Anomaly Detected!",
        )
        logger.info("SNS alert sent")
    except (BotoCoreError, ClientError):
        logger.exception("SNS publish failed")
        raise
