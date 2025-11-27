from contextlib import asynccontextmanager
from fastapi import FastAPI, Cookie, HTTPException, Depends, Request
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import os
import logging
from logging.handlers import RotatingFileHandler
import secrets
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
import pymysql
from pydantic import BaseModel
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Configure logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            log_dir / "1debug.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment
env = os.getenv('ENVIRONMENT')
if not env:
    raise ValueError("ENVIRONMENT variable not set. Must be 'development' or 'production'")

env_file = Path(__file__).parent / f'.env.{env}'
if not load_dotenv(env_file):
    raise FileNotFoundError(f"Environment file not found: {env_file}")

# MySQL configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

if not all([MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE]):
    raise ValueError("MySQL credentials not set in environment file")

ph = PasswordHasher()

def hash_password(password: str) -> str:
    """Hash a password using Argon2."""
    return ph.hash(password)


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

def execute_db(sql, params=None):
    """Execute a write query (INSERT, UPDATE, DELETE). Returns last insert id."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Application started - {env}")
    yield

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_request_duration(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration_ms:.1f}ms")
    return response

# Pydantic models
class AuthRequest(BaseModel):
    email: str
    password: str

# Auth dependency
def get_current_user(session_id: str = Cookie(None)):
    """Validate session cookie and return current user."""
    if not session_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    logger.debug("Querying session table for validation")
    session = query_db(
        "SELECT s.*, u.id as user_id, u.email FROM session s "
        "JOIN user u ON s.user_id = u.id "
        "WHERE s.session_id = %s AND s.expires_at > NOW()",
        (session_id,),
        fetchone=True
    )

    if not session:
        logger.debug("Session not found or expired")
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    logger.debug(f"Session valid for user: {session['email']}")
    return {"id": session["user_id"], "email": session["email"]}

# API routes
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/servertime")
def servertime():
    return {"time": datetime.now(timezone.utc).isoformat()}


@app.post("/api/register")
def register(data: AuthRequest):
    """Register a new user."""
    existing = query_db(
        "SELECT id FROM user WHERE email = %s",
        (data.email,),
        fetchone=True
    )

    if existing:
        logger.warning(f"Registration failed: email already exists - {data.email}")
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = hash_password(data.password)
    execute_db(
        "INSERT INTO user (email, password) VALUES (%s, %s)",
        (data.email, hashed)
    )

    logger.info(f"New user registered: {data.email}")
    return {"message": "Registration successful"}


@app.post("/api/login")
def login(credentials: AuthRequest):
    """Authenticate user and create session."""
    user = query_db(
        "SELECT id, email, password FROM user WHERE email = %s",
        (credentials.email,),
        fetchone=True
    )

    if not user:
        logger.warning(f"Login failed: unknown email - {credentials.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        ph.verify(user["password"], credentials.password)
    except VerifyMismatchError:
        logger.warning(f"Login failed: wrong password - {credentials.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create session
    session_id = secrets.token_urlsafe(32)
    execute_db(
        "INSERT INTO session (session_id, user_id, expires_at) "
        "VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 7 DAY))",
        (session_id, user["id"])
    )

    logger.info(f"User logged in: {credentials.email}")
    response = JSONResponse(content={"message": "Login successful", "email": user["email"]})
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=os.getenv('ENVIRONMENT') == 'production',
        samesite="lax",
        max_age=60 * 60 * 24 * 7  # 7 days
    )
    return response


@app.post("/api/logout")
def logout(session_id: str = Cookie(None)):
    """Destroy session and clear cookie."""
    if session_id:
        execute_db("DELETE FROM session WHERE session_id = %s", (session_id,))
        logger.info("User logged out")

    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie(key="session_id")
    return response


@app.get("/api/me")
def get_me(user = Depends(get_current_user)):
    """Get current logged-in user info."""
    return {"user": user}


@app.get("/api/users")
def users(_user = Depends(get_current_user)):
    return {"users": query_db("SELECT id, email FROM user")}

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
