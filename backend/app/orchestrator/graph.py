import asyncio
import uuid
from app.agents.fluency_agent import FluencyAgent
from app.agents.grammar_agent import GrammarAgent
from app.agents.confidence_agent import ConfidenceAgent
from app.agents.pronunciation_agent import PronunciationAgent
from app.agents.conversation_agent import ConversationAgent
from app.agents.vocab_agent import VocabAgent
from app.agents.analytics_agent import AnalyticsAgent
from app.agents.memory_agent import MemoryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.interview_agent import InterviewAgent


class AgentOrchestrator:

    def __init__(self):
        self.fluency_agent       = FluencyAgent()
        self.grammar_agent       = GrammarAgent()
        self.confidence_agent    = ConfidenceAgent()
        self.pronunciation_agent = PronunciationAgent()
        self.conversation_agent  = ConversationAgent()
        self.vocab_agent         = VocabAgent()
        self.analytics_agent     = AnalyticsAgent()
        self.memory_agent        = MemoryAgent()
        self.planner_agent       = PlannerAgent()
        self.interview_agent     = InterviewAgent()
        print("✅ All 10 agents initialized")

    async def run_conversation_session(self, state: dict) -> dict:
        # Ensure session_id exists
        if "session_id" not in state:
            state["session_id"] = str(uuid.uuid4())
        if "user_id" not in state:
            state["user_id"] = "default_user"

        # Step 1 — Run fast agents in parallel
        results = await asyncio.gather(
            self.fluency_agent.analyze(state.copy()),
            self.confidence_agent.analyze(state.copy()),
            self.vocab_agent.analyze(state.copy()),
            self.pronunciation_agent.analyze(state.copy()),
            return_exceptions=True,
        )

        # Merge parallel results
        for result in results:
            if isinstance(result, dict):
                state.update(result)
            elif isinstance(result, Exception):
                print(f"Agent error: {result}")

        # Step 2 — Grammar agent
        try:
            state = await self.grammar_agent.analyze(state)
        except Exception as e:
            print(f"Grammar agent error: {e}")

        # Step 3 — Conversation agent
        try:
            state = await self.conversation_agent.analyze(state)
        except Exception as e:
            print(f"Conversation agent error: {e}")

        # Step 4 — Analytics
        try:
            state = await self.analytics_agent.analyze(state)
        except Exception as e:
            print(f"Analytics agent error: {e}")

        # Step 5 — Memory (stores to ChromaDB)
        try:
            state = await self.memory_agent.analyze(state)
        except Exception as e:
            print(f"Memory agent error: {e}")

        # Step 6 — Daily planner
        try:
            state = await self.planner_agent.analyze(state)
        except Exception as e:
            print(f"Planner agent error: {e}")

        return state

    async def run_interview_session(self, state: dict) -> dict:
        if "session_id" not in state:
            state["session_id"] = str(uuid.uuid4())

        state = await self.confidence_agent.analyze(state)
        state = await self.grammar_agent.analyze(state)
        state = await self.interview_agent.analyze(state)
        state = await self.analytics_agent.analyze(state)
        state = await self.memory_agent.analyze(state)
        return state

    def generate_coaching_summary(self, state: dict) -> str:
        conversation_response = state.get("conversation_response", "")
        memory_context        = state.get("memory_context", "")
        confidence_tip        = state.get("confidence_tip", "")
        grammar_tip           = state.get("grammar_tip", "")
        vocab_tip             = state.get("vocab_tip", "")
        fluency_tip           = state.get("fluency_tip", "")
        overall_feedback      = state.get("overall_feedback", "")

        # Use conversation response as the primary message
        response = conversation_response or overall_feedback

        # Add one coaching tip
        tips = [t for t in [
            confidence_tip, grammar_tip, vocab_tip, fluency_tip
        ] if t and t not in response]

        if tips:
            import random
            tip = random.choice(tips[:2])
            response = f"{response} {tip}"

        return response.strip()


orchestrator = AgentOrchestrator()
