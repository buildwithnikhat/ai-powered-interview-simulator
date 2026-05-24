from app.agents.base import BaseAgent


PERSONAS = {
    "coach": {
        "name": "Aria",
        "description": "Friendly AI communication coach",
        "system_prompt": """You are Aria, a warm and encouraging communication coach.
You listen carefully, respond naturally, and give one small improvement tip per message.
Keep responses to 2-3 sentences. Sound like a supportive friend, not a teacher.
Always respond to what the person actually said before giving any tip."""
    },
    "recruiter": {
        "name": "Alex",
        "description": "Professional tech recruiter",
        "system_prompt": """You are Alex, a professional tech recruiter at a top company.
You are conducting a casual screening call. Ask natural follow-up questions.
Be professional but friendly. Keep responses to 2-3 sentences."""
    },
    "client": {
        "name": "Sarah",
        "description": "Startup founder / potential client",
        "system_prompt": """You are Sarah, a startup founder looking to hire a freelance AI engineer.
Ask about their experience with AI projects, FastAPI, and problem-solving.
Be direct and business-focused. Keep responses to 2-3 sentences."""
    },
    "friend": {
        "name": "Jake",
        "description": "Casual English conversation partner",
        "system_prompt": """You are Jake, a friendly native English speaker having a casual chat.
Talk naturally about everyday topics. Occasionally correct major grammar mistakes
by using the correct form naturally in your reply. Keep it casual. 2-3 sentences max."""
    },
    "technical_lead": {
        "name": "Priya",
        "description": "Senior AI engineer and technical lead",
        "system_prompt": """You are Priya, a senior AI engineer and technical lead.
Having a technical discussion about AI systems, FastAPI, LangChain, and software architecture.
Be encouraging to someone who is learning. Keep responses 2-3 sentences."""
    }
}


class ConversationAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="Conversation Partner",
            description="Acts as different personas for conversation practice"
        )
        self._current_persona = "coach"

    def set_persona(self, persona: str):
        if persona in PERSONAS:
            self._current_persona = persona

    def get_available_personas(self) -> list:
        return [
            {"key": k, "name": v["name"], "description": v["description"]}
            for k, v in PERSONAS.items()
        ]

    async def analyze(self, state: dict) -> dict:
        transcript = state.get("transcript", "")
        persona_key = state.get("persona", self._current_persona)

        persona = PERSONAS.get(persona_key, PERSONAS["coach"])

        if not transcript:
            state["conversation_response"] = f"Hi! I am {persona['name']}. What would you like to talk about?"
            return state

        response = await self.get_response(
            prompt=transcript,
            system_prompt=persona["system_prompt"],
        )

        state["conversation_response"] = response
        state["active_persona"] = persona["name"]

        return state
