import random
from app.agents.base import BaseAgent
from app.agents.interview_data import (
    HR_QUESTIONS, TECHNICAL_QUESTIONS, AI_ENGINEERING_QUESTIONS,
    DEVOPS_QUESTIONS, FREELANCE_QUESTIONS, PROJECT_PROMPTS,
    STORYTELLING_PROMPTS, CONFIDENCE_EXERCISES, STAR_FRAMEWORK
)


INTERVIEW_TYPES = {
    "hr":          {"name": "HR Interview",           "questions": HR_QUESTIONS},
    "technical":   {"name": "Technical Interview",    "questions": TECHNICAL_QUESTIONS},
    "ai":          {"name": "AI Engineering",         "questions": AI_ENGINEERING_QUESTIONS},
    "devops":      {"name": "DevOps Interview",       "questions": DEVOPS_QUESTIONS},
    "freelance":   {"name": "Freelance Client Call",  "questions": FREELANCE_QUESTIONS},
    "storytelling":{"name": "Storytelling Practice",  "questions": STORYTELLING_PROMPTS},
    "confidence":  {"name": "Confidence Building",    "questions": CONFIDENCE_EXERCISES},
    "fastapi":     {"name": "FastAPI Project",        "questions": PROJECT_PROMPTS["fastapi"]},
    "ai_agent":    {"name": "AI Agent Project",       "questions": PROJECT_PROMPTS["ai_agent"]},
    "rag":         {"name": "RAG System Project",     "questions": PROJECT_PROMPTS["rag"]},
    "saas":        {"name": "SaaS Project",           "questions": PROJECT_PROMPTS["saas"]},
}


class InterviewAgent(BaseAgent):
    """
    Full interview simulation agent.
    Asks questions, evaluates answers, gives follow-ups.
    """

    def __init__(self):
        super().__init__(
            name="Interview Coach",
            description="Full mock interview with evaluation and follow-ups"
        )
        self._sessions = {}  # Track active interview sessions

    def get_interview_types(self) -> list:
        return [
            {"key": k, "name": v["name"], "count": len(v["questions"])}
            for k, v in INTERVIEW_TYPES.items()
        ]

    def start_interview(self, session_id: str, interview_type: str = "hr") -> dict:
        """Start a new interview session and return the first question."""
        interview = INTERVIEW_TYPES.get(interview_type, INTERVIEW_TYPES["hr"])
        questions = random.sample(
            interview["questions"],
            min(6, len(interview["questions"]))
        )

        self._sessions[session_id] = {
            "type":          interview_type,
            "name":          interview["name"],
            "questions":     questions,
            "current_index": 0,
            "answers":       [],
            "scores":        [],
        }

        return {
            "interview_type": interview_type,
            "interview_name": interview["name"],
            "total_questions": len(questions),
            "current_question": questions[0],
            "question_number": 1,
            "star_tip": STAR_FRAMEWORK if interview_type in ["hr", "freelance"] else "",
        }

    def get_session(self, session_id: str) -> dict:
        return self._sessions.get(session_id, {})

    def advance_question(self, session_id: str) -> dict:
        """Move to the next question."""
        session = self._sessions.get(session_id)
        if not session:
            return {"done": True, "message": "Session not found"}

        session["current_index"] += 1
        idx = session["current_index"]

        if idx >= len(session["questions"]):
            return {"done": True, "final_score": self._calculate_final_score(session)}

        return {
            "done": False,
            "current_question": session["questions"][idx],
            "question_number": idx + 1,
            "total_questions": len(session["questions"]),
        }

    def _calculate_final_score(self, session: dict) -> dict:
        scores = session.get("scores", [])
        if not scores:
            return {"overall": 0, "message": "No answers evaluated yet"}

        avg = sum(scores) / len(scores)
        if avg >= 80:
            grade = "Excellent"
            advice = "You are interview-ready! Keep practicing to maintain this level."
        elif avg >= 65:
            grade = "Good"
            advice = "Solid performance. Work on giving more specific examples."
        elif avg >= 50:
            grade = "Needs Practice"
            advice = "Keep practicing. Focus on the STAR method for behavioral questions."
        else:
            grade = "Keep Practicing"
            advice = "Practice daily. Record yourself and listen back to improve."

        return {
            "overall": round(avg),
            "grade": grade,
            "advice": advice,
            "questions_answered": len(scores),
        }

    async def evaluate_answer(
        self,
        question: str,
        answer: str,
        interview_type: str,
        session_id: str = None,
    ) -> dict:
        """Evaluate a single interview answer."""

        if not answer or len(answer.split()) < 3:
            return {
                "score": 30,
                "feedback": "Your answer was too short. Try to give a complete response with specific details.",
                "improvement": "Use the STAR method: Situation, Task, Action, Result.",
                "follow_up": "Can you elaborate more on that?",
                "encouragement": "Take your time and give a fuller answer.",
            }

        system_prompt = """You are an expert interview coach evaluating a candidate's answer.
Be encouraging but honest. Respond ONLY in this exact format — no extra text:

SCORE: [0-100]
FEEDBACK: [2 sentences evaluating the answer — be specific]
IMPROVEMENT: [one specific actionable suggestion]
FOLLOW_UP: [one natural follow-up question]
ENCOURAGEMENT: [one short encouraging sentence]"""

        prompt = f"""Interview type: {interview_type}
Question: {question}
Candidate's answer: {answer}

Evaluate this answer."""

        try:
            response = await self.get_response(prompt, system_prompt)
            parsed = {}
            for line in response.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    parsed[key.strip()] = value.strip()

            score = int(parsed.get('SCORE', '65').replace('%', '').strip())
            score = max(0, min(100, score))

            result = {
                "score":         score,
                "feedback":      parsed.get('FEEDBACK', 'Good attempt! Keep practicing.'),
                "improvement":   parsed.get('IMPROVEMENT', 'Try using the STAR method.'),
                "follow_up":     parsed.get('FOLLOW_UP', 'Can you give a specific example?'),
                "encouragement": parsed.get('ENCOURAGEMENT', 'You are improving with every answer!'),
            }

            # Store score in session
            if session_id and session_id in self._sessions:
                self._sessions[session_id]["scores"].append(score)
                self._sessions[session_id]["answers"].append({
                    "question": question,
                    "answer": answer,
                    "score": score,
                })

            return result

        except Exception as e:
            print(f"Interview evaluation error: {e}")
            return {
                "score": 65,
                "feedback": "Good effort! Your answer showed understanding of the topic.",
                "improvement": "Add more specific examples to strengthen your answer.",
                "follow_up": "Can you tell me more about that experience?",
                "encouragement": "Every practice session makes you better!",
            }

    async def analyze(self, state: dict) -> dict:
        """Standard agent analyze method."""
        transcript     = state.get("transcript", "")
        question       = state.get("current_interview_question", "")
        interview_type = state.get("interview_type", "hr")
        session_id     = state.get("session_id", "")

        if not transcript or not question:
            state["interview_feedback"]    = ""
            state["interview_score"]       = 0
            state["interview_follow_up"]   = ""
            state["interview_improvement"] = ""
            return state

        result = await self.evaluate_answer(
            question=question,
            answer=transcript,
            interview_type=interview_type,
            session_id=session_id,
        )

        state["interview_score"]       = result["score"]
        state["interview_feedback"]    = result["feedback"]
        state["interview_improvement"] = result["improvement"]
        state["interview_follow_up"]   = result["follow_up"]
        state["interview_encouragement"] = result["encouragement"]

        return state
