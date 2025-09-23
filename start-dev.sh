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
