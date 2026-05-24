from app.memory.vector_store import get_collection
from typing import List, Dict


def retrieve_similar_sessions(
    user_id: str,
    query_text: str,
    n_results: int = 3,
) -> List[Dict]:
    """
    Find past sessions semantically similar to the current transcript.
    Used to give the AI context about the user's history.
    """
    collection = get_collection("sessions")

    try:
        count = collection.count()
        if count == 0:
            return []

        results = collection.query(
            query_texts=[query_text],
            n_results=min(n_results, count),
            where={"user_id": user_id},
        )

        sessions = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                sessions.append({
                    "text": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 1.0,
                })
        return sessions

    except Exception as e:
        print(f"Retrieval error: {e}")
        return []


def retrieve_past_mistakes(
    user_id: str,
    n_results: int = 5,
) -> List[Dict]:
    """Get the user's most recent mistakes for coaching context."""
    collection = get_collection("mistakes")

    try:
        count = collection.count()
        if count == 0:
            return []

        results = collection.query(
            query_texts=["grammar pronunciation mistake error"],
            n_results=min(n_results, count),
            where={"user_id": user_id},
        )

        mistakes = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                mistakes.append({
                    "text": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                })
        return mistakes

    except Exception as e:
        print(f"Mistake retrieval error: {e}")
        return []


def get_user_progress_summary(user_id: str) -> Dict:
    """
    Generate a summary of user progress from stored sessions.
    Used by the AI to personalize coaching.
    """
    collection = get_collection("sessions")

    try:
        count = collection.count()
        if count == 0:
            return {
                "total_sessions": 0,
                "avg_fluency": 0,
                "avg_confidence": 0,
                "avg_grammar": 0,
                "most_common_weakness": "fluency",
                "summary": "This is your first session. Welcome to AI-COS!",
            }

        # Get all sessions for this user
        results = collection.get(
            where={"user_id": user_id},
            include=["metadatas"],
        )

        if not results["metadatas"]:
            return {
                "total_sessions": 0,
                "avg_fluency": 0,
                "avg_confidence": 0,
                "avg_grammar": 0,
                "most_common_weakness": "fluency",
                "summary": "Starting fresh — let us build your communication profile!",
            }

        metadatas = results["metadatas"]
        total = len(metadatas)

        avg_fluency    = sum(m.get("fluency_score", 0) for m in metadatas) / total
        avg_confidence = sum(m.get("confidence_score", 0) for m in metadatas) / total
        avg_grammar    = sum(m.get("grammar_score", 0) for m in metadatas) / total

        # Find most common weak area
        weaknesses = [m.get("weakest_area", "") for m in metadatas if m.get("weakest_area")]
        most_common = max(set(weaknesses), key=weaknesses.count) if weaknesses else "fluency"

        summary = f"""You have completed {total} sessions.
Average fluency: {avg_fluency:.0f}/100
Average confidence: {avg_confidence:.0f}/100
Average grammar: {avg_grammar:.0f}/100
Your biggest focus area: {most_common}"""

        return {
            "total_sessions": total,
            "avg_fluency": round(avg_fluency),
            "avg_confidence": round(avg_confidence),
            "avg_grammar": round(avg_grammar),
            "most_common_weakness": most_common,
            "summary": summary,
        }

    except Exception as e:
        print(f"Progress summary error: {e}")
        return {
            "total_sessions": 0,
            "summary": "Building your profile...",
        }
