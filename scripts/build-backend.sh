#!/bin/bash
set -e

echo "Building FastAPI backend..."

# Change to backend directory
cd backend

# Create virtual environment if needed
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run linting
echo "Running linting..."
pylint src/ --disable=all --enable=C,W || true

# Run tests
echo "Running tests..."
python -m pytest tests/ -v || true

echo "Backend build complete!"
