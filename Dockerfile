# Stage 1: Base Python environment
FROM python:3.10-alpine3.16 AS base
RUN apk add --no-cache bash

# Stage 2: Get Gitleaks binary
FROM zricethezav/gitleaks:latest AS gitleaks

# Stage 3: Final image
FROM base

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Gitleaks binary
COPY --from=gitleaks /usr/bin/gitleaks /usr/bin/gitleaks

# Copy application code
COPY transform_gitleaks.py /app/transform_gitleaks.py

WORKDIR /code
ENTRYPOINT ["python", "/app/transform_gitleaks.py"]