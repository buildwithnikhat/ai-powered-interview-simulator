from app.agents.base import BaseAgent


class GrammarAgent(BaseAgent):
    """
    Analyzes grammar mistakes in spoken text.
    Corrects mistakes and explains them simply.
    """

    def __init__(self):
        super().__init__(
            name="Grammar Coach",
            description="Detects and corrects grammar mistakes"
        )

    async def analyze(self, state: dict) -> dict:
        transcript = state.get("transcript", "")

        if not transcript or len(transcript.split()) < 3:
            state["grammar_score"] = 100
            state["grammar_issues"] = []
            state["grammar_correction"] = ""
            state["grammar_tip"] = ""
            return state

        system_prompt = """You are a grammar analysis expert. 
Analyze the spoken text for grammar mistakes.
Respond ONLY in this exact format with no extra text:

SCORE: [0-100]
ISSUES: [comma separated list of issues, or 'none']
CORRECTION: [corrected version of the sentence]
TIP: [one specific grammar tip in simple words]

Be lenient with spoken English — focus on serious mistakes only."""

        prompt = f'Analyze this spoken text for grammar: "{transcript}"'

        try:
            response = await self.get_response(prompt, system_prompt)

            # Parse the structured response
            lines = response.strip().split('\n')
            parsed = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    parsed[key.strip()] = value.strip()

            score = int(parsed.get('SCORE', '85').replace('%', ''))
            issues_raw = parsed.get('ISSUES', 'none')
            issues = [] if issues_raw.lower() == 'none' else [i.strip() for i in issues_raw.split(',')]
            correction = parsed.get('CORRECTION', transcript)
            tip = parsed.get('TIP', 'Keep practicing — your grammar is improving!')

        except Exception:
            score = 80
            issues = []
            correction = transcript
            tip = "Keep practicing your grammar!"

        state["grammar_score"] = score
        state["grammar_issues"] = issues
        state["grammar_correction"] = correction
        state["grammar_tip"] = tip

        return state
