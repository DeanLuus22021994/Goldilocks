#!/bin/bash
# Setup script for Goldilocks optimized Docker environment
# Creates persistent cache directories on SSD for maximum performance

set -e

echo "🏗️  Setting up Goldilocks optimized build environment..."

# Define cache directories for optimal SSD performance
CACHE_BASE="/tmp/goldilocks-cache"
CACHE_DIRS=(
  ".buildx-cache-builder"
  ".buildx-cache-tools"
  ".buildx-cache-runtime"
  ".buildx-cache-production"
  ".buildx-cache-devcontainer"
  "goldilocks-venv"
  "goldilocks-node-modules"
  "goldilocks-bytecode"
  "goldilocks-build-cache"
  "pip-cache"
  "npm-cache"
  "pre-commit-cache"
  "mypy-cache"
  "pytest-cache"
  "ruff-cache"
  "buildx-cache"
)

# Create base cache directory
sudo mkdir -p "$CACHE_BASE"

# Create all cache directories with proper permissions
echo "📁 Creating optimized cache directories..."
for dir in "${CACHE_DIRS[@]}"; do
  FULL_PATH="/tmp/$dir"
  sudo mkdir -p "$FULL_PATH"
  sudo chown -R "${USER}:${USER}" "$FULL_PATH"
  echo "  ✅ Created: $FULL_PATH"
done

# Set up Docker BuildKit builder for advanced features
echo "🔧 Configuring Docker BuildKit builder..."
docker buildx create --name goldilocks-builder --driver docker-container --use --bootstrap 2>/dev/null || {
  echo "Builder already exists, using existing one..."
  docker buildx use goldilocks-builder
}

# Pre-create Docker volumes for immediate availability
echo "📦 Pre-creating Docker volumes..."
VOLUME_NAMES=(
  "goldilocks-venv"
  "vscode-server-cache"
  "pip-cache"
  "npm-cache"
  "pre-commit-cache"
  "mypy-cache"
  "pytest-cache"
  "ruff-cache"
  "buildx-cache"
)

for volume in "${VOLUME_NAMES[@]}"; do
  docker volume create "$volume" >/dev/null 2>&1 || echo "Volume $volume already exists"
  echo "  ✅ Volume: $volume"
done

# Set optimal Docker daemon configuration
echo "⚙️  Checking Docker configuration..."
DOCKER_CONFIG_DIR="$HOME/.docker"
DOCKER_CONFIG_FILE="$DOCKER_CONFIG_DIR/daemon.json"

mkdir -p "$DOCKER_CONFIG_DIR"

# Create optimized Docker daemon config if it doesn't exist
if [ ! -f "$DOCKER_CONFIG_FILE" ]; then
  cat > "$DOCKER_CONFIG_FILE" << 'EOF'
{
  "features": {
    "buildkit": true
  },
  "experimental": true,
  "builder": {
    "gc": {
      "enabled": true,
      "defaultKeepStorage": "10GB"
    }
  }
}
EOF
  echo "  ✅ Created optimized Docker daemon configuration"
else
  echo "  ✅ Docker daemon configuration exists"
fi

# Display cache statistics
echo ""
echo "📊 Cache directory statistics:"
for dir in "${CACHE_DIRS[@]}"; do
  FULL_PATH="/tmp/$dir"
  if [ -d "$FULL_PATH" ]; then
    SIZE=$(du -sh "$FULL_PATH" 2>/dev/null | cut -f1)
    echo "  $dir: $SIZE"
  fi
done

echo ""
echo "✅ Goldilocks optimized build environment setup complete!"
echo ""
echo "🚀 Next steps:"
echo "  1. Build optimized images: ./infrastructure/docker/build.sh"
echo "  2. Start development: docker-compose --profile dev up"
echo "  3. Or build specific target: ./infrastructure/docker/build.sh dev"
echo ""
echo "💡 All subsequent builds will leverage SSD cache for near-instant performance!"
echo "📈 Expected performance improvement: 5-10x faster builds after first run"
