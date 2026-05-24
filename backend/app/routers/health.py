from fastapi import APIRouter
from datetime import datetime
import httpx
import redis as redis_lib
from app.config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    return {
        "status": "ok",
        "app":     settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/full")
async def full_health_check():
    """Check all services are running."""
    results = {}

    # Check PostgreSQL
    try:
        from app.database import engine
        async with engine.connect() as conn:
            await conn.execute(__import__('sqlalchemy').text("SELECT 1"))
        results["postgres"] = "ok"
    except Exception as e:
        results["postgres"] = f"error: {str(e)[:50]}"

    # Check Redis
    try:
        r = redis_lib.from_url(settings.REDIS_URL)
        r.ping()
        results["redis"] = "ok"
    except Exception as e:
        results["redis"] = f"error: {str(e)[:50]}"

    # Check Ollama
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            data = resp.json()
            models = [m["name"] for m in data.get("models", [])]
            results["ollama"] = f"ok — models: {models}"
    except Exception as e:
        results["ollama"] = f"error: {str(e)[:50]}"

    # Check ChromaDB
    try:
        from app.memory.vector_store import get_chroma_client
        client = get_chroma_client()
        results["chromadb"] = f"ok — collections: {len(client.list_collections())}"
    except Exception as e:
        results["chromadb"] = f"error: {str(e)[:50]}"

    overall = "ok" if all("ok" in v for v in results.values()) else "degraded"

    return {
        "status":    overall,
        "app":       settings.APP_NAME,
        "version":   settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "services":  results,
    }
