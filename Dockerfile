# Modern Python 3.13.7 Dockerfile for Production - Secure & Optimized
FROM python:3.13.7-slim-bookworm AS base

# Set build arguments for cache optimization
ARG BUILDKIT_INLINE_CACHE=1
ARG PIP_NO_CACHE_DIR=0
ARG TARGETPLATFORM

# Set environment variables for security and performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/app/.local/bin:$PATH"

# Install system dependencies with cache mount - minimal security packages
RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  apt-get update && apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Create non-root app user for security
RUN useradd --create-home --shell /bin/bash --uid 1000 app

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies with cache mount
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
  pip install --no-cache-dir --upgrade pip setuptools wheel && \
  pip install --no-cache-dir -r requirements.txt

# Copy application code (modern Python 3.13.7 ready)
COPY app.py ./
COPY src/ ./src/
COPY frontend/static/ ./frontend/static/
COPY pyproject.toml ./

# Change ownership to app user for security
RUN chown -R app:app /app

# Modern health check with timeout optimization
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:9000/health || exit 1

# Switch to non-root user for security
USER app
EXPOSE 9000

# Run the modernized Flask application
CMD ["python", "app.py"]
