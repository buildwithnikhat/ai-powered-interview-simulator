from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json

from app.voice.stt import transcribe_audio_bytes
from app.voice.tts import text_to_speech_bytes_async
from app.voice.llm import check_ollama_connection
from app.orchestrator.graph import orchestrator

router = APIRouter(prefix="/voice", tags=["voice"])


@router.get("/status")
async def voice_status():
    ollama_ok = await check_ollama_connection()
    return {
        "whisper":   "ready",
        "tts":       "ready",
        "ollama":    "connected" if ollama_ok else "not connected",
        "agents":    "10 agents ready",
        "websocket": "ready",
    }


@router.get("/personas")
async def get_personas():
    return orchestrator.conversation_agent.get_available_personas()


async def safe_send_json(websocket: WebSocket, data: dict) -> bool:
    """Send JSON safely — returns False if connection is closed."""
    try:
        await websocket.send_json(data)
        return True
    except Exception:
        return False


async def safe_send_bytes(websocket: WebSocket, data: bytes) -> bool:
    """Send bytes safely — returns False if connection is closed."""
    try:
        await websocket.send_bytes(data)
        return True
    except Exception:
        return False


@router.websocket("/ws")
async def voice_websocket(websocket: WebSocket):
    await websocket.accept()
    print("Voice WebSocket connected")

    conversation_history = []

    try:
        while True:
            message = await websocket.receive()

            if "text" in message:
                data = json.loads(message["text"])
                msg_type = data.get("type")

                if msg_type == "ping":
                    await safe_send_json(websocket, {"type": "pong"})

                elif msg_type == "start_session":
                    await safe_send_json(websocket, {
                        "type": "session_started",
                        "message": "AI-COS ready — 10 agents + memory online",
                    })

                elif msg_type == "set_persona":
                    persona = data.get("persona", "coach")
                    orchestrator.conversation_agent.set_persona(persona)
                    await safe_send_json(websocket, {
                        "type": "persona_set",
                        "persona": persona
                    })

                elif msg_type == "text_message":
                    user_text = data.get("text", "").strip()
                    if user_text:
                        await process_and_respond(
                            websocket, user_text, conversation_history
                        )

            elif "bytes" in message:
                audio_bytes = message["bytes"]
                if len(audio_bytes) < 1000:
                    continue

                await safe_send_json(websocket, {
                    "type": "status",
                    "message": "Transcribing your speech..."
                })

                loop = asyncio.get_event_loop()
                try:
                    transcription = await loop.run_in_executor(
                        None, transcribe_audio_bytes, audio_bytes
                    )
                    transcript_text = transcription["text"].strip()
                    words = transcription.get("words", [])
                except Exception as e:
                    await safe_send_json(websocket, {
                        "type": "error",
                        "message": f"Transcription failed: {str(e)}"
                    })
                    continue

                if not transcript_text:
                    await safe_send_json(websocket, {
                        "type": "error",
                        "message": "Could not hear anything clearly. Please speak louder."
                    })
                    continue

                await process_and_respond(
                    websocket, transcript_text,
                    conversation_history, words=words
                )

    except WebSocketDisconnect:
        print("Voice WebSocket disconnected normally")
    except Exception as e:
        print(f"WebSocket error: {e}")


async def process_and_respond(
    websocket: WebSocket,
    transcript: str,
    conversation_history: list,
    words: list = None,
    persona: str = "coach",
):
    try:
        # Step 1 — Send transcript immediately
        ok = await safe_send_json(websocket, {
            "type": "transcript",
            "text": transcript,
        })
        if not ok:
            return

        # Step 2 — Build state
        import uuid
        state = {
            "transcript":           transcript,
            "words":                words or [],
            "duration_seconds":     max(len(transcript.split()) / 2.5, 1),
            "persona":              persona,
            "conversation_history": conversation_history.copy(),
            "session_type":         "conversation",
            "user_id":              "default_user",
            "session_id":           str(uuid.uuid4()),
        }

        # Step 3 — Run all agents
        ok = await safe_send_json(websocket, {
            "type": "status",
            "message": "Analyzing with 10 agents..."
        })
        if not ok:
            return

        state = await orchestrator.run_conversation_session(state)

        # Step 4 — Send scores
        ok = await safe_send_json(websocket, {
            "type": "analysis",
            "data": {
                "confidence_score":    state.get("confidence_score", 0),
                "fluency_score":       state.get("fluency_score", 0),
                "grammar_score":       state.get("grammar_score", 0),
                "pronunciation_score": state.get("pronunciation_score", 0),
                "vocab_score":         state.get("vocab_score", 0),
                "overall_score":       state.get("overall_score", 0),
                "filler_count":        state.get("filler_count", 0),
                "word_count":          state.get("word_count", 0),
                "weakest_area":        state.get("weakest_area", ""),
                "strongest_area":      state.get("strongest_area", ""),
            }
        })
        if not ok:
            return

        # Step 5 — Send agent tips
        await safe_send_json(websocket, {
            "type": "agent_feedback",
            "data": {
                "fluency_tip":      state.get("fluency_tip", ""),
                "grammar_tip":      state.get("grammar_tip", ""),
                "confidence_tip":   state.get("confidence_tip", ""),
                "vocab_tip":        state.get("vocab_tip", ""),
                "overall_feedback": state.get("overall_feedback", ""),
                "daily_plan":       state.get("daily_plan", {}),
                "word_of_day":      state.get("word_of_day", {}),
                "memory_context":   state.get("memory_context", ""),
                "session_count":    state.get("session_count", 0),
            }
        })

        # Step 6 — Generate coaching response
        coaching_text = orchestrator.generate_coaching_summary(state)

        ok = await safe_send_json(websocket, {
            "type": "coaching",
            "text": coaching_text,
        })
        if not ok:
            return

        # Step 7 — Update conversation history
        conversation_history.append({"role": "user", "content": transcript})
        conversation_history.append({"role": "assistant", "content": coaching_text})
        if len(conversation_history) > 20:
            conversation_history[:] = conversation_history[-20:]

        # Step 8 — TTS with timeout protection
        ok = await safe_send_json(websocket, {
            "type": "status",
            "message": "Generating voice response..."
        })
        if not ok:
            return

        try:
            # 30 second timeout for TTS
            audio_bytes = await asyncio.wait_for(
                text_to_speech_bytes_async(coaching_text),
                timeout=30.0
            )
            await safe_send_json(websocket, {"type": "audio_ready"})
            await safe_send_bytes(websocket, audio_bytes)

        except asyncio.TimeoutError:
            print("TTS timeout — skipping audio")
            await safe_send_json(websocket, {
                "type": "status",
                "message": "✅ Done (audio took too long — text response shown above)"
            })
        except Exception as e:
            print(f"TTS error: {e}")
            await safe_send_json(websocket, {
                "type": "status",
                "message": "✅ Response ready (text shown above)"
            })

    except Exception as e:
        print(f"Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        await safe_send_json(websocket, {
            "type": "error",
            "message": f"Error: {str(e)}"
        })
