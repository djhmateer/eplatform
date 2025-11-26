from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import os
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
import pymysql

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

# MySQL configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

if not all([MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE]):
    raise ValueError("MySQL credentials not set in environment file")

def get_db_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def query_db(sql, params=None, fetchone=False):
    """Execute a query and return results. Handles connection lifecycle."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone() if fetchone else cursor.fetchall()
    finally:
        conn.close()

app = FastAPI()

# API routes
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/servertime")
def servertime():
    return {"time": datetime.now(timezone.utc).isoformat()}


@app.get("/api/users")
def users():
    return {"users": query_db("SELECT * FROM user")}

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
