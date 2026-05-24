from app.agents.base import BaseAgent
from datetime import datetime


class AnalyticsAgent(BaseAgent):
    """
    Tracks progress across all sessions.
    Calculates overall communication score and improvement trends.
    """

    def __init__(self):
        super().__init__(
            name="Analytics Agent",
            description="Tracks progress and calculates overall communication score"
        )

    async def analyze(self, state: dict) -> dict:
        # Gather all scores from other agents
        fluency_score      = state.get("fluency_score", 0)
        grammar_score      = state.get("grammar_score", 0)
        confidence_score   = state.get("confidence_score", 0)
        pronunciation_score= state.get("pronunciation_score", 0)
        vocab_score        = state.get("vocab_score", 0)

        # Calculate weighted overall score
        scores = [s for s in [
            fluency_score, grammar_score,
            confidence_score, pronunciation_score, vocab_score
        ] if s > 0]

        overall_score = round(sum(scores) / len(scores)) if scores else 0

        # Find the weakest area
        score_map = {
            "fluency":       fluency_score,
            "grammar":       grammar_score,
            "confidence":    confidence_score,
            "pronunciation": pronunciation_score,
            "vocabulary":    vocab_score,
        }
        weakest = min(score_map, key=score_map.get) if scores else "fluency"
        strongest = max(score_map, key=score_map.get) if scores else "confidence"

        # Generate overall feedback
        if overall_score >= 90:
            overall_feedback = "Outstanding performance! You are communicating at a professional level."
        elif overall_score >= 75:
            overall_feedback = f"Great job! Focus on improving your {weakest} to reach the next level."
        elif overall_score >= 60:
            overall_feedback = f"Good progress! Your {strongest} is strong. Work on your {weakest} next."
        else:
            overall_feedback = f"Keep practicing! Focus on {weakest} — small daily improvements add up fast."

        state["overall_score"] = overall_score
        state["weakest_area"] = weakest
        state["strongest_area"] = strongest
        state["overall_feedback"] = overall_feedback
        state["session_timestamp"] = datetime.utcnow().isoformat()
        state["score_breakdown"] = score_map

        return state
