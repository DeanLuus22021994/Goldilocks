#!/bin/bash

# Build script for Goldilocks multi-stage Docker architecture
# This script builds all Docker stages with proper caching and optimization

set -e

echo "🏗️  Building Goldilocks multi-stage Docker architecture..."

# Enable Docker BuildKit for better caching
export DOCKER_BUILDKIT=1

# Build arguments for caching
BUILD_ARGS="--build-arg BUILDKIT_INLINE_CACHE=1"

# Change to project root
cd "$(dirname "$0")/../.." || exit 1

echo "📦 Building stage 1: Builder (dependencies + bytecode compilation)..."
docker build \
    ${BUILD_ARGS} \
    --target builder \
    --cache-from goldilocks:builder \
    --tag goldilocks:builder \
    --file infrastructure/docker/build.Dockerfile \
    .

echo "🔧 Building stage 2: Tools (development environment)..."
docker build \
    ${BUILD_ARGS} \
    --target tools \
    --cache-from goldilocks:builder,goldilocks:tools \
    --tag goldilocks:tools \
    --file infrastructure/docker/tools.Dockerfile \
    .

echo "🚀 Building stage 3: Runtime (production environment)..."
docker build \
    ${BUILD_ARGS} \
    --target runtime \
    --cache-from goldilocks:builder,goldilocks:runtime \
    --tag goldilocks:runtime \
    --file infrastructure/docker/runtime.Dockerfile \
    .

echo "📊 Docker images built:"
docker images | grep goldilocks

echo "✅ Multi-stage build complete!"
echo ""
echo "Usage:"
echo "  Development: docker-compose --profile dev up"
echo "  Production:  docker-compose --profile prod up"
echo "  Build only:  docker-compose --profile build up"
