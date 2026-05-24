from app.agents.base import BaseAgent


class PronunciationAgent(BaseAgent):
    """
    Analyzes pronunciation using Whisper word-level confidence scores.
    Low confidence scores indicate mispronounced or unclear words.
    """

    def __init__(self):
        super().__init__(
            name="Pronunciation Analyzer",
            description="Detects mispronounced words using Whisper confidence scores"
        )

    async def analyze(self, state: dict) -> dict:
        words = state.get("words", [])  # Word-level data from Whisper
        transcript = state.get("transcript", "")

        if not words:
            state["pronunciation_score"] = 85
            state["unclear_words"] = []
            state["pronunciation_tip"] = "Speak clearly and the system will analyze your pronunciation."
            return state

        # Find words with low confidence (likely mispronounced)
        unclear_words = []
        total_confidence = 0

        for word_data in words:
            prob = word_data.get("probability", 1.0)
            word = word_data.get("word", "").strip()
            total_confidence += prob

            if prob < 0.7 and len(word) > 2:
                unclear_words.append({
                    "word": word,
                    "confidence": round(prob * 100)
                })

        # Calculate pronunciation score
        if words:
            avg_confidence = total_confidence / len(words)
            pronunciation_score = round(avg_confidence * 100)
        else:
            pronunciation_score = 85

        # Generate tip
        if not unclear_words:
            tip = "Great pronunciation! Every word was clear and well-articulated."
        elif len(unclear_words) == 1:
            word = unclear_words[0]["word"]
            tip = f"Almost perfect! The word '{word}' was slightly unclear — try emphasizing each syllable."
        else:
            words_list = ", ".join([w["word"] for w in unclear_words[:3]])
            tip = f"Focus on pronouncing these words more clearly: {words_list}. Slow down on difficult words."

        state["pronunciation_score"] = pronunciation_score
        state["unclear_words"] = unclear_words
        state["pronunciation_tip"] = tip

        return state
