import asyncio
import io
import os
import tempfile


def text_to_speech_bytes(text: str) -> bytes:
    """
    Convert text to speech using gTTS.
    Returns MP3 bytes directly.
    """
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        mp3_buffer = io.BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)
        return mp3_buffer.read()
    except Exception as e:
        print(f"gTTS error: {e}")
        # Return empty bytes if TTS fails — coaching text still shown
        return b""


async def text_to_speech_bytes_async(text: str) -> bytes:
    """Async wrapper for TTS."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, text_to_speech_bytes, text)
