# Production runtime stage - Minimal image with only runtime dependencies
FROM python:3.13-slim-bookworm AS runtime

# Set build arguments
ARG TARGETPLATFORM
ARG BUILDPLATFORM

# Set runtime environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONOPTIMIZE=2 \
  PATH="/opt/venv/bin:$PATH" \
  FLASK_APP=goldilocks.app \
  FLASK_ENV=production

# Install only runtime system dependencies with cache mount
RUN --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  apt-get update && apt-get install -y --no-install-recommends \
  sqlite3 \
  curl \
  && apt-get clean

# Create app user
RUN useradd --create-home --no-log-init --shell /bin/bash app

# Copy virtual environment from builder
COPY --from=builder --chown=app:app /opt/venv /opt/venv

# Copy precompiled application
COPY --from=builder --chown=app:app /app/precompiled /app

# Copy frontend static assets
COPY --chown=app:app frontend/static/ /app/static/

# Create production entrypoint
COPY infrastructure/docker/entrypoint-prod.sh /entrypoint-prod.sh
RUN chmod +x /entrypoint-prod.sh

# Switch to app user
USER app
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9000/health')" || exit 1

# Expose port
EXPOSE 9000

# Production entrypoint
ENTRYPOINT ["/entrypoint-prod.sh"]
