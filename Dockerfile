FROM python:3.11-slim

WORKDIR /app

COPY HybridGuard/app/requirements.txt .

# டைம்-அவுட்டை 100 செகண்டா மாத்தி, 5 முறை ரீட்ரை பண்ண லாஜிக் சேர்த்திருக்கோம்!
RUN pip install --no-cache-dir --default-timeout=100 --retries 5 -r requirements.txt

ENV CACHE_BUSTER=15
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


# ENV CACHE_BUSTER=15

# COPY HybridGuard/app/ .
# COPY HybridGuard/models/ /models/

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
