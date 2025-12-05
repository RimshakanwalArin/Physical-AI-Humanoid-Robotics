#!/bin/bash
set -e

echo "Building Docusaurus frontend..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing npm dependencies..."
  npm install
fi

# Build static site
npm run build

echo "Frontend build complete! Output in ./build"
