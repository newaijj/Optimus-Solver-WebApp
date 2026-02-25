FROM python:3.11-slim

WORKDIR /app

# Install small system deps (if any Python wheels need building)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps (use root requirements.txt)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY api /app/api

ENV PORT=5000
EXPOSE 5000

# Run with gunicorn (api.app:app should expose `app`)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api.app:app", "--workers", "2", "--worker-class", "gthread"]