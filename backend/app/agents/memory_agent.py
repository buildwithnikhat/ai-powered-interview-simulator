import uuid
from app.agents.base import BaseAgent
from app.memory.vector_store import store_session_memory, store_mistake
from app.memory.retriever import retrieve_similar_sessions, get_user_progress_summary


class MemoryAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="Memory Agent",
            description="Persistent memory using ChromaDB"
        )

    async def analyze(self, state: dict) -> dict:
        transcript    = state.get("transcript", "")
        user_id       = state.get("user_id", "default_user")
        session_id    = state.get("session_id", str(uuid.uuid4()))
        coaching_resp = state.get("conversation_response", "")
        grammar_issues= state.get("grammar_issues", [])
        grammar_corr  = state.get("grammar_correction", "")
        grammar_tip   = state.get("grammar_tip", "")

        print(f"[Memory Agent] user={user_id} transcript='{transcript[:50]}' coaching='{coaching_resp[:50]}'")

        scores = {
            "fluency_score":       state.get("fluency_score", 0),
            "confidence_score":    state.get("confidence_score", 0),
            "grammar_score":       state.get("grammar_score", 0),
            "pronunciation_score": state.get("pronunciation_score", 0),
            "filler_count":        state.get("filler_count", 0),
            "word_count":          state.get("word_count", 0),
            "weakest_area":        state.get("weakest_area", ""),
        }

        # Retrieve past sessions for context
        past_sessions = []
        if transcript:
            try:
                past_sessions = retrieve_similar_sessions(
                    user_id=user_id,
                    query_text=transcript,
                    n_results=3,
                )
                print(f"[Memory Agent] Retrieved {len(past_sessions)} past sessions")
            except Exception as e:
                print(f"[Memory Agent] Retrieval error: {e}")

        # Get progress summary
        try:
            progress = get_user_progress_summary(user_id)
        except Exception as e:
            print(f"[Memory Agent] Progress error: {e}")
            progress = {"total_sessions": 0, "summary": "Starting fresh"}

        # Store this session
        if transcript:
            try:
                store_session_memory(
                    user_id=user_id,
                    session_id=session_id,
                    transcript=transcript,
                    coaching_response=coaching_resp or "No response yet",
                    scores=scores,
                )
                print(f"[Memory Agent] ✅ Session stored: {session_id}")
            except Exception as e:
                print(f"[Memory Agent] ❌ Store error: {e}")
                import traceback
                traceback.print_exc()

        # Store grammar mistakes
        if grammar_issues and grammar_corr:
            try:
                store_mistake(
                    user_id=user_id,
                    mistake_id=str(uuid.uuid4()),
                    mistake_type="grammar",
                    original_text=transcript,
                    corrected_text=grammar_corr,
                    explanation=grammar_tip,
                )
                print(f"[Memory Agent] ✅ Mistake stored")
            except Exception as e:
                print(f"[Memory Agent] ❌ Mistake store error: {e}")

        # Build memory context
        total = progress.get("total_sessions", 0)
        if total == 0:
            memory_context = "First session — building your communication profile."
        else:
            memory_context = progress.get("summary", "")

        state["memory_context"]   = memory_context
        state["session_count"]    = total
        state["progress_summary"] = progress
        state["past_sessions"]    = past_sessions
        state["session_id"]       = session_id

        return state
