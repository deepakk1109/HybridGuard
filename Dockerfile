FROM python:3.11-slim
WORKDIR /app
COPY HybridGuard/app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY HybridGuard/app/ .
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
