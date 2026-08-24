"""Shared helpers for calling the Typecast text-to-speech API.

API key is read from (in order): TYPECAST_API_KEY env var, then
credentials/typecast_api_key.txt (gitignored). Never hardcode the key here.
"""

import os

import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_DIR = os.path.join(BASE_DIR, "credentials")
API_KEY_FILE = os.path.join(CREDENTIALS_DIR, "typecast_api_key.txt")
API_BASE = "https://api.typecast.ai/v1"


def get_api_key() -> str:
    env_key = os.environ.get("TYPECAST_API_KEY")
    if env_key:
        return env_key.strip()
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r", encoding="utf-8") as f:
            key = f.read().strip()
        if key:
            return key
    raise RuntimeError(
        "Typecast API 키를 찾을 수 없습니다. "
        "TYPECAST_API_KEY 환경변수를 설정하거나 "
        f"{API_KEY_FILE} 파일에 키를 저장하세요."
    )


def list_voices() -> list[dict]:
    resp = requests.get(
        f"{API_BASE}/voices",
        headers={"X-API-KEY": get_api_key()},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def synthesize(
    text: str,
    voice_id: str,
    model: str = "ssfm-v30",
    language: str | None = None,
    emotion_preset: str | None = None,
    audio_format: str = "wav",
) -> bytes:
    text = text[:2000]
    body = {
        "voice_id": voice_id,
        "text": text,
        "model": model,
        "output": {"audio_format": audio_format},
    }
    if language:
        body["language"] = language
    if emotion_preset:
        body["prompt"] = {"emotion_preset": emotion_preset}

    resp = requests.post(
        f"{API_BASE}/text-to-speech",
        headers={"Content-Type": "application/json", "X-API-KEY": get_api_key()},
        json=body,
        timeout=60,
    )
    if not resp.ok:
        raise RuntimeError(f"Typecast API error {resp.status_code}: {resp.text[:300]}")
    return resp.content
