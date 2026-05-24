import whisper
import tempfile
import os
import subprocess
import asyncio

_model = None

def get_whisper_model():
    global _model
    if _model is None:
        print("Loading Whisper model...")
        _model = whisper.load_model("base")
        print("Whisper model loaded")
    return _model


def convert_to_wav(input_path: str) -> str:
    """Convert any audio format to WAV using ffmpeg."""
    output_path = input_path.replace('.tmp', '.wav').replace('.webm', '.wav')
    if not output_path.endswith('.wav'):
        output_path = input_path + '.wav'

    try:
        result = subprocess.run([
            'ffmpeg', '-y',
            '-i', input_path,
            '-ar', '16000',      # 16kHz sample rate for Whisper
            '-ac', '1',          # Mono channel
            '-f', 'wav',
            output_path
        ], capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"ffmpeg error: {result.stderr}")
            return None
        return output_path
    except Exception as e:
        print(f"Conversion error: {e}")
        return None


def transcribe_audio_file(audio_path: str) -> dict:
    """Transcribe an audio file using Whisper."""
    model = get_whisper_model()

    result = model.transcribe(
        audio_path,
        language="en",
        task="transcribe",
        word_timestamps=True,
        fp16=False,
        verbose=False,
    )

    return {
        "text": result["text"].strip(),
        "language": result.get("language", "en"),
        "segments": result.get("segments", []),
        "words": extract_words(result.get("segments", [])),
    }


def extract_words(segments: list) -> list:
    words = []
    for segment in segments:
        if "words" in segment:
            for word in segment["words"]:
                words.append({
                    "word": word.get("word", "").strip(),
                    "start": word.get("start", 0),
                    "end": word.get("end", 0),
                    "probability": word.get("probability", 0),
                })
    return words


def transcribe_audio_bytes(audio_bytes: bytes) -> dict:
    """
    Transcribe raw audio bytes from browser.
    Handles webm, ogg, wav — converts to wav first.
    """
    # Save raw bytes to temp file
    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    wav_path = None
    try:
        # Convert to WAV first
        wav_path = convert_to_wav(tmp_path)

        if wav_path and os.path.exists(wav_path):
            # Check file has audio content
            size = os.path.getsize(wav_path)
            print(f"WAV file size: {size} bytes")

            if size < 1000:
                return {"text": "", "words": [], "segments": []}

            result = transcribe_audio_file(wav_path)
            print(f"Transcribed: '{result['text']}'")
            return result
        else:
            # Fallback — try transcribing original
            result = transcribe_audio_file(tmp_path)
            return result

    except Exception as e:
        print(f"Transcription error: {e}")
        import traceback
        traceback.print_exc()
        return {"text": "", "words": [], "segments": []}

    finally:
        # Clean up temp files
        for path in [tmp_path, wav_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass


def count_filler_words(text: str) -> dict:
    filler_words = [
        "umm", "um", "uh", "uhh", "like", "basically",
        "you know", "i mean", "sort of", "kind of",
        "actually", "literally", "right", "so yeah"
    ]
    text_lower = text.lower()
    counts = {}
    total = 0
    for filler in filler_words:
        count = text_lower.count(filler)
        if count > 0:
            counts[filler] = count
            total += count
    return {"total_filler_count": total, "filler_breakdown": counts}


def calculate_speaking_speed(text: str, duration_seconds: float) -> float:
    if duration_seconds <= 0:
        return 0.0
    word_count = len(text.split())
    minutes = duration_seconds / 60
    return round(word_count / minutes, 1) if minutes > 0 else 0
