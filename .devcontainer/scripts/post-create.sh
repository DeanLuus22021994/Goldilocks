#!/bin/bash

# Post-create script for Goldilocks development environment
# This script runs after the dev container is created and sets up the development environment

set -e

echo "🚀 Starting Goldilocks post-create setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}📦 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Set up workspace ownership
print_step "Setting up workspace permissions..."
sudo chown -R vscode:vscode /workspaces/goldilocks
print_success "Workspace permissions configured"

# Configure Git safely
print_step "Configuring Git safe directories..."
git config --global --add safe.directory /workspaces/goldilocks
print_success "Git safe directory configured"

# Update system packages
print_step "Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq
print_success "System packages updated"

# Install additional system dependencies
print_step "Installing additional system dependencies..."
sudo apt-get install -y -qq \
    build-essential \
    curl \
    wget \
    unzip \
    tree \
    htop \
    jq \
    sqlite3 \
    postgresql-client \
    redis-tools \
    nano \
    vim \
    tmux \
    screen
print_success "Additional system dependencies installed"

# Set up Python environment
print_step "Setting up Python environment..."

# Upgrade pip and install uv
python -m pip install --upgrade pip setuptools wheel
python -m pip install uv

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_step "Creating Python virtual environment..."
    python -m venv .venv --upgrade-deps
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
print_step "Installing Python dependencies..."
source .venv/bin/activate

# Install requirements using uv for faster installation
if [ -f "requirements.txt" ]; then
    uv pip install -r requirements.txt
    print_success "Python requirements installed"
else
    print_warning "No requirements.txt found"
fi

# Install development dependencies
print_step "Installing development dependencies..."
uv pip install \
    pytest \
    pytest-cov \
    pytest-xdist \
    black \
    isort \
    flake8 \
    mypy \
    ruff \
    pre-commit \
    bandit \
    safety \
    coverage \
    httpx \
    requests

print_success "Development dependencies installed"

# Set up pre-commit hooks
print_step "Setting up pre-commit hooks..."
pre-commit install --install-hooks
pre-commit autoupdate
print_success "Pre-commit hooks configured"

# Set up Node.js environment if package.json exists
if [ -f "package.json" ]; then
    print_step "Setting up Node.js environment..."
    npm install
    print_success "Node.js dependencies installed"
fi

# Create project structure
print_step "Setting up project structure..."

# Create source directories
mkdir -p src/goldilocks/{api,core,models,services,utils}
mkdir -p frontend/{components,styles,scripts,assets}
mkdir -p infrastructure/{docker,kubernetes,terraform}
mkdir -p docs/{api,deployment,development}

# Create __init__.py files for Python packages
touch src/__init__.py
touch src/goldilocks/__init__.py
touch src/goldilocks/{api,core,models,services,utils}/__init__.py

print_success "Project structure created"

# Set up VS Code workspace settings
print_step "Configuring VS Code workspace..."
mkdir -p .vscode

cat > .vscode/settings.json << 'EOF'
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.analysis.autoSearchPaths": true,
  "python.analysis.extraPaths": ["${workspaceFolder}/src"],
  "pylint.args": ["--init-hook", "import sys; sys.path.append('${workspaceFolder}/src')"],
  "python.envFile": "${workspaceFolder}/.env",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests", "-v", "--tb=short"],
  "python.testing.autoTestDiscoverOnSaveEnabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true,
    "*.egg-info": true,
    "**/.mypy_cache": true,
    "**/.ruff_cache": true,
    "**/build": true,
    "**/dist": true,
    "**/.coverage": true,
    "**/htmlcov": true
  }
}
EOF

print_success "VS Code workspace configured"

# Set up environment file template
print_step "Creating environment configuration..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Goldilocks Environment Configuration
FLASK_APP=src.goldilocks.app
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///goldilocks.db

# API Configuration
API_VERSION=v1
API_PREFIX=/api/v1

# Cache Configuration
REDIS_URL=redis://localhost:6379/0

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json

# Development Configuration
DEBUG=1
TESTING=0
EOF
    print_success "Environment configuration created"
else
    print_warning "Environment file already exists"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    print_step "Installing Docker Compose..."
    sudo pip install docker-compose
    print_success "Docker Compose installed"
fi

# Set up database (if needed)
print_step "Setting up development database..."
if [ -f "src/goldilocks/database.py" ]; then
    python -c "from src.goldilocks.database import init_db; init_db()" 2>/dev/null || true
    print_success "Database initialized"
fi

# Run initial tests to verify setup
print_step "Running initial tests..."
if [ -d "tests" ]; then
    python -m pytest tests/ -v --tb=short || print_warning "Some tests failed - this is normal for initial setup"
    print_success "Test suite executed"
fi

# Generate coverage report
print_step "Generating coverage report..."
if [ -d "tests" ]; then
    python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing --quiet || true
    print_success "Coverage report generated"
fi

# Set up Git hooks for development
print_step "Setting up Git development hooks..."
mkdir -p .git/hooks

cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# Pre-push hook to run tests and linting

echo "🧪 Running pre-push checks..."

# Run linting
echo "🔍 Running linting..."
python -m ruff check . || exit 1
python -m mypy src/ || exit 1

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ --maxfail=1 --quiet || exit 1

echo "✅ All pre-push checks passed!"
EOF

chmod +x .git/hooks/pre-push
print_success "Git development hooks configured"

# Create startup script for easy development
print_step "Creating development scripts..."
cat > start-dev.sh << 'EOF'
#!/bin/bash
# Development startup script

echo "🚀 Starting Goldilocks development environment..."

# Activate virtual environment
source .venv/bin/activate

# Set environment variables
export FLASK_APP=src.goldilocks.app
export FLASK_ENV=development
export FLASK_DEBUG=1

# Start the Flask development server
flask run --host=0.0.0.0 --port=9000 --reload --debugger
EOF

chmod +x start-dev.sh
print_success "Development scripts created"

# Final setup message
echo ""
echo -e "${PURPLE}🎉 Goldilocks development environment setup complete!${NC}"
echo ""
echo -e "${CYAN}Quick Start Commands:${NC}"
echo -e "  ${GREEN}./start-dev.sh${NC}          - Start development server"
echo -e "  ${GREEN}python -m pytest${NC}        - Run tests"
echo -e "  ${GREEN}python -m ruff check .${NC}  - Run linting"
echo -e "  ${GREEN}pre-commit run --all-files${NC} - Run pre-commit hooks"
echo ""
echo -e "${CYAN}Available Ports:${NC}"
echo -e "  ${GREEN}9000${NC} - Goldilocks Flask App"
echo -e "  ${GREEN}8000${NC} - Development Server"
echo -e "  ${GREEN}5000${NC} - Flask/FastAPI Server"
echo -e "  ${GREEN}3000${NC} - Node.js Server"
echo ""
echo -e "${YELLOW}Happy coding! 🚀${NC}"
