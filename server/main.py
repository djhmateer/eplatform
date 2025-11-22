from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
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
env_loaded = load_dotenv(env_file)

logger.info(f"Env file path: {env_file}")
logger.info(f"Env file loaded: {'SUCCESS' if env_loaded else 'NOT FOUND'}")
logger.info(f"PORT from env: {os.getenv('PORT', 'not set')}")

app = FastAPI()

# Add CORS middleware for development
if env == 'development':
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # Vite dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS enabled for development")

DIST_PATH = Path(__file__).parent.parent / "client" / "dist"

# API routes
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/servertime")
def servertime():
    return {"time": datetime.now(timezone.utc).isoformat()}

# Serve frontend react in production
# in dev use vite dev server
@app.get("/{path:path}")
def serve_frontend(path: str):
    if not DIST_PATH.exists():
        return {"error": "Frontend not built"}

    file_path = DIST_PATH / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(DIST_PATH / "index.html")
