from app.agents.base import BaseAgent


class FluencyAgent(BaseAgent):
    """
    Analyzes how fluently the user speaks.
    Measures sentence flow, speaking speed, and hesitation patterns.
    """

    def __init__(self):
        super().__init__(
            name="Fluency Coach",
            description="Analyzes fluency, flow, and speaking rhythm"
        )

    async def analyze(self, state: dict) -> dict:
        transcript = state.get("transcript", "")
        words = transcript.split()
        word_count = len(words)
        duration = state.get("duration_seconds", 10)

        # Calculate speaking speed (words per minute)
        wpm = round((word_count / max(duration, 1)) * 60)

        # Score fluency based on word count and speed
        if word_count < 5:
            fluency_score = 20
            fluency_level = "very short"
        elif word_count < 15:
            fluency_score = 50
            fluency_level = "short"
        elif wpm < 80:
            fluency_score = 60
            fluency_level = "slow"
        elif wpm > 180:
            fluency_score = 65
            fluency_level = "too fast"
        else:
            fluency_score = min(100, 70 + (word_count // 5))
            fluency_level = "good"

        # Generate coaching tip
        if word_count < 5:
            tip = "Try to speak in complete sentences — aim for at least 10 words."
        elif wpm < 80:
            tip = "Good pace! Try to speak a little faster for more natural flow."
        elif wpm > 180:
            tip = "Slow down slightly — you are speaking very fast. Pausing helps clarity."
        else:
            tip = "Good fluency! Keep practicing longer sentences to build stamina."

        state["fluency_score"] = fluency_score
        state["fluency_level"] = fluency_level
        state["fluency_wpm"] = wpm
        state["fluency_tip"] = tip
        state["word_count"] = word_count

        return state
