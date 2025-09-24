#!/bin/bash

# Optimized build script for Goldilocks using Docker Bake
# Leverages BuildKit cache mounts, inline cache, and persistent SSD storage

set -e

echo "🏗️  Building Goldilocks with Docker Bake (optimized for SSD performance)..."

# Enable Docker BuildKit with advanced features
export DOCKER_BUILDKIT=1
export BUILDKIT_PROGRESS=plain
export BUILDX_NO_DEFAULT_ATTESTATIONS=1

# Change to project root
cd "$(dirname "$0")/../.." || exit 1

# Create cache directories on SSD for maximum performance
echo "� Setting up SSD cache directories..."
sudo mkdir -p /tmp/{.buildx-cache-{builder,tools,runtime,production,devcontainer},goldilocks-{venv,node-modules,bytecode,build-cache},pip-cache,npm-cache,pre-commit-cache,mypy-cache,pytest-cache,ruff-cache,buildx-cache}
sudo chown -R ${USER}:${USER} /tmp/{.buildx-cache-*,goldilocks-*,pip-cache,npm-cache,pre-commit-cache,mypy-cache,pytest-cache,ruff-cache,buildx-cache}

# Initialize buildx builder with advanced features
echo "🔧 Setting up buildx builder..."
docker buildx create --name goldilocks-builder --driver docker-container --use --bootstrap 2>/dev/null || docker buildx use goldilocks-builder

# Default target selection
TARGET=${1:-default}

case "$TARGET" in
  "dev"|"development")
    echo "� Building development environment..."
    docker buildx bake -f docker-bake.json development --load
    ;;
  "prod"|"production")
    echo "🚀 Building production environment..."
    docker buildx bake -f docker-bake.json production --load
    ;;
  "builder")
    echo "📦 Building base builder stage..."
    docker buildx bake -f docker-bake.json builder --load
    ;;
  "tools")
    echo "🔧 Building tools stage..."
    docker buildx bake -f docker-bake.json tools --load
    ;;
  "runtime")
    echo "🚀 Building runtime stage..."
    docker buildx bake -f docker-bake.json runtime --load
    ;;
  "devcontainer")
    echo "🏠 Building devcontainer..."
    docker buildx bake -f docker-bake.json devcontainer --load
    ;;
  "all"|"default"|*)
    echo "🌟 Building all targets with maximum cache optimization..."
    docker buildx bake -f docker-bake.json --load
    ;;
esac

# Show cache usage statistics
echo ""
echo "📊 Build cache statistics:"
du -sh /tmp/.buildx-cache-* 2>/dev/null || echo "No cache directories found"
du -sh /tmp/goldilocks-* 2>/dev/null || echo "No volume directories found"

echo ""
echo "📊 Docker images built:"
docker images | grep goldilocks

echo ""
echo "✅ Optimized multi-stage build complete!"
echo ""
echo "🚀 Usage:"
echo "  Development: docker-compose --profile dev up"
echo "  Production:  docker-compose --profile prod up"
echo "  Build only:  docker-compose --profile build up"
echo ""
echo "💡 Subsequent builds will be near-instant thanks to SSD cache optimization!"
