# Lightweight production Dockerfile - uses multi-stage build
# For development, use: docker-compose --profile dev up
# For production: docker-compose --profile prod up

# Import the runtime stage from the multi-stage architecture
FROM goldilocks:runtime

# This Dockerfile is kept for compatibility with simple docker build commands
# It references the optimized multi-stage runtime image

# To build the multi-stage images:
# docker build -f infrastructure/docker/build.Dockerfile --target builder -t goldilocks:builder .
# docker build -f infrastructure/docker/tools.Dockerfile --target tools -t goldilocks:tools .
# docker build -f infrastructure/docker/runtime.Dockerfile --target runtime -t goldilocks:runtime .
