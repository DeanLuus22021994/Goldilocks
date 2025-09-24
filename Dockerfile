# Simple optimized Dockerfile for Goldilocks Flask App
FROM python:3.12-slim-bookworm AS base

# Set build arguments for cache optimization
ARG BUILDKIT_INLINE_CACHE=1
ARG PIP_NO_CACHE_DIR=0
ARG TARGETPLATFORM

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONOPTIMIZE=2 \
  FLASK_APP=src/goldilocks/app.py \
  FLASK_ENV=production

# Install system dependencies with cache mount
RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  apt-get update && apt-get install -y --no-install-recommends \
  curl \
  && apt-get clean

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies with cache mount
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
  pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY frontend/static/ ./static/
COPY pyproject.toml ./

# Change ownership to app user
RUN chown -R app:app /app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:9000/health || exit 1

USER app
EXPOSE 9000

# Run the Flask application with gunicorn for production
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:9000", "--workers", "2", "--timeout", "30", "--access-logfile", "-", "--error-logfile", "-", "goldilocks.app:app"]
