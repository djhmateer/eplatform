#!/bin/bash

# Kill any existing instances
echo "Killing anything on port 8000..."
sudo netstat -tulnp | grep 8000 | awk '{print $7}' | cut -d'/' -f1 | xargs -r sudo kill -9

echo "Step 1: Pulling latest changes..."
git pull

echo "Step 2: Installing frontend dependencies..."
cd client
pnpm install --frozen-lockfile

echo "Step 3: Building frontend..."
step_start=$(date +%s)
pnpm build
step_end=$(date +%s)
echo "Build completed in $((step_end - step_start)) seconds"

echo "Step 4: Installing backend dependencies..."
cd ../server
uv sync

echo "Step 5: Starting FastAPI server..."
uv run uvicorn main:app --host 0.0.0.0 --port 8000
