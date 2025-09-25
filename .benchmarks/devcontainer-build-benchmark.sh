#!/bin/bash
# DevContainer Build Benchmarking Script - JSON Output Only
# Tracks Python version, resource usage, and performance metrics

set -e

BENCHMARK_DIR="/projects/Goldilocks/.benchmarks"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BENCHMARK_FILE="$BENCHMARK_DIR/build_${TIMESTAMP}.json"

# All progress messages go to stderr, only final JSON goes to stdout
echo "🔍 DevContainer Build Benchmark Starting..." >&2
echo "Timestamp: $(date)" >&2
echo "Benchmark file: $BENCHMARK_FILE" >&2

# Create benchmarks directory if it doesn't exist
mkdir -p "$BENCHMARK_DIR"

# Start timing
BUILD_START=$(date +%s.%3N)

# System info before build
echo "📊 Collecting pre-build system metrics..." >&2

# Get initial system metrics
INITIAL_MEMORY=$(free -m | awk '/^Mem:/ {print $3}')
INITIAL_DISK=$(df -BM /var/lib/docker | awk 'NR==2 {print $3}' | sed 's/M//')
INITIAL_GPU_MEMORY=0

# Check GPU memory if available
if command -v nvidia-smi &> /dev/null; then
    INITIAL_GPU_MEMORY=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -n1)
fi

# Start JSON benchmark file
cat > "$BENCHMARK_FILE" << EOF
{
  "benchmark_info": {
    "timestamp": "$(date -Iseconds)",
    "script_version": "1.0.0",
    "benchmark_id": "${TIMESTAMP}"
  },
  "system_info": {
    "os": "$(uname -s)",
    "kernel": "$(uname -r)",
    "architecture": "$(uname -m)",
    "cpu_cores": $(nproc),
    "total_memory_mb": $(free -m | awk '/^Mem:/ {print $2}'),
    "docker_version": "$(docker --version | cut -d' ' -f3 | tr -d ',')",
    "buildx_version": "$(docker buildx version | head -n1 | cut -d' ' -f2)"
  },
  "gpu_info": {
EOF

# Add GPU info if available
if command -v nvidia-smi &> /dev/null; then
    cat >> "$BENCHMARK_FILE" << EOF
    "available": true,
    "driver_version": "$(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits | head -n1)",
    "gpu_name": "$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -n1)",
    "total_memory_mb": $(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -n1)
EOF
else
    cat >> "$BENCHMARK_FILE" << EOF
    "available": false,
    "driver_version": "N/A",
    "gpu_name": "N/A",
    "total_memory_mb": 0
EOF
fi

cat >> "$BENCHMARK_FILE" << EOF
  },
  "pre_build_metrics": {
    "memory_used_mb": $INITIAL_MEMORY,
    "disk_used_mb": $INITIAL_DISK,
    "gpu_memory_used_mb": $INITIAL_GPU_MEMORY
  },
  "build_process": {
EOF

echo "🚀 Starting DevContainer CLI build test..." >&2

# Test 1: Initialize volumes
echo "📦 Step 1: Initializing volumes..." >&2
VOLUME_START=$(date +%s.%3N)

# Run initialize command
bash -c "docker volume create goldilocks-venv-optimized; docker volume create goldilocks-python-cache; docker volume create goldilocks-pip-cache; docker volume create goldilocks-build-cache; docker volume create goldilocks-bytecode-cache; docker volume create goldilocks-precompiled; docker volume create goldilocks-dev-cache; docker volume create goldilocks-pre-commit; docker volume create goldilocks-mypy; docker volume create goldilocks-ruff; docker volume create goldilocks-pytest; docker volume create docker-buildx-cache" >&2

VOLUME_END=$(date +%s.%3N)
VOLUME_TIME=$(echo "$VOLUME_END - $VOLUME_START" | bc)

echo "    Volume initialization time: ${VOLUME_TIME}s" >&2

# Test 2: Build the devcontainer
echo "🏗️  Step 2: Building devcontainer..." >&2
BUILD_DOCKER_START=$(date +%s.%3N)

# Build using devcontainer CLI
if false; then  # Temporarily disabled due to Python 3.14 compatibility issues
    echo "Using devcontainer CLI..." >&2
    devcontainer build --workspace-folder /projects/Goldilocks --log-level trace
    BUILD_SUCCESS=true
else
    echo "Using docker build directly (recommended for Python 3.14.0rc3)..." >&2
    docker build \
        --file infrastructure/docker/dockerfiles/Dockerfile.multi-stage \
        --target devcontainer \
        --tag goldilocks:devcontainer-benchmark \
        --build-arg PYTHON_VERSION=3.14.0rc3-trixie \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --build-arg BUILDX_EXPERIMENTAL=1 \
        --platform linux/amd64 \
        --progress plain \
        . >&2 && BUILD_SUCCESS=true || BUILD_SUCCESS=false
fi

BUILD_DOCKER_END=$(date +%s.%3N)
BUILD_DOCKER_TIME=$(echo "$BUILD_DOCKER_END - $BUILD_DOCKER_START" | bc)

echo "    Docker build time: ${BUILD_DOCKER_TIME}s" >&2

# Test 3: Get container info and Python version
echo "🐍 Step 3: Testing container and Python version..." >&2
CONTAINER_TEST_START=$(date +%s.%3N)

# Start a test container
CONTAINER_ID=$(docker run -d \
    --name goldilocks-benchmark-test \
    --gpus=all \
    --shm-size=4g \
    -v goldilocks-venv-optimized:/opt/venv \
    goldilocks:devcontainer-benchmark \
    tail -f /dev/null)

# Wait for container to be ready
sleep 3

# Get Python version
PYTHON_VERSION=$(docker exec $CONTAINER_ID /bin/bash -c "python --version" 2>&1 || echo "Python version unavailable")
PYTHON_EXECUTABLE=$(docker exec $CONTAINER_ID /bin/bash -c "which python" 2>&1 || echo "/usr/local/bin/python")
VENV_PYTHON_VERSION=$(docker exec $CONTAINER_ID /bin/bash -c "/opt/venv/bin/python --version" 2>&1 || echo "Venv Python unavailable")

# Check if Flask is available
FLASK_VERSION=$(docker exec $CONTAINER_ID /bin/bash -c "/opt/venv/bin/pip show flask | grep Version | cut -d' ' -f2" 2>&1 || echo "Flask not installed")

# Get container resource usage
CONTAINER_MEMORY=$(docker stats $CONTAINER_ID --no-stream --format "table {{.MemUsage}}" | tail -n1 | cut -d'/' -f1 | sed 's/ //g')
CONTAINER_CPU=$(docker stats $CONTAINER_ID --no-stream --format "table {{.CPUPerc}}" | tail -n1)

# Clean up test container
docker stop $CONTAINER_ID &>/dev/null
docker rm $CONTAINER_ID &>/dev/null

CONTAINER_TEST_END=$(date +%s.%3N)
CONTAINER_TEST_TIME=$(echo "$CONTAINER_TEST_END - $CONTAINER_TEST_START" | bc)

echo "    Container test time: ${CONTAINER_TEST_TIME}s" >&2
echo "    Python version: $PYTHON_VERSION" >&2
echo "    Venv Python version: $VENV_PYTHON_VERSION" >&2
echo "    Flask version: $FLASK_VERSION" >&2

# Get post-build system metrics
echo "📈 Collecting post-build system metrics..." >&2
FINAL_MEMORY=$(free -m | awk '/^Mem:/ {print $3}')
FINAL_DISK=$(df -BM /var/lib/docker | awk 'NR==2 {print $3}' | sed 's/M//')
FINAL_GPU_MEMORY=0

if command -v nvidia-smi &> /dev/null; then
    FINAL_GPU_MEMORY=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -n1)
fi

# Calculate resource deltas
MEMORY_DELTA=$((FINAL_MEMORY - INITIAL_MEMORY))
DISK_DELTA=$((FINAL_DISK - INITIAL_DISK))
GPU_MEMORY_DELTA=$((FINAL_GPU_MEMORY - INITIAL_GPU_MEMORY))

BUILD_END=$(date +%s.%3N)
TOTAL_TIME=$(echo "$BUILD_END - $BUILD_START" | bc)

# Format decimal numbers with leading zeros
VOLUME_TIME_FORMATTED=$(printf "%.3f" "$VOLUME_TIME")
BUILD_DOCKER_TIME_FORMATTED=$(printf "%.3f" "$BUILD_DOCKER_TIME")
CONTAINER_TEST_TIME_FORMATTED=$(printf "%.3f" "$CONTAINER_TEST_TIME")
TOTAL_TIME_FORMATTED=$(printf "%.3f" "$TOTAL_TIME")

# Complete the JSON file
cat >> "$BENCHMARK_FILE" << EOF
    "volume_initialization_time_seconds": $VOLUME_TIME_FORMATTED,
    "docker_build_time_seconds": $BUILD_DOCKER_TIME_FORMATTED,
    "container_test_time_seconds": $CONTAINER_TEST_TIME_FORMATTED,
    "total_build_time_seconds": $TOTAL_TIME_FORMATTED,
    "build_successful": $BUILD_SUCCESS
  },
  "python_info": {
    "system_python_version": "$PYTHON_VERSION",
    "python_executable": "$PYTHON_EXECUTABLE",
    "venv_python_version": "$VENV_PYTHON_VERSION",
    "flask_version": "$FLASK_VERSION"
  },
  "resource_usage": {
    "memory_delta_mb": $MEMORY_DELTA,
    "disk_delta_mb": $DISK_DELTA,
    "gpu_memory_delta_mb": $GPU_MEMORY_DELTA,
    "peak_container_memory": "$CONTAINER_MEMORY",
    "peak_container_cpu": "$CONTAINER_CPU"
  },
  "post_build_metrics": {
    "memory_used_mb": $FINAL_MEMORY,
    "disk_used_mb": $FINAL_DISK,
    "gpu_memory_used_mb": $FINAL_GPU_MEMORY
  },
  "performance_summary": {
    "build_efficiency": "$(printf "%.1f" $(echo "scale=3; $BUILD_DOCKER_TIME / 60" | bc)) minutes",
    "memory_efficiency": "${MEMORY_DELTA}MB increase",
    "disk_efficiency": "${DISK_DELTA}MB increase",
    "overall_rating": "$(if [ "$BUILD_SUCCESS" = "true" ] && (( $(echo "$TOTAL_TIME < 120" | bc -l) )); then echo "Excellent"; elif [ "$BUILD_SUCCESS" = "true" ] && (( $(echo "$TOTAL_TIME < 300" | bc -l) )); then echo "Good"; elif [ "$BUILD_SUCCESS" = "true" ]; then echo "Fair"; else echo "Failed"; fi)"
  }
}
EOF

# Clean up old benchmark files, keep only the 3 most recent
find "$BENCHMARK_DIR" -name "build_*.json" -type f | sort -r | tail -n +4 | xargs -r rm

# Output only the JSON content to stdout
cat "$BENCHMARK_FILE"

# Clean exit based on build success
if [ "$BUILD_SUCCESS" = "true" ]; then
    exit 0
else
    exit 1
fi
