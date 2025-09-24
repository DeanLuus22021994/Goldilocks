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

# Get pyproject.toml hash
PYPROJECT_TOML_HASH=""
if [[ -f "pyproject.toml" ]]; then
    PYPROJECT_TOML_HASH=$(hash_file "pyproject.toml")
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

# Get TOML packages from pyproject.toml
TOML_PACKAGES="{}"
if [[ -f "pyproject.toml" ]]; then
    TOML_PACKAGES=$(python3 -c "
import json
import re
packages = {}
try:
    with open('pyproject.toml', 'r') as f:
        content = f.read()
        # Basic parsing for [tool.poetry.dependencies] section
        match = re.search(r'\[tool\.poetry\.dependencies\](.*?)(?=\[|\Z)', content, re.DOTALL)
        if match:
            deps_section = match.group(1)
            for line in deps_section.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        name = parts[0].strip()
                        version = parts[1].strip().strip('\"').strip(\"'\")
                        packages[name] = version
except:
    pass
print(json.dumps(packages, indent=2))
")
fi

# Get tool versions
GIT_VERSION=$(git --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' || echo "unknown")
GITHUB_CLI_VERSION=$(gh --version 2>/dev/null | head -n1 | cut -d' ' -f3 || echo "unknown")
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
      "image": "goldilocks:devcontainer",
      "features": {
        "git": {
          "version": "$GIT_VERSION",
          "source": "apt-install",
          "hash": "manual"
        },
        "github-cli": {
          "version": "$GITHUB_CLI_VERSION",
          "source": "apt-install",
          "hash": "manual"
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
      "requirements_hash": "$REQUIREMENTS_HASH",
      "toml_packages": $TOML_PACKAGES,
      "pyproject_hash": "$PYPROJECT_TOML_HASH",
      "python_sha256": "646dc945e49c73a141896deda12d43f3f293fd69426774c16fc43496180e8fcd"
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
      "base_image": "goldilocks:devcontainer",
      "base_hash": "sha256:646dc945e49c73a141896deda12d43f3f293fd69426774c16fc43496180e8fcd",
      "apt_packages": ["git", "gh"],
      "cache_paths": [
        "/home/app/.cache/pip",
        "/home/app/.npm",
        "/home/app/.cache/uv",
        "/home/app/.vscode-server",
        "/home/app/.vscode-server/extensions"
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
    "cache_hit_rate": 0,
    "tools": {
      "git": "$GIT_VERSION",
      "github_cli": "$GITHUB_CLI_VERSION"
    }
  }
}
EOF

echo "✅ Lock file generated: $LOCK_FILE"
echo "🔍 Summary:"
echo "  - DevContainer hash: $DEVCONTAINER_HASH"
echo "  - Requirements hash: $REQUIREMENTS_HASH"
echo "  - Package.json hash: $PACKAGE_JSON_HASH"
echo "  - Pyproject.toml hash: $PYPROJECT_TOML_HASH"
echo "  - Python version: $(python3 --version | cut -d' ' -f2)"
echo "  - Node version: $(node --version 2>/dev/null || echo 'not-installed')"
echo "  - Git version: $GIT_VERSION"
echo "  - GitHub CLI version: $GITHUB_CLI_VERSION"
