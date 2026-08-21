---
name: gws-docs
description: Researches a given topic on the web and writes it up directly into a real, live Google Docs document (not a local file) using this project's GWS CLI tool (scripts/gws_docs_create.py). Use this whenever the user asks for a document about a topic and wants it specifically in Google Docs / 구글 독스 / 구글 문서 — phrases like "구글독스에 ~ 보고서 작성해줘", "이 주제로 구글 문서 만들어줘", "Google Docs로 정리해줘", "구글독스에 올려줘", "write this up in Google Docs" — even if they don't spell out every step, since "구글독스" or "Google Docs" naming the destination is the trigger, not just "보고서 써줘" alone. Do NOT use this for a local .docx/Word file request (that's the research-report-docx skill) — only trigger when the destination is explicitly the online Google Docs service. Also trigger for follow-up requests to add content to or extend an existing GWS-created Google Doc.
---

# GWS Docs (research → live Google Doc)

Turn a bare topic into a short, sourced report written directly into a real Google Docs document via this project's GWS integration — the user gets a shareable `docs.google.com` link back, not a file to upload themselves.

## Why this shape

The whole point of asking for "구글독스" instead of a Word file is that the user wants something already live and shareable — no download/upload step. Skipping the actual API call and just handing back a local .docx defeats the request. Keep the report itself light (this is meant to be fast — see §3), but never skip the "actually create it via the API and hand back the URL" part.

## 1. Pin down the topic and language

Most requests are already specific enough. If the topic is too broad to say anything concrete about ("경제", "AI"), ask the user to narrow it. Default to Korean unless the user asks in another language. Don't ask about depth or output format — those are fixed by this skill (see below).

## 2. Research with WebSearch/WebFetch

Use `WebSearch` (and `WebFetch` on promising results when you need more than a snippet) to gather real, current information — don't invent facts. Keep a running list of `(title, url)` pairs as you go; you need them verbatim for the source list at the end. For anything time-sensitive (prices, stats, news), note how current the source is.

## 3. Keep the report short

Default depth is light — this skill is for a fast, shareable writeup, not a deep research report (use `research-report-docx` instead if the user wants a full multi-section report as a local file). Aim for roughly this shape as plain text:

```
<제목>
작성일: <날짜>

1. 개요
<2-3문장으로 무엇에 대한 문서인지>

2. <주요 내용 A>
<핵심 사실/수치, 근거 포함>

3. <주요 내용 B — 필요한 만큼 섹션 추가, 보통 2-4개면 충분>

4. 요약
<핵심을 다시 한 번 정리>

출처:
- <출처명> (<url>)
- <출처명> (<url>)
```

This is plain text, not python-docx — `gws_docs_create.py` inserts it as-is into the document body (no bold/heading styling applied automatically), so numbered section labels like "1. 개요" are what carry the structure visually.

## 4. Write the content to a temp file, then create the doc

Write the plain-text report above to a file in the scratchpad/temp directory (never commit this file — it's throwaway), then call the GWS CLI tool from the repo root:

```bash
python scripts/gws_docs_create.py --title "<문서 제목>" --content-file "<path-to-temp-file>"
```

This prints:
```
documentId: <id>
url: https://docs.google.com/document/d/<id>/edit
```

That `url` is the deliverable — report it back to the user.

## 5. Handle first-time auth and the API-not-enabled error

Two things can happen on a machine/account where `documents` scope hasn't been used before — both are expected, not failures to work around silently:

- **First-ever run for this scope**: the script opens a browser to `accounts.google.com` for OAuth consent and blocks until the user approves. Run it via Bash with `run_in_background: true` and a generous timeout, tell the user a browser window needs their approval, and pick the result up from the background task's output once it completes. The granted token is cached to `credentials/gws_docs_token.json`, so this only happens once.
- **`Google Docs API has not been used in project ... or it is disabled` (HTTP 403 SERVICE_DISABLED)**: this means OAuth succeeded but the Docs API itself isn't turned on for the Google Cloud project behind `credentials/gws_oauth_client_secret.json`. The error message includes an activation URL (`https://console.developers.google.com/apis/api/docs.googleapis.com/overview?project=...`) — surface that link to the user, ask them to click "사용 설정"/"Enable", wait for their confirmation, then re-run the exact same command. This is a one-time setup step per Google Cloud project, not a recurring problem.

## 6. Report back

After the doc is created, tell the user in chat: the title, the URL, and a 1-2 sentence summary of what it covers and how many sources were used. Don't paste the full report text into chat — the live doc is the deliverable.

## Edge cases

- **Topic has little real coverage**: say so in the 개요 section rather than padding with speculation.
- **User provides their own source material** instead of asking for web research: skip WebSearch, build the report from what they gave you, and note in 개요 that it's based on user-provided material.
- **User asks to add to / extend an existing GWS-created doc** rather than create a new one: this skill's script only creates new documents. Use the Docs API directly (`documents().batchUpdate` with an `insertText` request against the existing `documentId`) the same way `gws_docs_create.py` does internally, rather than creating a duplicate document.
- **User actually wanted a local file**, not something live/shareable: that's `research-report-docx`, not this skill — check which one actually matches before starting.
