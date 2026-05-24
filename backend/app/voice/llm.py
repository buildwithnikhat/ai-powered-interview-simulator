import httpx
from app.config import settings


async def get_llm_response(
    user_message: str,
    system_prompt: str = None,
    conversation_history: list = None,
) -> str:

    if system_prompt is None:
        system_prompt = """You are Aria, a friendly AI communication coach and speaking partner. 

Your personality:
- Warm, encouraging, and natural — like a supportive friend
- You speak conversationally, not like a formal teacher
- You listen carefully and respond to what the person actually said
- You mix coaching with genuine conversation

Your approach:
- First acknowledge what they said naturally
- Then give ONE small, specific improvement tip if needed
- Keep responses short — 2 to 3 sentences maximum
- Never be robotic or use bullet points
- Sound human and warm

Examples of good responses:
- "That was great! I noticed you paused nicely. Try making eye contact next time too."
- "Nice one! One thing — swap 'basically' with a pause instead. It sounds more confident."
- "Good energy! Your sentence structure was clear. Keep that up!"

Remember: you are having a real conversation, not giving a lecture."""

    messages = []
    messages.append({"role": "system", "content": system_prompt})

    if conversation_history:
        messages.extend(conversation_history[-10:])

    messages.append({"role": "user", "content": user_message})

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.OLLAMA_BASE_URL}/api/chat",
            json={
                "model": settings.OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.85,
                    "num_predict": 150,
                }
            }
        )
        response.raise_for_status()
        data = response.json()

    return data["message"]["content"].strip()


async def check_ollama_connection() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            return any(settings.OLLAMA_MODEL in m for m in models)
    except Exception:
        return False


async def get_coaching_response(transcript: str, analysis: dict) -> str:

    filler_count = analysis.get("filler_count", 0)
    word_count = analysis.get("word_count", 0)
    confidence_score = analysis.get("confidence_score", 0)

    if word_count < 3:
        prompt = f"""The person said: "{transcript}"

That was very short. Encourage them warmly to say more and keep the conversation going naturally. Ask them a simple follow-up question about what they want to practice today."""

    elif filler_count > 3:
        prompt = f"""The person said: "{transcript}"

They used {filler_count} filler words. Respond naturally to what they said first, then gently mention the filler words with one specific tip. Keep it encouraging and brief."""

    elif confidence_score < 50:
        prompt = f"""The person said: "{transcript}"

They sound a bit nervous (confidence score {confidence_score}/100). Respond warmly to their message and give them one confidence tip. Be very encouraging."""

    else:
        prompt = f"""The person said: "{transcript}"

Respond naturally as their conversation partner. Acknowledge what they said, keep the conversation flowing, and give one small improvement tip if relevant. Sound like a friendly coach, not a teacher."""

    return await get_llm_response(prompt)
