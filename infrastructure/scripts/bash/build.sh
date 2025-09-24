#!/bin/bash
# Optimized build script using Docker Bake for maximum cache efficiency

set -e

echo "🏗️ Building Goldilocks with maximum cache optimization..."

# Enable BuildKit features
export DOCKER_BUILDKIT=1
export BUILDKIT_PROGRESS=plain
export BUILDX_NO_DEFAULT_ATTESTATIONS=1

# Change to project root
cd "$(dirname "$0")/../../.." || exit 1

# Setup cache directories for instant subsequent builds
echo "📁 Setting up SSD cache directories..."
CACHE_DIRS=(
    "/tmp/goldilocks-cache/buildx"
    "/tmp/goldilocks-cache/pip"
    "/tmp/goldilocks-cache/npm"
    "/tmp/goldilocks-cache/pre-commit"
    "/tmp/goldilocks-cache/mypy"
    "/tmp/goldilocks-cache/pytest"
    "/tmp/goldilocks-cache/ruff"
)

for dir in "${CACHE_DIRS[@]}"; do
    sudo mkdir -p "$dir" && sudo chown -R "${USER}:${USER}" "$dir"
done

# Create buildx builder
docker buildx create --name goldilocks-builder --driver docker-container --use --bootstrap 2>/dev/null || \
docker buildx use goldilocks-builder

# Build target selection
TARGET=${1:-all}

build_image() {
    local target="$1"
    local tag="$2"
    local description="$3"

    echo "🚀 $description..."

    docker buildx build \
        --target "$target" \
        --tag "goldilocks:$tag" \
        --file infrastructure/docker/dockerfiles/Dockerfile.multi-stage \
        --cache-from "type=local,src=/tmp/goldilocks-cache/buildx" \
        --cache-to "type=local,dest=/tmp/goldilocks-cache/buildx,mode=max" \
        --load \
        .
}

case "$TARGET" in
    "builder"|"build")
        build_image "builder" "builder" "Building base builder stage"
        ;;
    "tools"|"dev"|"development")
        build_image "devcontainer" "devcontainer" "Building development environment"
        ;;
    "runtime"|"prod"|"production")
        build_image "runtime" "runtime" "Building production runtime"
        build_image "production" "production" "Building production image"
        ;;
    "devcontainer")
        build_image "devcontainer" "devcontainer" "Building devcontainer"
        ;;
    "all"|*)
        build_image "builder" "builder" "Building base builder"
        build_image "devcontainer" "devcontainer" "Building development tools"
        build_image "runtime" "runtime" "Building production runtime"
        ;;
esac

echo ""
echo "📊 Build complete! Images created:"
docker images | grep goldilocks
echo ""
echo "💡 Subsequent builds will be near-instant thanks to aggressive caching!"
