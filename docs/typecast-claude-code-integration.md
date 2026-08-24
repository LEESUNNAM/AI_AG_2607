# Typecast Voice Integration for Claude Code

Automatically reads Claude Code's responses aloud using a chosen Typecast AI voice character, via a Stop hook.

## Files

- `scripts/typecast_client.py` — shared API client (auth, `/voices`, `/text-to-speech`)
- `scripts/typecast_list_voices.py` — lists available voice characters
- `scripts/typecast_speak.py` — converts text to speech and plays it (usable standalone)
- `.claude/hooks/typecast_stop_hook.py` — Stop hook that reads Claude's last response aloud
- `.claude/settings.json` — registers the Stop hook (30s timeout)
- `credentials/typecast_api_key.txt` — your API key (gitignored, not committed)
- `credentials/typecast_voice_id.txt` — the chosen voice's `voice_id` (gitignored)

## One-time setup

1. Get a free API key at https://typecast.ai/developers/api/ and save it to
   `credentials/typecast_api_key.txt` (one line, no quotes). Alternatively set
   the `TYPECAST_API_KEY` environment variable.
2. List available voices:
   ```
   python scripts/typecast_list_voices.py
   ```
3. Pick a voice and save its `voice_id` to `credentials/typecast_voice_id.txt`.
4. Test it manually:
   ```
   python scripts/typecast_speak.py "안녕하세요, 테스트입니다."
   ```
5. Reload hooks in Claude Code (`/hooks`) or restart the session so the new
   Stop hook takes effect.

## How it works

After every Claude Code response, the Stop hook receives
`last_assistant_message` on stdin, strips markdown/code/URLs, truncates to
500 characters, and calls `typecast_speak.speak()` with the saved voice_id.
Playback uses Windows' built-in `winsound` module (no extra dependencies).
Any failure (missing key, network error, etc.) is logged to
`credentials/typecast_hook_error.log` and never blocks Claude Code — the
hook always exits 0.

## Disabling

Remove the `hooks.Stop` section from `.claude/settings.json`, or delete
`credentials/typecast_voice_id.txt` (the hook will fail closed and just log).
