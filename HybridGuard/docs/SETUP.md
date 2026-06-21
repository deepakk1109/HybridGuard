# Setup Guide — HybridGuard

## 1. Prerequisites

- Red Hat Developer account (developers.redhat.com)
- AWS account (aws.amazon.com/free)
- GitHub account
- Docker installed (WSL2/Linux)
- Python 3.11+
- `oc` CLI installed
- `aws` CLI installed

## 2. Clone & Local Run

```bash
git clone https://github.com/deepakk1109/HybridGuard.git
cd HybridGuard
python -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
```

Place your exported ONNX model at `models/fraud_model.onnx` (export it from
your existing CreditGuard scikit-learn RandomForest model using `skl2onnx`).

Set required environment variables before running locally:

```bash
export AWS_REGION=ap-south-1
export S3_BUCKET=hybridguard-deepak
export SNS_TOPIC_ARN=arn:aws:sns:ap-south-1:XXXX:hybridguard-alerts
export AWS_ACCESS_KEY_ID=YOUR_KEY
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET
```

Run the app:

```bash
uvicorn app.main:app --reload --port 8080
curl http://localhost:8080/health
```

## 3. Next Steps

- See `docs/AWS_SETUP.md` for S3/SNS/IAM setup
- See `docs/OPENSHIFT_SETUP.md` for deployment
- See `docs/JENKINS_SETUP.md` for CI/CD automation
