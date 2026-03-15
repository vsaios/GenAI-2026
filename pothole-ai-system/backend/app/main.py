"""FastAPI app with chatbot and reports."""
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Fixed import — use relative path instead of app.
from database.db import engine, Base
from routes.reports import router as reports_router

try:
    from routes.chat import router as chat_router
    CHAT_AVAILABLE = True
except Exception as e:
    print(f"[Chat] Chat router unavailable: {e}")
    chat_router = None
    CHAT_AVAILABLE = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Rua API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if CHAT_AVAILABLE:
    app.include_router(chat_router)
app.include_router(reports_router, prefix="/api", tags=["reports"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.get("/")
def root():
    return {"status": "Pothole AI backend is running"}