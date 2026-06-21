import boto3
import json
import os
from datetime import datetime

s3 = boto3.client('s3', region_name='ap-south-1')
sns = boto3.client('sns', region_name='ap-south-1')

BUCKET = os.getenv('S3_BUCKET', 'hybridguard-deepak')
SNS_ARN = os.getenv('SNS_TOPIC_ARN')

def upload_prediction_data(data):
    key = f"predictions/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    s3.put_object(Bucket=BUCKET, Key=key, Body=json.dumps(data))
    return key

def send_alert_message(message):
    sns.publish(
        TopicArn=SNS_ARN,
        Message=message,
        Subject="HybridGuard Alert - Anomaly Detected!"
    )
