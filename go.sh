#!/bin/bash

# Kill any existing instances
echo "Killing anything on port 3000..."
sudo netstat -tulnp | grep 3000 | awk '{print $7}' | cut -d'/' -f1 | xargs -r sudo kill -9

echo "Step 1: Pulling latest changes..."
git pull

echo "Step 2: Updating frontend dependencies with pnpm..."
cd client
pnpm install --frozen-lockfile

echo "Step 3: Building frontend with pnpm..."
pnpm build

echo "Step 4: Installing backend dependencies with uv lock --upgrade and uv sync..."
cd ../server
uv lock --upgrade
uv sync

echo "Step 5: Starting FastAPI server..."

# Set production environment
export ENVIRONMENT=production

# see notes on workers for production deployment
# uv run uvicorn main:app --host 0.0.0.0 --port 3000 --workers 4
uv run uvicorn main:app --host 0.0.0.0 --port 3000

