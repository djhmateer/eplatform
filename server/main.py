from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# API routes
@app.get("/api/health")
def health():
    return {"status": "ok"}


# Serve frontend in production
dist_path = Path(__file__).parent.parent / "client" / "dist"
if dist_path.exists():
    app.mount("/assets", StaticFiles(directory=dist_path / "assets"), name="assets")

    @app.get("/{path:path}")
    def serve_frontend(path: str):
        file_path = dist_path / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(dist_path / "index.html")
