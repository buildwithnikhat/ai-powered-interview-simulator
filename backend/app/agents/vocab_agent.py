from app.agents.base import BaseAgent


DAILY_VOCAB = [
    {"word": "articulate", "meaning": "able to express ideas clearly", "example": "She was very articulate during the presentation."},
    {"word": "concise", "meaning": "brief and clear", "example": "Please give a concise answer."},
    {"word": "elaborate", "meaning": "to explain in more detail", "example": "Can you elaborate on that point?"},
    {"word": "proficient", "meaning": "skilled and experienced", "example": "He is proficient in Python and FastAPI."},
    {"word": "collaborate", "meaning": "to work together", "example": "We need to collaborate on this project."},
    {"word": "implement", "meaning": "to put into action", "example": "Let me implement that feature today."},
    {"word": "leverage", "meaning": "to use something to maximum advantage", "example": "We can leverage AI to automate this."},
    {"word": "scalable", "meaning": "able to handle growth", "example": "We need a scalable architecture."},
    {"word": "iterate", "meaning": "to repeat a process to improve it", "example": "Let us iterate on this design."},
    {"word": "optimize", "meaning": "to make as effective as possible", "example": "We need to optimize the query speed."},
]


class VocabAgent(BaseAgent):
    """
    Tracks vocabulary usage and suggests words to improve communication.
    Detects weak vocabulary and suggests professional alternatives.
    """

    WEAK_WORDS = {
        "good": "excellent / outstanding / proficient",
        "bad": "challenging / problematic / suboptimal",
        "big": "significant / substantial / large-scale",
        "small": "minimal / compact / lightweight",
        "use": "utilize / implement / leverage",
        "make": "develop / create / build / implement",
        "get": "obtain / acquire / retrieve",
        "show": "demonstrate / present / illustrate",
        "very": "extremely / highly / remarkably",
        "a lot": "significantly / considerably / substantially",
        "thing": "component / element / feature / aspect",
        "stuff": "components / elements / materials",
        "nice": "excellent / impressive / well-designed",
    }

    def __init__(self):
        super().__init__(
            name="Vocabulary Coach",
            description="Improves vocabulary and suggests professional alternatives"
        )
        self._word_index = 0

    def get_word_of_day(self) -> dict:
        import datetime
        day_index = datetime.datetime.now().timetuple().tm_yday % len(DAILY_VOCAB)
        return DAILY_VOCAB[day_index]

    async def analyze(self, state: dict) -> dict:
        transcript = state.get("transcript", "").lower()
        words_used = transcript.split()

        # Find weak words used
        weak_found = {}
        for weak_word, alternative in self.WEAK_WORDS.items():
            if weak_word in transcript:
                weak_found[weak_word] = alternative

        # Calculate vocabulary score
        unique_words = len(set(words_used))
        total_words = len(words_used)
        variety_ratio = unique_words / max(total_words, 1)

        if weak_found:
            vocab_score = max(50, 100 - (len(weak_found) * 15))
        elif variety_ratio > 0.8:
            vocab_score = 95
        elif variety_ratio > 0.6:
            vocab_score = 80
        else:
            vocab_score = 65

        # Generate tip
        if weak_found:
            weak_word = list(weak_found.keys())[0]
            alternative = weak_found[weak_word]
            vocab_tip = f"Instead of '{weak_word}', try: {alternative}"
        else:
            word_of_day = self.get_word_of_day()
            vocab_tip = f"Word of the day: '{word_of_day['word']}' — {word_of_day['meaning']}"

        state["vocab_score"] = vocab_score
        state["weak_words_found"] = weak_found
        state["vocab_tip"] = vocab_tip
        state["word_of_day"] = self.get_word_of_day()

        return state
