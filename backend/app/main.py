from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.core.config import get_settings
from app.db.mongo import db
from contextlib import asynccontextmanager

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.connect()
    yield
    # Shutdown
    db.close()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.include_router(router)

import os

# Mount frontend
# We need to go up one level from 'backend' to reach 'frontend'
# Current working directory is 'backend' when running uvicorn
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

if not os.path.exists(frontend_path):
    # Fallback if running from root
    frontend_path = "frontend"

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
