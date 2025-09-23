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
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy development configuration files
COPY .pre-commit-config.yaml pyproject.toml ./
COPY package.json package-lock.json* ./

# Install Node.js dependencies if package.json exists
RUN if [ -f "package.json" ]; then npm ci --only=production; fi

# Tests are already copied as part of src/ in the base stage
# No separate test copy needed since tests are in src/goldilocks/tests/

# Set up pre-commit hooks
RUN /opt/venv/bin/pre-commit install-hooks || true

# Create development entrypoint
COPY infrastructure/docker/entrypoint-dev.sh /entrypoint-dev.sh
RUN chmod +x /entrypoint-dev.sh

USER app
EXPOSE 9000
ENTRYPOINT ["/entrypoint-dev.sh"]
