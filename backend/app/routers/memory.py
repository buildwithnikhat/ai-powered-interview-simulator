from fastapi import APIRouter
from app.memory.retriever import (
    get_user_progress_summary,
    retrieve_past_mistakes,
    retrieve_similar_sessions,
)
from app.memory.vector_store import get_collection

router = APIRouter(prefix="/memory", tags=["memory"])


@router.get("/progress/{user_id}")
async def get_progress(user_id: str = "default_user"):
    """Get user progress summary from ChromaDB."""
    progress = get_user_progress_summary(user_id)
    return progress


@router.get("/mistakes/{user_id}")
async def get_mistakes(user_id: str = "default_user"):
    """Get user's past mistakes."""
    mistakes = retrieve_past_mistakes(user_id)
    return {"mistakes": mistakes, "count": len(mistakes)}


@router.get("/sessions/{user_id}")
async def get_sessions(user_id: str = "default_user"):
    """Get all stored sessions for a user."""
    collection = get_collection("sessions")
    try:
        results = collection.get(
            where={"user_id": user_id},
            include=["documents", "metadatas"],
        )
        sessions = []
        for i, doc in enumerate(results.get("documents", [])):
            sessions.append({
                "text": doc,
                "metadata": results["metadatas"][i] if results.get("metadatas") else {},
            })
        return {"sessions": sessions, "count": len(sessions)}
    except Exception as e:
        return {"sessions": [], "count": 0, "error": str(e)}


@router.get("/stats")
async def get_stats():
    """Get overall ChromaDB statistics."""
    try:
        sessions_col  = get_collection("sessions")
        mistakes_col  = get_collection("mistakes")
        vocab_col     = get_collection("vocabulary")
        return {
            "total_sessions":  sessions_col.count(),
            "total_mistakes":  mistakes_col.count(),
            "total_vocab":     vocab_col.count(),
            "status": "ChromaDB running",
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}


@router.delete("/reset/{user_id}")
async def reset_memory(user_id: str = "default_user"):
    """Clear all memory for a user — fresh start."""
    try:
        for col_name in ["sessions", "mistakes", "vocabulary"]:
            col = get_collection(col_name)
            results = col.get(where={"user_id": user_id})
            if results["ids"]:
                col.delete(ids=results["ids"])
        return {"message": f"Memory cleared for user {user_id}"}
    except Exception as e:
        return {"error": str(e)}
