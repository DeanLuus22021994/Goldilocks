# Simple Dockerfile for Goldilocks Flask App
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  FLASK_APP=src/goldilocks/app.py \
  FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY pyproject.toml ./

# Change ownership to app user
RUN chown -R app:app /app

USER app
EXPOSE 9000

# Run the Flask application
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "9000"]
