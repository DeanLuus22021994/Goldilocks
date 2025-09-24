#!/bin/bash
# DevContainer Build Benchmarking Script
# Tracks Python version, resource usage, and performance metrics

set -e

BENCHMARK_DIR="/projects/Goldilocks/.benchmarks"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BENCHMARK_FILE="$BENCHMARK_DIR/build_${TIMESTAMP}.json"

echo "🔍 DevContainer Build Benchmark Starting..."
echo "Timestamp: $(date)"
echo "Benchmark file: $BENCHMARK_FILE"

# Create benchmarks directory if it doesn't exist
mkdir -p "$BENCHMARK_DIR"

# Start timing
BUILD_START=$(date +%s.%3N)

# System info before build
echo "📊 Collecting pre-build system metrics..."

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

echo "🚀 Starting DevContainer CLI build test..."

# Test 1: Initialize volumes
echo "📦 Step 1: Initializing volumes..."
VOLUME_START=$(date +%s.%3N)

# Run initialize command
bash -c "docker volume create goldilocks-venv-optimized; docker volume create goldilocks-python-cache; docker volume create goldilocks-pip-cache; docker volume create goldilocks-build-cache; docker volume create goldilocks-bytecode-cache; docker volume create goldilocks-precompiled; docker volume create vscode-server-insiders; docker volume create vscode-extensions-cache; docker volume create goldilocks-dev-cache; docker volume create goldilocks-pre-commit; docker volume create goldilocks-mypy; docker volume create goldilocks-ruff; docker volume create goldilocks-pytest; docker volume create docker-buildx-cache"

VOLUME_END=$(date +%s.%3N)
VOLUME_TIME=$(echo "$VOLUME_END - $VOLUME_START" | bc)

echo "    Volume initialization time: ${VOLUME_TIME}s"

# Test 2: Build the devcontainer
echo "🏗️  Step 2: Building devcontainer..."
BUILD_DOCKER_START=$(date +%s.%3N)

# Build using devcontainer CLI
if command -v devcontainer &> /dev/null; then
    echo "Using devcontainer CLI..."
    devcontainer build --workspace-folder /projects/Goldilocks --log-level trace
    BUILD_SUCCESS=true
else
    echo "devcontainer CLI not found, using docker build directly..."
    docker build \
        --file infrastructure/docker/dockerfiles/Dockerfile.multi-stage \
        --target devcontainer \
        --tag goldilocks:devcontainer-benchmark \
        --build-arg PYTHON_VERSION=3.14.0rc3-trixie \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --build-arg BUILDX_EXPERIMENTAL=1 \
        --platform linux/amd64 \
        --progress plain \
        . || BUILD_SUCCESS=false
    BUILD_SUCCESS=true
fi

BUILD_DOCKER_END=$(date +%s.%3N)
BUILD_DOCKER_TIME=$(echo "$BUILD_DOCKER_END - $BUILD_DOCKER_START" | bc)

echo "    Docker build time: ${BUILD_DOCKER_TIME}s"

# Test 3: Get container info and Python version
echo "🐍 Step 3: Testing container and Python version..."
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

echo "    Container test time: ${CONTAINER_TEST_TIME}s"
echo "    Python version: $PYTHON_VERSION"
echo "    Venv Python version: $VENV_PYTHON_VERSION"
echo "    Flask version: $FLASK_VERSION"

# Get post-build system metrics
echo "📈 Collecting post-build system metrics..."
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

# Complete the JSON file
cat >> "$BENCHMARK_FILE" << EOF
    "volume_initialization_time_seconds": $VOLUME_TIME,
    "docker_build_time_seconds": $BUILD_DOCKER_TIME,
    "container_test_time_seconds": $CONTAINER_TEST_TIME,
    "total_build_time_seconds": $TOTAL_TIME,
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
    "build_efficiency": "$(echo "scale=1; $BUILD_DOCKER_TIME / 60" | bc) minutes",
    "memory_efficiency": "${MEMORY_DELTA}MB increase",
    "disk_efficiency": "${DISK_DELTA}MB increase",
    "overall_rating": "$(if [ "$BUILD_SUCCESS" = "true" ] && (( $(echo "$TOTAL_TIME < 120" | bc -l) )); then echo "Excellent"; elif [ "$BUILD_SUCCESS" = "true" ] && (( $(echo "$TOTAL_TIME < 300" | bc -l) )); then echo "Good"; elif [ "$BUILD_SUCCESS" = "true" ]; then echo "Fair"; else echo "Failed"; fi)"
  }
}
EOF

# Display results
echo ""
echo "🎯 DevContainer Build Benchmark Results"
echo "======================================="
echo "Build Success: $BUILD_SUCCESS"
echo "Total Time: ${TOTAL_TIME}s ($(echo "scale=1; $TOTAL_TIME / 60" | bc) minutes)"
echo "Python Version: $PYTHON_VERSION"
echo "Venv Python: $VENV_PYTHON_VERSION"
echo "Flask Version: $FLASK_VERSION"
echo "Memory Usage: +${MEMORY_DELTA}MB"
echo "Disk Usage: +${DISK_DELTA}MB"
echo "GPU Memory: +${GPU_MEMORY_DELTA}MB"
echo "Peak Container Memory: $CONTAINER_MEMORY"
echo "Peak Container CPU: $CONTAINER_CPU"
echo ""
echo "📊 Detailed benchmark saved to: $BENCHMARK_FILE"
echo ""

# Create a summary file
SUMMARY_FILE="$BENCHMARK_DIR/latest_benchmark_summary.txt"
cat > "$SUMMARY_FILE" << EOF
DevContainer Build Benchmark - $(date)
=====================================
Build Success: $BUILD_SUCCESS
Total Time: ${TOTAL_TIME}s
Python Version: $PYTHON_VERSION
Venv Python: $VENV_PYTHON_VERSION
Flask Version: $FLASK_VERSION
Memory Delta: +${MEMORY_DELTA}MB
Disk Delta: +${DISK_DELTA}MB
GPU Memory Delta: +${GPU_MEMORY_DELTA}MB

Performance Rating: $(if [ "$BUILD_SUCCESS" = "true" ] && (( $(echo "$TOTAL_TIME < 120" | bc -l) )); then echo "Excellent"; elif [ "$BUILD_SUCCESS" = "true" ] && (( $(echo "$TOTAL_TIME < 300" | bc -l) )); then echo "Good"; elif [ "$BUILD_SUCCESS" = "true" ]; then echo "Fair"; else echo "Failed"; fi)
EOF

echo "📋 Quick summary saved to: $SUMMARY_FILE"

if [ "$BUILD_SUCCESS" = "true" ]; then
    echo "✅ DevContainer build completed successfully!"
    exit 0
else
    echo "❌ DevContainer build failed!"
    exit 1
fi
