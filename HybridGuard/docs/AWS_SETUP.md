# AWS Setup Guide — HybridGuard

> Note: CloudWatch is intentionally NOT used in this project to avoid
> AWS Free Tier billing risk. Use Prometheus + Grafana (OpenShift) instead.

## 1. Create IAM User

AWS Console → IAM → Users → Create User

- Username: `hybridguard-svc`
- Permissions: `AmazonS3FullAccess`, `AmazonSNSFullAccess`
- Do NOT attach `CloudWatchFullAccess`
- Download the Access Key CSV and store it securely (never commit to Git)

## 2. Configure AWS CLI

```bash
aws configure
# AWS Access Key ID: <from CSV>
# AWS Secret Access Key: <from CSV>
# Default region: ap-south-1
# Default output format: json

aws sts get-caller-identity   # verify
```

## 3. Create S3 Bucket

```bash
aws s3 mb s3://hybridguard-deepak --region ap-south-1
aws s3api put-object --bucket hybridguard-deepak --key predictions/
```

## 4. Create SNS Topic + Subscribe Email

```bash
aws sns create-topic --name hybridguard-alerts --region ap-south-1
# copy the TopicArn from the output

aws sns subscribe \
  --topic-arn arn:aws:sns:ap-south-1:XXXX:hybridguard-alerts \
  --protocol email \
  --notification-endpoint your@email.com
```

Check your email and confirm the subscription.

## 5. Inject Credentials into OpenShift (Secret, not ConfigMap)

```bash
oc create secret generic aws-credentials \
  --from-literal=AWS_ACCESS_KEY_ID=YOUR_KEY \
  --from-literal=AWS_SECRET_ACCESS_KEY=YOUR_SECRET \
  -n deepakkrishnamoorthi
```
