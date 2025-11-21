from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

DIST_PATH = Path(__file__).parent.parent / "client" / "dist"


# API routes
@app.get("/api/health")
def health():
    return {"status": "ok"}


# Serve frontend in production
@app.get("/{path:path}")
def serve_frontend(path: str):
    if not DIST_PATH.exists():
        return {"error": "Frontend not built"}

    file_path = DIST_PATH / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(DIST_PATH / "index.html")
