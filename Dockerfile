FROM python:3.11-slim

WORKDIR /app

COPY HybridGuard/app/requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt


ENV CACHE_BUSTER=9

COPY HybridGuard/app/ .
COPY HybridGuard/models/ /models/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
# FROM python:3.11-slim

# WORKDIR /app

# COPY HybridGuard/app/requirements.txt .

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache-dir -r requirements.txt
# # ENV CACHE_BUSTER=1
# # COPY HybridGuard/app/ .
# ENV CACHE_BUSTER=7
# COPY HybridGuard/app/ .
# COPY HybridGuard/models/ /models/

# COPY HybridGuard/app/ .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
