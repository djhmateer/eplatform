#!/bin/bash

# Load production environment variables to get PORT
cd "$(dirname "$0")/server"
export $(grep -v '^#' .env.production | xargs)
cd ..

# Kill any existing instances
echo "Killing anything on port ${PORT:-3000}..."
lsof -ti:${PORT:-3000} | xargs -r kill -9

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

# Load production environment variables
export $(grep -v '^#' .env.production | xargs)

# see notes on workers
uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-3000} --workers 4

#   For even better performance, consider using Gunicorn with uvicorn workers:
#   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000

#   This gives you Gunicorn's process management with uvicorn's async performance.

