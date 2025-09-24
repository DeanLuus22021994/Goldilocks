# Consolidated Dockerfile for devcontainer
# Combines builder and tools stages in one file to avoid dependency issues

# Build stage - Compile Python bytecode and install dependencies
# Modern Python 3.14.0rc3 DevContainer - Secure Base Image
FROM python:3.14.0rc3-trixie AS builder

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

# Development tools stage - Add testing, linting, and development utilities
FROM builder AS tools

# Install development dependencies
RUN /opt/venv/bin/pip install \
  pytest \
  pytest-cov \
  pytest-xdist \
  ruff \
  mypy \
  pre-commit \
  black \
  isort \
  flake8 \
  bandit \
  safety \
  httpx

# Install Node.js for frontend tooling (minimal installation)
RUN apt-get update && apt-get install -y --no-install-recommends \
  nodejs \
  npm \
  git \
  curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy development configuration files
COPY .pre-commit-config.yaml pyproject.toml ./
COPY package.json package-lock.json* ./

# Install Node.js dependencies if package.json exists
RUN if [ -f "package.json" ]; then npm ci --only=production; fi

# Set up pre-commit hooks
RUN /opt/venv/bin/pre-commit install-hooks || true

# Create development entrypoint
COPY infrastructure/docker/entrypoint-dev.sh /entrypoint-dev.sh
RUN chmod +x /entrypoint-dev.sh

# Set up PATH to include venv
ENV PATH="/opt/venv/bin:$PATH"

# Create startup script to fix permissions
RUN echo '#!/bin/bash\n\
  # Fix git permissions on startup\n\
  if [ -d "/workspaces/Goldilocks/.git" ]; then\n\
  sudo chown -R app:app /workspaces/Goldilocks/.git/\n\
  sudo chmod -R u+w /workspaces/Goldilocks/.git/\n\
  fi\n\
  exec "$@"' > /usr/local/bin/fix-permissions.sh

RUN chmod +x /usr/local/bin/fix-permissions.sh

# Install sudo for the permission fix script
RUN apt-get update && apt-get install -y --no-install-recommends sudo \
  && echo 'app ALL=(ALL) NOPASSWD: /bin/chown, /bin/chmod' >> /etc/sudoers \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER app
EXPOSE 9000
WORKDIR /workspaces/Goldilocks

# Use permission-fixing entrypoint
ENTRYPOINT ["/usr/local/bin/fix-permissions.sh"]
CMD ["/bin/bash"]
