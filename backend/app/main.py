from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.database import engine, Base
from app.routers import health
from app.routers import voice
from app.routers import memory
from app.routers import interview

os.makedirs(settings.AUDIO_UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
os.makedirs("static", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from app.memory.vector_store import get_chroma_client
    get_chroma_client()

    from app.orchestrator.graph import orchestrator
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} started")
    print(f"✅ 10 agents loaded")
    print(f"✅ ChromaDB memory ready")
    print(f"✅ Interview system ready")

    yield
    await engine.dispose()
    print("🛑 AI-COS shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Communication Operating System",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://127.0.0.1:3000",
        "http://localhost:8000", "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(voice.router)
app.include_router(memory.router)
app.include_router(interview.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {
        "message":       "AI-COS — Complete Communication Platform",
        "version":       settings.APP_VERSION,
        "agents":        10,
        "docs":          "/docs",
        "voice_ui":      "http://localhost:8000/static/test_voice.html",
        "interview_ui":  "http://localhost:8000/static/interview.html",
        "memory_stats":  "http://localhost:8000/memory/stats",
    }
