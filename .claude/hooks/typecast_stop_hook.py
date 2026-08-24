"""Stop hook: read Claude's last response aloud using a Typecast voice.

Registered in .claude/settings.json under hooks.Stop. Reads the hook JSON
payload from stdin, strips it down to speakable text, and calls
scripts/typecast_speak.py. Failures (missing API key, network error, etc.)
are logged but never block Claude Code, since this hook always exits 0.
"""

import json
import os
import re
import sys

sys.stdin.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))


def clean_text(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[#*_>]+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:500]


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    message = payload.get("last_assistant_message", "") or ""
    text = clean_text(message)
    if not text:
        sys.exit(0)

    try:
        from typecast_speak import speak

        speak(text)
    except Exception as exc:
        log_path = os.path.join(BASE_DIR, "credentials", "typecast_hook_error.log")
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"{exc}\n")
        except Exception:
            pass

    sys.exit(0)


if __name__ == "__main__":
    main()
