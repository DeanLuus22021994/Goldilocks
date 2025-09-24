#!/bin/bash

# Devcontainer lock file generator and cache manager
# This script creates and updates devcontainer-lock.json for build reproducibility

set -e

LOCK_FILE=".devcontainer/devcontainer-lock.json"

echo "🔒 Generating devcontainer lock file..."

# Function to compute SHA256 hash of a file
hash_file() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        shasum -a 256 "$1" | cut -d' ' -f1
    else
        sha256sum "$1" | cut -d' ' -f1
    fi
}

# Function to compute SHA256 hash of a string
hash_string() {
    echo -n "$1" | sha256sum | cut -d' ' -f1
}

# Get current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")

# Read current devcontainer.json
DEVCONTAINER_HASH=$(hash_file ".devcontainer/devcontainer.json")

# Get requirements.txt hash
REQUIREMENTS_HASH=""
if [[ -f "requirements.txt" ]]; then
    REQUIREMENTS_HASH=$(hash_file "requirements.txt")
fi

# Get package.json hash
PACKAGE_JSON_HASH=""
if [[ -f "package.json" ]]; then
    PACKAGE_JSON_HASH=$(hash_file "package.json")
fi

# Get Python packages from requirements.txt
PYTHON_PACKAGES="{}"
if [[ -f "requirements.txt" ]]; then
    PYTHON_PACKAGES=$(python3 -c "
import json
packages = {}
try:
    with open('requirements.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('-'):
                if '==' in line:
                    name, version = line.split('==', 1)
                    packages[name.strip()] = version.strip()
                elif line:
                    packages[line] = 'latest'
except:
    pass
print(json.dumps(packages, indent=2))
")
fi

# Get Node packages from package.json
NODE_PACKAGES="{}"
if [[ -f "package.json" ]]; then
    NODE_PACKAGES=$(python3 -c "
import json
try:
    with open('package.json', 'r') as f:
        data = json.load(f)
        deps = {}
        deps.update(data.get('dependencies', {}))
        deps.update(data.get('devDependencies', {}))
        print(json.dumps(deps, indent=2))
except:
    print('{}')
")
fi

# Get Docker version
DOCKER_VERSION=""
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | grep -oP '\d+\.\d+\.\d+')
fi

# Get system info
OS_TYPE=$(uname -s)

# Create the lock file
cat > "$LOCK_FILE" << EOF
{
  "\$schema": "https://json-schema.org/draft-07/schema",
  "version": "1.0.0",
  "generated": "$TIMESTAMP",
  "lockfile": {
    "devcontainer": {
      "hash": "$DEVCONTAINER_HASH",
      "image": "mcr.microsoft.com/devcontainers/python:1-3.14.0-trixie",
      "features": {
        "node": {
          "version": "22",
          "hash": "sha256:placeholder"
        }
      }
    },
    "python": {
      "version": "$(python3 --version | cut -d' ' -f2)",
      "pip": {
        "version": "$(pip --version | grep -oP '\\d+\\.\\d+\\.\\d+')",
        "hash": "sha256:placeholder"
      },
      "packages": $PYTHON_PACKAGES,
      "requirements_hash": "$REQUIREMENTS_HASH"
    },
    "node": {
      "version": "$(node --version 2>/dev/null | sed 's/v//' || echo 'not-installed')",
      "npm": {
        "version": "$(npm --version 2>/dev/null || echo 'not-installed')",
        "hash": "sha256:placeholder"
      },
      "packages": $NODE_PACKAGES,
      "package_json_hash": "$PACKAGE_JSON_HASH"
    },
    "system": {
      "base_image": "mcr.microsoft.com/devcontainers/python:1-3.14.0-trixie",
      "base_hash": "sha256:placeholder",
      "apt_packages": [],
      "cache_paths": [
        "/home/vscode/.cache/pip",
        "/home/vscode/.npm",
        "/home/vscode/.cache/uv",
        "/home/vscode/.vscode-server",
        "/home/vscode/.vscode-server/extensions"
      ]
    }
  },
  "cache": {
    "volumes": {
      "goldilocks-venv": {
        "created": "$TIMESTAMP",
        "size": "$(docker volume inspect goldilocks-venv --format '{{.Mountpoint}}' 2>/dev/null | xargs du -sh 2>/dev/null | cut -f1 || echo 'unknown')",
        "python_version": "$(python3 --version | cut -d' ' -f2)"
      },
      "goldilocks-node-modules": {
        "created": "$TIMESTAMP",
        "size": "$(docker volume inspect goldilocks-node-modules --format '{{.Mountpoint}}' 2>/dev/null | xargs du -sh 2>/dev/null | cut -f1 || echo 'unknown')",
        "node_version": "$(node --version 2>/dev/null | sed 's/v//' || echo 'not-installed')"
      },
      "goldilocks-bytecode": {
        "created": "$TIMESTAMP",
        "size": "$(docker volume inspect goldilocks-bytecode --format '{{.Mountpoint}}' 2>/dev/null | xargs du -sh 2>/dev/null | cut -f1 || echo 'unknown')",
        "python_optimize": 2
      },
      "pip-cache": {
        "created": "$TIMESTAMP",
        "size": "$(docker volume inspect pip-cache --format '{{.Mountpoint}}' 2>/dev/null | xargs du -sh 2>/dev/null | cut -f1 || echo 'unknown')"
      },
      "npm-cache": {
        "created": "$TIMESTAMP",
        "size": "$(docker volume inspect npm-cache --format '{{.Mountpoint}}' 2>/dev/null | xargs du -sh 2>/dev/null | cut -f1 || echo 'unknown')"
      }
    }
  },
  "build_info": {
    "os": "$OS_TYPE",
    "docker_version": "$DOCKER_VERSION",
    "build_time": "$TIMESTAMP",
    "cache_hit_rate": 0
  }
}
EOF

echo "✅ Lock file generated: $LOCK_FILE"
echo "🔍 Summary:"
echo "  - DevContainer hash: $DEVCONTAINER_HASH"
echo "  - Requirements hash: $REQUIREMENTS_HASH"
echo "  - Package.json hash: $PACKAGE_JSON_HASH"
echo "  - Python version: $(python3 --version | cut -d' ' -f2)"
echo "  - Node version: $(node --version 2>/dev/null || echo 'not-installed')"
