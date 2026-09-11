FROM python:3.11-slim

WORKDIR /srv

# curl is needed for the HEALTHCHECK below
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first (better layer caching)
COPY app/requirements.txt ./app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt

# Copy model and app code
COPY model/model.pkl ./model/model.pkl
COPY app/app.py ./app/app.py

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--chdir", "app", "app:app"]
