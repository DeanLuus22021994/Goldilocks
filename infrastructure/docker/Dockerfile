# Lightweight production Dockerfile - uses optimized multi-stage build
# For development, use: docker-compose --profile dev up
# For production: docker-compose --profile prod up

# Import the runtime stage from the multi-stage architecture
FROM goldilocks:runtime AS production

# Add production-specific optimizations
LABEL maintainer="Goldilocks Team"
LABEL version="1.0.0"
LABEL description="Goldilocks Flask Application - Production Ready"

# Copy any additional production assets
COPY --chown=app:app frontend/static/ /app/static/

# Final production configuration
ENV FLASK_ENV=production \
  FLASK_DEBUG=0 \
  WORKERS=2 \
  WORKER_CLASS=sync \
  TIMEOUT=30

# This Dockerfile leverages the optimized multi-stage runtime image
# Built with maximum SSD cache optimization and BuildKit features

# To build the complete multi-stage images with cache optimization:
# ./infrastructure/docker/build.sh production
#
# Or using Docker Bake for maximum performance:
# docker buildx bake -f docker-bake.json production --load
