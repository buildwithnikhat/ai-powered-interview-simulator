from app.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    """
    Creates a personalized daily learning plan.
    Adapts based on weak areas identified by other agents.
    """

    EXERCISES = {
        "fluency": [
            "Read one paragraph aloud every morning",
            "Practice shadow speaking — repeat after a podcast",
            "Tell a story about your day in 60 seconds",
            "Describe your project in 30 seconds without stopping",
        ],
        "grammar": [
            "Write 5 sentences about your work and check grammar",
            "Practice past tense by describing yesterday",
            "Use 'however', 'therefore', 'moreover' in 3 sentences",
            "Rewrite 3 informal sentences in professional English",
        ],
        "confidence": [
            "Record yourself speaking for 60 seconds",
            "Practice saying your introduction 5 times without fillers",
            "Do 5 minutes of power posing before speaking",
            "Speak to the AI coach for 10 minutes without stopping",
        ],
        "pronunciation": [
            "Practice tongue twisters for 5 minutes",
            "Repeat 5 technical words slowly: API, asynchronous, algorithm",
            "Listen and repeat a 2-minute YouTube video",
            "Record and compare your pronunciation with a native speaker",
        ],
        "vocabulary": [
            "Learn 3 new professional words today",
            "Use 'leverage', 'implement', 'optimize' in sentences",
            "Replace 5 weak words in your speech with stronger alternatives",
            "Read a tech article and note 5 new words",
        ]
    }

    def __init__(self):
        super().__init__(
            name="Learning Planner",
            description="Creates personalized daily learning plans"
        )

    async def analyze(self, state: dict) -> dict:
        weakest_area = state.get("weakest_area", "fluency")
        overall_score = state.get("overall_score", 0)
        session_count = state.get("session_count", 1)

        import random

        # Get exercises for weak area
        primary_exercises = self.EXERCISES.get(weakest_area, self.EXERCISES["fluency"])
        primary_task = random.choice(primary_exercises)

        # Get a secondary exercise from another area
        other_areas = [a for a in self.EXERCISES.keys() if a != weakest_area]
        secondary_area = random.choice(other_areas)
        secondary_task = random.choice(self.EXERCISES[secondary_area])

        # Create daily plan
        daily_plan = {
            "focus_area": weakest_area,
            "primary_task": primary_task,
            "secondary_task": secondary_task,
            "daily_goal": f"Practice {weakest_area} for 15 minutes",
            "session_count": session_count,
            "motivation": self._get_motivation(overall_score, session_count),
        }

        state["daily_plan"] = daily_plan

        return state

    def _get_motivation(self, score: int, sessions: int) -> str:
        if sessions == 1:
            return "Great start! Consistency is the key to improvement."
        elif score >= 80:
            return "You are doing amazing! Keep up this momentum."
        elif score >= 60:
            return "Good progress! Every session makes you better."
        else:
            return "Keep going! The most successful people practice every single day."
