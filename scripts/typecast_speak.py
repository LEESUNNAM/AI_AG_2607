"""Convert text to speech with a chosen Typecast voice and play it aloud.

Usage:
    python scripts/typecast_speak.py "읽어줄 텍스트" --voice-id tc_xxxx
Voice id defaults to credentials/typecast_voice_id.txt if --voice-id is omitted.
"""

import argparse
import os
import sys
import tempfile
import winsound

from typecast_client import synthesize

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE_ID_FILE = os.path.join(BASE_DIR, "credentials", "typecast_voice_id.txt")


def default_voice_id() -> str:
    if os.path.exists(VOICE_ID_FILE):
        with open(VOICE_ID_FILE, "r", encoding="utf-8") as f:
            voice_id = f.read().strip()
        if voice_id:
            return voice_id
    raise RuntimeError(
        f"voice_id가 지정되지 않았습니다. --voice-id를 전달하거나 {VOICE_ID_FILE} 파일에 저장하세요."
    )


def speak(text: str, voice_id: str | None = None, emotion_preset: str | None = None) -> None:
    if not text.strip():
        return
    voice_id = voice_id or default_voice_id()
    audio = synthesize(text, voice_id=voice_id, emotion_preset=emotion_preset, audio_format="wav")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio)
        path = f.name

    try:
        winsound.PlaySound(path, winsound.SND_FILENAME)
    finally:
        os.remove(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", help="읽어줄 텍스트 (생략 시 stdin에서 읽음)")
    parser.add_argument("--voice-id", default=None)
    parser.add_argument("--emotion", default=None, help="normal|happy|sad|angry|whisper|toneup|tonedown")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    speak(text, voice_id=args.voice_id, emotion_preset=args.emotion)


if __name__ == "__main__":
    main()
