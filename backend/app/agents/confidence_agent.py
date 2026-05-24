from app.agents.base import BaseAgent
from app.voice.stt import count_filler_words


class ConfidenceAgent(BaseAgent):
    """
    Measures how confident the speaker sounds.
    Detects filler words, hesitation, and speaking patterns.
    """

    FILLER_WORDS = [
        "umm", "um", "uh", "uhh", "like", "basically",
        "you know", "i mean", "sort of", "kind of",
        "actually", "literally", "right", "so yeah"
    ]

    def __init__(self):
        super().__init__(
            name="Confidence Coach",
            description="Measures confidence through filler words and speech patterns"
        )

    async def analyze(self, state: dict) -> dict:
        transcript = state.get("transcript", "").lower()
        word_count = state.get("word_count", len(transcript.split()))

        # Count filler words
        filler_data = count_filler_words(transcript)
        filler_count = filler_data["total_filler_count"]
        filler_breakdown = filler_data["filler_breakdown"]

        # Calculate confidence score
        if word_count == 0:
            confidence_score = 0
        else:
            filler_ratio = filler_count / max(word_count, 1)
            if filler_ratio > 0.3:
                confidence_score = 30
            elif filler_ratio > 0.2:
                confidence_score = 50
            elif filler_ratio > 0.1:
                confidence_score = 70
            elif filler_ratio > 0.05:
                confidence_score = 85
            else:
                confidence_score = 100

        # Generate tip based on fillers found
        if filler_count == 0:
            confidence_tip = "Excellent! No filler words — you sound very confident."
            confidence_level = "high"
        elif filler_count <= 2:
            most_common = max(filler_breakdown, key=filler_breakdown.get) if filler_breakdown else "um"
            confidence_tip = f"Good job! Just watch out for '{most_common}' — replace it with a brief pause."
            confidence_level = "good"
        elif filler_count <= 5:
            confidence_tip = f"You used {filler_count} filler words. Practice pausing instead of saying 'um' or 'uh'."
            confidence_level = "moderate"
        else:
            confidence_tip = f"You used {filler_count} filler words. Slow down and breathe — pauses sound more confident than fillers."
            confidence_level = "needs work"

        state["confidence_score"] = confidence_score
        state["confidence_level"] = confidence_level
        state["filler_count"] = filler_count
        state["filler_breakdown"] = filler_breakdown
        state["confidence_tip"] = confidence_tip

        return state
