---
name: notion-personal
description: Register a new personal schedule/event entry into the user's Notion "개인일정" database using the Notion API tools (notion-fetch, notion-create-pages, notion-get-users). Use whenever the user asks to add a personal appointment, plan, reminder, or event to Notion — phrases like "노션에 일정 추가해줘", "이거 개인일정에 등록해줘", "치과 예약 노션에 넣어줘", "다음주 가족모임 일정 등록해줘", "친구랑 저녁 약속 노션에 기록해줘" — even when the user doesn't say "개인일정" explicitly, as long as it's a personal (non-work, non-study) plan they want tracked in Notion. Covers events with a date/time, category (가족/건강/약속/기타), and optionally people attending. Do NOT use this for work tasks (업무 DB) or study goals (학습 DB) — those belong to different databases.
---

# Notion Personal Schedule Registration

Registers a personal event the user mentions (an appointment, a family gathering, a doctor's visit, etc.) as a new page in the user's Notion "개인일정" (Personal Schedule) database. Uses only Notion API tools (`notion-fetch`, `notion-create-pages`, `notion-get-users`, `notion-search`) — never browser automation or Playwright.

## Known locations

- Parent page: "노션 db 연동 실습" (`https://app.notion.com/p/3cac1740333f80a1a657f705112bb28e`)
- Database: "개인일정" (`https://app.notion.com/p/efe330c63ad94be989e6c33d4c1c663e`)
- Data source (for schema lookups / queries): `collection://191e7deb-2d91-45c3-88e3-3e5c3afe7dc7`

These are reference defaults, not guarantees. **Before every registration, call `notion-fetch` on the database URL above to confirm the current schema.** Select options may have been added or renamed since this skill was written, and the IDs will differ entirely in a different workspace. If `notion-fetch` fails on the known ID, fall back to `notion-search` for "개인일정" to find the current URL.

## Property schema (as of 2026-08-31)

| Property | Type | How to set it |
|---|---|---|
| 제목 (Title) | title | String. This is the page title and is required. |
| 날짜 (Date) | date | See "Setting the date" below |
| 카테고리 (Category) | select | One of `"가족"` (family), `"건강"` (health), `"약속"` (appointment), `"기타"` (other) |
| 완료여부 (Done) | checkbox | `"__YES__"` (done) or `"__NO__"` (not done). Defaults to not-done if omitted |
| 함께하는 사람 (People) | person | Array of user ID strings. See "Setting attendees" below |
| 장소 (Place) | place | **Cannot be set directly via the API** (a coordinate-based special type). See "Handling location" below |
| 완료작업 (Completed work) | relation | Links to the 완료작업 database. Not used when registering a new schedule entry |

### Setting the date

`notion-create-pages` does not accept a single `날짜` key for date properties — it uses expanded column names instead:

- `"date:날짜:start"`: an ISO-8601 date or datetime string (e.g. `"2026-09-05"` or `"2026-09-05T18:00:00"`)
- `"date:날짜:is_datetime"`: `1` if a specific time was given, `0` or omitted if it's a date-only, all-day event
- `"date:날짜:end"`: only set this for a multi-day/ranged event. Leave it out entirely for a single date

When the user gives a relative date/time ("next Tuesday at 3pm"), resolve it to an absolute date against today's date before formatting it this way.

### Setting attendees

If the user mentions people attending ("with so-and-so"), look them up with `notion-get-users` (search by name) to get their user IDs, then pass those IDs as a string array under `"함께하는 사람"`. If a named person can't be matched to a workspace user, drop that name silently from the property and tell the user which name couldn't be resolved and why.

### Handling location

The `장소` property is Notion's "place" type, which often rejects a plain text string:

1. First try passing the location as a plain string under the `"장소"` key.
2. If the API rejects it, skip setting that property and instead add a line like "Location: X" to the page `content` so the information isn't lost.
3. Briefly tell the user which of the two ways the location ended up being stored.

## Registration steps

1. Call `notion-fetch` on the "개인일정" database to confirm the current data source URL and category options.
2. Extract from the user's message: title (required), date/time (required — ask if missing), category (infer the closest match among 가족/건강/약속/기타; if genuinely ambiguous, default to 기타 and tell the user), attendees (if any), location (if any).
3. Call `notion-create-pages` with `parent` set to `{"type": "data_source_id", "data_source_id": "<the data source ID confirmed above>"}`.
4. Report the created page's URL back to the user, along with a short summary of what was set (title/date/category/attendees/etc.).
5. If the user later asks to edit an existing entry's date, category, or completion status, find it with `notion-search` or `notion-query-data-sources`, then apply the change with `notion-update-page`.

## Example

**Input**: "다음주 화요일 저녁 7시에 치과 예약 있어, 노션에 등록해줘" (I have a dentist appointment next Tuesday at 7pm, add it to Notion)

**Processing**:
- Title: "치과 예약" (Dentist appointment)
- Date: resolve "next Tuesday" to its absolute date; `date:날짜:start` = that date at `T19:00:00`, `date:날짜:is_datetime` = 1
- Category: "건강" (Health)
- Done: left unset (defaults to not-done)

**Output**: the created Notion page URL, plus a confirmation such as "Added the dentist appointment to 개인일정 for Tue Sep X at 7pm, category '건강'."
