---
name: gws-calendar
description: Registers a real event on the user's Google Calendar using this project's GWS CLI tool (scripts/gws_calendar_create.py) — creates it directly via the Calendar API, not just a suggestion in chat. Use this whenever the user asks to add, register, schedule, or book something on their calendar — phrases like "캘린더에 일정 추가해줘", "다음주 화요일 3시에 회의 잡아줘", "구글 캘린더에 등록해줘", "일정 하나 잡아줄래", "schedule a meeting for me", "add this to my calendar" — even if they just describe an event casually without saying "캘린더" explicitly, as long as they clearly want it to actually exist on their calendar afterward (not just a reminder written in chat). This is distinct from the 일정관리 subagent, which only reads/briefs on existing events — use gws-calendar for anything that writes a new event. Also trigger for requests to invite others to a meeting via calendar invite.
---

# GWS Calendar (register a real event)

Create an actual Google Calendar event via the Calendar API — the user should end up with something they (and, if invited, others) can see on their real calendar, not just a description of what they should add themselves.

## Why this needs care

Unlike the read-only calendar briefing, this skill writes to the user's real calendar and — if attendees are involved — sends real email invites to other people. A wrong date/time is annoying to fix; a wrong or unintended attendee list means someone else gets an unwanted invite in their inbox. Get the details right and confirmed before calling the API, not after.

## 1. Gather the event details

Required: **title**, **date**, and **start/end time** (or mark it all-day). Don't guess these if they're missing or ambiguous — ask. In particular:

- Resolve relative dates ("다음주 화요일", "내일") to an absolute date yourself using today's date (available in your context), and state the resolved date back to the user as part of your confirmation rather than assuming silently — a misread "다음주" is a classic source of wrong-day events.
- Default timezone is `Asia/Seoul` (`+09:00`) unless the user's context says otherwise.
- If the user only gives a start time with no duration, default to 1 hour unless the type of event implies otherwise.
- Location and description are optional — include them only if the user mentions them or they're obviously implied.

## 2. Attendees require explicit confirmation

If the user wants to invite other people, this sends them a real calendar invite email the moment you run the script (`sendUpdates=all`). Before running it:
- Read back the exact list of email addresses you're about to invite and get explicit confirmation, even if the user already listed them — a typo'd email is hard to notice after the fact and either fails silently or emails the wrong person.
- If the user names people without emails ("팀원들한테"), ask for the actual addresses — don't guess them.
- If there are no attendees, skip this step; `sendUpdates` is automatically `none` for a personal-only event.

## 3. Create the event

From the repo root:

```bash
python scripts/gws_calendar_create.py \
  --summary "<제목>" \
  --start "2026-08-25T10:00:00+09:00" \
  --end "2026-08-25T11:00:00+09:00" \
  --location "<선택>" \
  --description "<선택>" \
  --attendees "a@example.com,b@example.com"
```

For an all-day event, add `--all-day` and pass plain dates (`--start 2026-08-25 --end 2026-08-26` — Calendar's all-day `end` is exclusive, so a single-day all-day event's end date is the day *after* start).

This prints:
```
eventId: <id>
htmlLink: <google calendar event url>
```

## 4. First-time auth

This script uses its own write-scoped token (`credentials/gws_calendar_events_token.json`, scope `calendar.events`), separate from the read-only briefing token. On first use it opens a browser for OAuth consent — run it via Bash with `run_in_background: true`, tell the user a browser approval is needed, and pick up the result from the background task output once it completes. If you hit `Google Calendar API has not been used ... or it is disabled` (unlikely, since the briefing script already exercises this API, but possible on a fresh project), surface the activation link from the error message the same way as any other GWS API-not-enabled error, wait for the user to enable it, then retry.

## 5. Report back

Tell the user: the event title, the resolved date/time, and the `htmlLink`. If attendees were invited, confirm invites were sent to the addresses used.

## Edge cases

- **Recurring events**: this script only creates single events — if the user wants a repeating event, say that's not currently supported rather than silently creating just the first occurrence and calling it done.
- **Possible double-booking**: if it seems useful (e.g. the user is scheduling something on a day that sounds busy), you can check for conflicts first with `scripts/gws_calendar_briefing.py` before creating the new event, and flag any overlap to the user.
- **Vague event ("일정 하나 잡아줘" with no other details)**: ask for at minimum a title and date/time before calling the script — don't invent a placeholder title.
