from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import os
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment-specific variables
env = os.getenv('ENVIRONMENT')
if not env:
    raise ValueError("ENVIRONMENT variable not set. Must be 'development' or 'production'")
logger.info(f"Environment: {env}")

# Load environment file from server directory
env_file = Path(__file__).parent / f'.env.{env}'
logger.info(f"Env file path: {env_file}")

env_loaded = load_dotenv(env_file)
if not env_loaded:
    raise FileNotFoundError(f"Environment file not found: {env_file}")
logger.info(f"Env file loaded successfully")

port = os.getenv('PORT')
if not port:
    raise ValueError("PORT not set in environment file")
logger.info(f"PORT from env: {port}")

app = FastAPI()

# API routes
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/servertime")
def servertime():
    return {"time": datetime.now(timezone.utc).isoformat()}

# Serve frontend react in production
# in dev use vite dev server
DIST_PATH = Path(__file__).parent.parent / "client" / "dist"
@app.get("/{path:path}")
def serve_frontend(path: str):
    if not DIST_PATH.exists():
        return {"error": "Frontend not built"}

    file_path = DIST_PATH / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(DIST_PATH / "index.html")
