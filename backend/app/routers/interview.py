from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
import uuid

from app.orchestrator.graph import orchestrator
from app.voice.stt import transcribe_audio_bytes
from app.voice.tts import text_to_speech_bytes_async

router = APIRouter(prefix="/interview", tags=["interview"])


async def safe_send(ws: WebSocket, data: dict) -> bool:
    try:
        await ws.send_json(data)
        return True
    except Exception:
        return False


async def safe_send_bytes(ws: WebSocket, data: bytes) -> bool:
    try:
        await ws.send_bytes(data)
        return True
    except Exception:
        return False


@router.get("/types")
async def get_interview_types():
    """Get all available interview types."""
    return {
        "types": orchestrator.interview_agent.get_interview_types()
    }


@router.websocket("/ws")
async def interview_websocket(websocket: WebSocket):
    """
    Dedicated WebSocket for interview sessions.
    Manages question flow, answer evaluation, and scoring.
    """
    await websocket.accept()
    print("Interview WebSocket connected")

    interview_session_id = str(uuid.uuid4())
    current_question     = ""
    interview_type       = "hr"

    try:
        while True:
            message = await websocket.receive()

            if "text" in message:
                data = json.loads(message["text"])
                msg_type = data.get("type")

                # Start a new interview
                if msg_type == "start_interview":
                    interview_type = data.get("interview_type", "hr")
                    result = orchestrator.interview_agent.start_interview(
                        session_id=interview_session_id,
                        interview_type=interview_type,
                    )
                    current_question = result["current_question"]

                    await safe_send(websocket, {
                        "type":             "interview_started",
                        "interview_name":   result["interview_name"],
                        "total_questions":  result["total_questions"],
                        "question":         current_question,
                        "question_number":  1,
                        "star_tip":         result.get("star_tip", ""),
                    })

                    # Speak the question
                    audio = await text_to_speech_bytes_async(
                        f"Question 1. {current_question}"
                    )
                    await safe_send_bytes(websocket, audio)

                # Text answer submission
                elif msg_type == "submit_answer":
                    answer = data.get("answer", "").strip()
                    if answer and current_question:
                        await evaluate_and_respond(
                            websocket, answer, current_question,
                            interview_type, interview_session_id
                        )

                # Move to next question
                elif msg_type == "next_question":
                    result = orchestrator.interview_agent.advance_question(
                        interview_session_id
                    )
                    if result.get("done"):
                        final = result.get("final_score", {})
                        await safe_send(websocket, {
                            "type":    "interview_complete",
                            "score":   final.get("overall", 0),
                            "grade":   final.get("grade", ""),
                            "advice":  final.get("advice", ""),
                            "message": f"Interview complete! Your score: {final.get('overall', 0)}/100"
                        })
                        audio = await text_to_speech_bytes_async(
                            f"Interview complete! Your overall score is {final.get('overall', 0)} out of 100. {final.get('advice', '')}"
                        )
                        await safe_send_bytes(websocket, audio)
                    else:
                        current_question = result["current_question"]
                        qnum = result["question_number"]
                        total = result["total_questions"]

                        await safe_send(websocket, {
                            "type":            "next_question",
                            "question":        current_question,
                            "question_number": qnum,
                            "total_questions": total,
                        })

                        audio = await text_to_speech_bytes_async(
                            f"Question {qnum}. {current_question}"
                        )
                        await safe_send_bytes(websocket, audio)

                elif msg_type == "ping":
                    await safe_send(websocket, {"type": "pong"})

            # Voice answer
            elif "bytes" in message:
                audio_bytes = message["bytes"]
                if len(audio_bytes) < 1000:
                    continue

                await safe_send(websocket, {
                    "type": "status",
                    "message": "Transcribing your answer..."
                })

                loop = asyncio.get_event_loop()
                try:
                    transcription = await loop.run_in_executor(
                        None, transcribe_audio_bytes, audio_bytes
                    )
                    answer = transcription["text"].strip()
                except Exception as e:
                    await safe_send(websocket, {
                        "type": "error",
                        "message": f"Could not transcribe: {str(e)}"
                    })
                    continue

                if not answer:
                    await safe_send(websocket, {
                        "type": "error",
                        "message": "Could not hear your answer. Please speak clearly."
                    })
                    continue

                await safe_send(websocket, {
                    "type": "transcript",
                    "text": answer,
                })

                await evaluate_and_respond(
                    websocket, answer, current_question,
                    interview_type, interview_session_id
                )

    except WebSocketDisconnect:
        print("Interview WebSocket disconnected")
    except Exception as e:
        print(f"Interview WebSocket error: {e}")


async def evaluate_and_respond(
    websocket: WebSocket,
    answer: str,
    question: str,
    interview_type: str,
    session_id: str,
):
    """Evaluate an interview answer and send feedback."""
    await safe_send(websocket, {
        "type": "status",
        "message": "Evaluating your answer..."
    })

    try:
        result = await orchestrator.interview_agent.evaluate_answer(
            question=question,
            answer=answer,
            interview_type=interview_type,
            session_id=session_id,
        )

        await safe_send(websocket, {
            "type":          "answer_evaluated",
            "score":         result["score"],
            "feedback":      result["feedback"],
            "improvement":   result["improvement"],
            "follow_up":     result["follow_up"],
            "encouragement": result["encouragement"],
        })

        # Speak the feedback
        feedback_text = f"{result['encouragement']} {result['feedback']} {result['improvement']}"
        try:
            audio = await asyncio.wait_for(
                text_to_speech_bytes_async(feedback_text),
                timeout=30.0
            )
            await safe_send_bytes(websocket, audio)
        except Exception as e:
            print(f"TTS error: {e}")

    except Exception as e:
        print(f"Evaluation error: {e}")
        await safe_send(websocket, {
            "type": "error",
            "message": str(e)
        })
# This is already handled — the double audio is from browser playing the blob twice
