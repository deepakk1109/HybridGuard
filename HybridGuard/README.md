# HybridGuard — OpenShift × AWS Hybrid Cloud Fraud Detection Platform

A hybrid cloud monitoring & fraud detection platform combining **Red Hat OpenShift**
(container orchestration) with **AWS Free Tier** services (S3, SNS, IAM), automated
via **GitHub + Jenkins** CI/CD. Built entirely on free-tier resources — **₹0/month**.

## Architecture

```
GitHub (push) --webhook--> Jenkins --build/push--> Docker Hub
                                          |
                                          v
                              OpenShift Developer Sandbox
                              ├── FastAPI app (Deployment)
                              ├── Route (public HTTPS)
                              └── Prometheus + Grafana (metrics)
                                          |
                                          v
                              AWS Free Tier (S3 + SNS + IAM)
                              (CloudWatch intentionally NOT used)
```

## Tech Stack

| Layer | Technology |
|---|---|
| Source Control | GitHub |
| CI/CD | Jenkins (self-hosted, open source) |
| Container Platform | Red Hat OpenShift (Developer Sandbox) |
| Image Registry | Docker Hub |
| Cloud Storage | AWS S3 |
| Cloud Alerting | AWS SNS |
| Cloud Security | AWS IAM |
| Monitoring | Prometheus + Grafana (OpenShift built-in) |
| API Framework | FastAPI (Python) |
| ML Inference | ONNX Runtime |

## Free Tier Cost Breakdown

| Service | Free Tier | Cost/Month |
|---|---|---|
| OpenShift Sandbox | 30 days, renewable | ₹0 |
| AWS S3 (5GB) | 12 months free | ₹0 |
| AWS SNS | 1,000 emails free | ₹0 |
| AWS IAM | Always free | ₹0 |
| Prometheus + Grafana | Built into OCP | ₹0 |
| GitHub | Unlimited public repos | ₹0 |
| Jenkins | Open source | ₹0 |
| Docker Hub | Public images | ₹0 |
| **Total** | | **₹0/month** |

## Project Structure

```
HybridGuard/
├── app/
│   ├── main.py          # FastAPI app (/health, /predict, /metrics)
│   ├── model.py          # ONNX model loader
│   ├── aws_utils.py      # boto3 S3 + SNS integration
│   └── requirements.txt
├── models/
│   └── fraud_model.onnx  # exported from CreditGuard
├── openshift/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── route.yaml
│   └── servicemonitor.yaml
├── docs/
│   ├── SETUP.md
│   ├── AWS_SETUP.md
│   ├── JENKINS_SETUP.md
│   └── OPENSHIFT_SETUP.md
├── Dockerfile
├── Jenkinsfile
├── .gitignore
└── README.md
```

## Quick Start (Local)

```bash
git clone https://github.com/deepakk1109/HybridGuard.git
cd HybridGuard

python -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt

uvicorn app.main:app --reload --port 8080

curl http://localhost:8080/health
```

## Documentation

- [Setup Guide](docs/SETUP.md)
- [AWS Configuration](docs/AWS_SETUP.md)
- [OpenShift Deployment](docs/OPENSHIFT_SETUP.md)
- [Jenkins Pipeline](docs/JENKINS_SETUP.md)

## Notes

- **CloudWatch is intentionally not used** to avoid AWS Free Tier billing risk.
  Monitoring is handled by Prometheus + Grafana, both built into OpenShift at no cost.
- Never commit AWS credentials. Use Jenkins Credentials Store (for the pipeline)
  and OpenShift Secrets (for the running app).

## License

MIT License — see [LICENSE](LICENSE)
