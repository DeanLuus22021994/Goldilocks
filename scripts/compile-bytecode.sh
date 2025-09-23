#!/bin/bash

# Python bytecode precompilation script
# Compiles Python files to optimized bytecode for faster startup

set -e

echo "🐍 Precompiling Python bytecode..."

# Configuration
SRC_DIR="src"
OPTIMIZE_LEVEL=2
CACHE_DIR="__pycache__"
FORCE_RECOMPILE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--force)
            FORCE_RECOMPILE=true
            shift
            ;;
        -o|--optimize)
            OPTIMIZE_LEVEL="$2"
            shift 2
            ;;
        -s|--src)
            SRC_DIR="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -f, --force      Force recompilation of all files"
            echo "  -o, --optimize   Optimization level (0, 1, or 2, default: 2)"
            echo "  -s, --src        Source directory (default: src)"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate optimization level
if [[ "$OPTIMIZE_LEVEL" != "0" && "$OPTIMIZE_LEVEL" != "1" && "$OPTIMIZE_LEVEL" != "2" ]]; then
    echo "Error: Optimization level must be 0, 1, or 2"
    exit 1
fi

# Check if source directory exists
if [[ ! -d "$SRC_DIR" ]]; then
    echo "Error: Source directory '$SRC_DIR' does not exist"
    exit 1
fi

# Remove old bytecode if force recompile
if [[ "$FORCE_RECOMPILE" == "true" ]]; then
    echo "🧹 Cleaning old bytecode files..."
    find "$SRC_DIR" -name "*.pyc" -delete
    find "$SRC_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
fi

# Set optimization environment variable
export PYTHONOPTIMIZE="$OPTIMIZE_LEVEL"

echo "📦 Compiling Python files in $SRC_DIR (optimization level: $OPTIMIZE_LEVEL)..."

# Compile Python files to bytecode
python -m compileall \
    -b \
    -f \
    --invalidation-mode unchecked-hash \
    "$SRC_DIR"

# Count compiled files
PYFILE_COUNT=$(find "$SRC_DIR" -name "*.py" | wc -l)
PYCFILE_COUNT=$(find "$SRC_DIR" -name "*.pyc" | wc -l)

echo "✅ Bytecode compilation complete!"
echo "📊 Statistics:"
echo "  - Python files: $PYFILE_COUNT"
echo "  - Bytecode files: $PYCFILE_COUNT"
echo "  - Optimization level: $OPTIMIZE_LEVEL"

# Optional: Remove source .py files for production (commented out by default)
# echo "🔧 Removing source .py files for production..."
# find "$SRC_DIR" -name "*.py" -delete

# Create bytecode manifest for caching
echo "📝 Creating bytecode manifest..."
cat > "$CACHE_DIR/manifest.json" << EOF
{
  "generated": "$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")",
  "optimization_level": $OPTIMIZE_LEVEL,
  "source_directory": "$SRC_DIR",
  "python_version": "$(python --version | cut -d' ' -f2)",
  "files": {
$(find "$SRC_DIR" -name "*.pyc" -exec basename {} .pyc \; | sed 's/^/    "/; s/$/": true,/' | sed '$ s/,$//')
  }
}
EOF

echo "🎉 Python bytecode precompilation complete!"
echo "💡 To use bytecode-only mode, set PYTHONOPTIMIZE=$OPTIMIZE_LEVEL and remove .py files"
