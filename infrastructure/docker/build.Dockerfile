# Build stage - Compile Python bytecode and install dependencies
FROM python:3.13-slim-bookworm AS builder

# Set build arguments
ARG BUILDKIT_INLINE_CACHE=1
ARG PIP_NO_CACHE_DIR=0
ARG PIP_DISABLE_PIP_VERSION_CHECK=1

# Set environment variables for build optimization
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONOPTIMIZE=2 \
  PIP_NO_INPUT=1 \
  PIP_TIMEOUT=100 \
  PIP_RETRIES=5

# Install system build dependencies (minimal set)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Create app user and directories
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt ./

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv \
  && /opt/venv/bin/pip install --upgrade pip setuptools wheel \
  && /opt/venv/bin/pip install -r requirements.txt \
  && find /opt/venv -name "*.pyc" -delete \
  && find /opt/venv -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Copy source code
COPY src/ ./src/
COPY pyproject.toml ./

# Compile Python bytecode for faster startup
RUN /opt/venv/bin/python -m compileall -b src/ \
  && find src/ -name "*.py" -delete \
  && find src/ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Create precompiled package structure
RUN mkdir -p /app/precompiled \
  && cp -r src/* /app/precompiled/ \
  && chown -R app:app /app /opt/venv
