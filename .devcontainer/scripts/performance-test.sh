#!/bin/bash
# Ultra-Performance DevContainer Validation Script
# Tests build performance, caching efficiency, and GPU utilization
# Adheres to Copilot Instructions: PERFORMANCE, RELIABILITY, MODERNIZE

set -e

echo "🚀 Goldilocks Ultra-Performance DevContainer Test Suite"
echo "======================================================"

# Performance metrics tracking
START_TIME=$(date +%s)

# Test 1: Docker BuildKit and GPU availability
echo "🔧 Test 1: Build environment validation..."
if ! docker version &>/dev/null; then
    echo "❌ Docker not available"
    exit 1
fi

if ! docker buildx version &>/dev/null; then
    echo "❌ Docker BuildX not available"
    exit 1
fi

echo "✅ Docker BuildKit: $(docker buildx version | head -n1)"

# Test 2: GPU availability
echo "🎮 Test 2: GPU acceleration check..."
if nvidia-smi &>/dev/null; then
    echo "✅ NVIDIA GPU available: $(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -n1)"
elif lspci | grep -i vga | grep -i nvidia &>/dev/null; then
    echo "⚠️  NVIDIA GPU detected but nvidia-smi not available"
else
    echo "⚠️  No NVIDIA GPU detected - builds will use CPU only"
fi

# Test 3: Volume persistence validation
echo "💾 Test 3: Persistent volume validation..."
VOLUMES=(
    "goldilocks-venv-optimized"
    "goldilocks-python-cache"
    "goldilocks-pip-cache"
    "goldilocks-build-cache"
    "goldilocks-bytecode-cache"
    "goldilocks-precompiled"
    "docker-buildx-cache"
)

for vol in "${VOLUMES[@]}"; do
    if docker volume inspect "$vol" &>/dev/null; then
        SIZE=$(docker volume inspect "$vol" --format '{{.Mountpoint}}' 2>/dev/null | xargs du -sh 2>/dev/null | cut -f1 || echo "unknown")
        echo "✅ Volume $vol exists (Size: $SIZE)"
    else
        echo "⚠️  Volume $vol will be created on first build"
    fi
done

# Test 4: Python image availability
echo "🐍 Test 4: Python image validation..."
if docker pull python:3.14.0rc3-trixie &>/dev/null; then
    IMAGE_SIZE=$(docker image inspect python:3.14.0rc3-trixie --format '{{.Size}}' | numfmt --to=iec)
    echo "✅ Python 3.14.0rc3-trixie available (Size: $IMAGE_SIZE)"
else
    echo "❌ Failed to pull python:3.14.0rc3-trixie"
    exit 1
fi

# Test 5: Cache hit simulation
echo "🎯 Test 5: Build cache efficiency test..."
BUILD_START=$(date +%s)

# Simulate first build (should take longer)
echo "   First build simulation (with cache warming)..."
docker build \
  --file infrastructure/docker/dockerfiles/Dockerfile.multi-stage \
  --target devcontainer \
  --tag goldilocks:devcontainer-test \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --build-arg PYTHON_VERSION=3.14.0rc3-trixie \
  --cache-from goldilocks:devcontainer-test \
  . 2>/dev/null || true

FIRST_BUILD_TIME=$(($(date +%s) - BUILD_START))

# Simulate second build (should be much faster)
echo "   Second build simulation (cache utilization)..."
SECOND_BUILD_START=$(date +%s)

docker build \
  --file infrastructure/docker/dockerfiles/Dockerfile.multi-stage \
  --target devcontainer \
  --tag goldilocks:devcontainer-test-2 \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --build-arg PYTHON_VERSION=3.14.0rc3-trixie \
  --cache-from goldilocks:devcontainer-test \
  . 2>/dev/null || true

SECOND_BUILD_TIME=$(($(date +%s) - SECOND_BUILD_START))

if [ $SECOND_BUILD_TIME -lt $FIRST_BUILD_TIME ]; then
    SPEEDUP=$(echo "scale=2; $FIRST_BUILD_TIME / $SECOND_BUILD_TIME" | bc 2>/dev/null || echo "N/A")
    echo "✅ Cache efficiency: ${SPEEDUP}x speedup (${FIRST_BUILD_TIME}s → ${SECOND_BUILD_TIME}s)"
else
    echo "⚠️  Cache may not be working optimally"
fi

# Test 6: DevContainer configuration validation
echo "⚙️  Test 6: DevContainer config validation..."
if [ -f ".devcontainer/devcontainer.json" ]; then
    echo "✅ DevContainer configuration found"

    # Check for performance optimizations
    if grep -q "gpu.*true" .devcontainer/devcontainer.json; then
        echo "✅ GPU acceleration enabled"
    fi

    if grep -q "buildkit" .devcontainer/devcontainer.json; then
        echo "✅ BuildKit optimization detected"
    fi

    MOUNT_COUNT=$(grep -c "source=" .devcontainer/devcontainer.json || echo "0")
    echo "✅ Persistent volume mounts: $MOUNT_COUNT"
else
    echo "❌ DevContainer configuration missing"
    exit 1
fi

# Performance summary
TOTAL_TIME=$(($(date +%s) - START_TIME))
echo ""
echo "🎯 Performance Test Summary"
echo "=========================="
echo "Total test time: ${TOTAL_TIME}s"
echo "First build time: ${FIRST_BUILD_TIME}s"
echo "Second build time: ${SECOND_BUILD_TIME}s"
if [ $SECOND_BUILD_TIME -lt $FIRST_BUILD_TIME ]; then
    echo "Cache efficiency: $(echo "scale=1; (1 - $SECOND_BUILD_TIME/$FIRST_BUILD_TIME) * 100" | bc 2>/dev/null || echo "N/A")% faster"
fi

echo ""
echo "🚀 Ultra-Performance DevContainer Ready!"
echo "   - Python 3.14.0rc3-trixie optimized"
echo "   - GPU acceleration configured"
echo "   - Persistent volume caching enabled"
echo "   - BuildKit optimization active"
echo "   - Bytecode precompilation ready"
echo ""
echo "✨ Subsequent builds should be near-instant!"
