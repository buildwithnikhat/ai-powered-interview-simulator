from abc import ABC, abstractmethod
from app.voice.llm import get_llm_response


class BaseAgent(ABC):

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def analyze(self, state: dict) -> dict:
        pass

    async def get_response(self, prompt: str, system_prompt: str = None) -> str:
        """Helper to call LLM — available to all agents."""
        return await get_llm_response(
            user_message=prompt,
            system_prompt=system_prompt
        )

    def __repr__(self):
        return f"<Agent: {self.name}>"
