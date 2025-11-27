#!/bin/bash

# this is for the test webserver to pull latest code and restart the server

# Kill any existing instances
echo "Killing anything on port 3000..."
sudo netstat -tulnp | grep 3000 | awk '{print $7}' | cut -d'/' -f1 | xargs -r sudo kill -9

echo "Step 1: Pulling latest changes..."
git pull

echo "Step 2: Updating CLIENT FRONTEND dependencies with pnpm..."
cd client
# pnpm install --frozen-lockfile
# may modify lockfile 
pnpnm install

echo "Step 3: Building frontend with pnpm..."
pnpm build

echo "Step 4: Installing SERVER BACKEND dependencies with uv lock --upgrade and uv sync..."
cd ../server
uv lock --upgrade
uv sync

echo "Step 5: Starting FastAPI server..."

# Set test environment
export ENVIRONMENT=test

# see notes on workers for production deployment
# have hacked in 3000 (not 8000) to as just easier for test as old process for node ran on this.
uv run uvicorn main:app --host 0.0.0.0 --port 3000

