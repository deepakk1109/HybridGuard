FROM python:3.11-slim

WORKDIR /app

# Install system deps needed by onnxruntime / numpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY models/ ./models/

# Run as non-root user (OpenShift requirement)
RUN useradd -m hybridguard && chown -R hybridguard /app
USER hybridguard

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
