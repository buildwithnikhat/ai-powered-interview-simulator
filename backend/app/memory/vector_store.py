import chromadb
from chromadb.config import Settings
import os
from app.config import settings


# Global ChromaDB client — initialized once
_client = None
_collections = {}


def get_chroma_client():
    """Get or create the ChromaDB client."""
    global _client
    if _client is None:
        persist_dir = os.path.abspath(settings.CHROMA_PERSIST_DIR)
        os.makedirs(persist_dir, exist_ok=True)

        _client = chromadb.PersistentClient(
            path=persist_dir,
        )
        print(f"✅ ChromaDB initialized at {persist_dir}")
    return _client


def get_collection(name: str):
    """Get or create a ChromaDB collection."""
    global _collections
    if name not in _collections:
        client = get_chroma_client()
        _collections[name] = client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
    return _collections[name]


def store_session_memory(
    user_id: str,
    session_id: str,
    transcript: str,
    coaching_response: str,
    scores: dict,
    metadata: dict = None,
):
    """
    Store a conversation session in ChromaDB.
    The text is embedded automatically by ChromaDB.
    """
    collection = get_collection("sessions")

    # Create a rich text representation for embedding
    text = f"""
User said: {transcript}
AI coaching: {coaching_response}
Fluency: {scores.get('fluency_score', 0)}
Confidence: {scores.get('confidence_score', 0)}
Grammar: {scores.get('grammar_score', 0)}
Fillers: {scores.get('filler_count', 0)}
Words: {scores.get('word_count', 0)}
""".strip()

    doc_metadata = {
        "user_id": user_id,
        "session_id": session_id,
        "fluency_score": float(scores.get("fluency_score", 0)),
        "confidence_score": float(scores.get("confidence_score", 0)),
        "grammar_score": float(scores.get("grammar_score", 0)),
        "filler_count": int(scores.get("filler_count", 0)),
        "word_count": int(scores.get("word_count", 0)),
        "weakest_area": str(scores.get("weakest_area", "")),
    }

    if metadata:
        doc_metadata.update(metadata)

    collection.upsert(
        ids=[session_id],
        documents=[text],
        metadatas=[doc_metadata],
    )


def store_mistake(
    user_id: str,
    mistake_id: str,
    mistake_type: str,
    original_text: str,
    corrected_text: str,
    explanation: str,
):
    """Store a grammar or pronunciation mistake for pattern tracking."""
    collection = get_collection("mistakes")

    text = f"""
Mistake type: {mistake_type}
Original: {original_text}
Corrected: {corrected_text}
Explanation: {explanation}
""".strip()

    collection.upsert(
        ids=[mistake_id],
        documents=[text],
        metadatas={
            "user_id": user_id,
            "mistake_type": mistake_type,
            "original_text": original_text,
            "corrected_text": corrected_text,
        }
    )


def store_vocabulary(
    user_id: str,
    word: str,
    definition: str,
    example: str,
    mastery_level: int = 0,
):
    """Store a vocabulary word for the user."""
    collection = get_collection("vocabulary")

    text = f"Word: {word}. Definition: {definition}. Example: {example}"

    collection.upsert(
        ids=[f"{user_id}_{word}"],
        documents=[text],
        metadatas={
            "user_id": user_id,
            "word": word,
            "definition": definition,
            "example": example,
            "mastery_level": mastery_level,
        }
    )
