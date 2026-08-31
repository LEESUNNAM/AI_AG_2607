---
name: notion-study
description: Register a new learning/study entry into the user's Notion "학습" database using the Notion API tools (notion-fetch, notion-create-pages). Use whenever the user asks to add a study topic, course, exam prep item, or learning goal into Notion — phrases like "학습 노션에 등록해줘", "이 강의 학습 DB에 추가해줘", "토익 공부 학습에 넣어줘", "이거 목표일 다음달 말로 학습에 등록해줘", "정보처리기사 공부 시작하는 거 기록해줘" — even when the user doesn't say "학습" explicitly, as long as it's a course, certification prep, language study, or any learning goal they want tracked in Notion. Do NOT use this for personal plans (개인일정 DB) or work tasks (업무 DB) — those belong to different databases.
---

# Notion Study Entry Registration

Registers a learning goal the user mentions (a course, an exam/certification prep item, a language-study plan, etc.) as a new page in the user's Notion "학습" (Study) database. Uses only Notion API tools (`notion-fetch`, `notion-create-pages`, `notion-search`) — never browser automation or Playwright.

## Known locations

- Parent page: "노션 db 연동 실습" (`https://app.notion.com/p/3cac1740333f80a1a657f705112bb28e`)
- Database: "학습" (`https://app.notion.com/p/d493740677784deb9a14fdf9f9546f3b`)
- Data source (for schema lookups / queries): `collection://6f22d7c7-a820-4cd3-b04c-ce065418cefa`

These are reference defaults, not guarantees. **Before every registration, call `notion-fetch` on the database URL above to confirm the current schema** — option lists (진행상태, 난이도, 분야) may have changed, and IDs will differ entirely in a different workspace. If `notion-fetch` fails on the known ID, fall back to `notion-search` for "학습" to find the current URL.

## Property schema (as of 2026-08-31)

| Property | Type | How to set it |
|---|---|---|
| 제목 (Title) | title | String. This is the page title and is required. |
| 진행상태 (Progress status) | status | One of `"시작 전"` (not started), `"진행 중"` (in progress), `"완료"` (done). Defaults to `"시작 전"` if omitted |
| 난이도 (Difficulty) | select | One of `"상"` (high), `"중"` (medium), `"하"` (low) |
| 분야 (Field) | select | One of `"개발"` (development), `"어학"` (language), `"자격증"` (certification), `"기타"` (other) |
| 목표일 (Target date) | date | See "Setting the target date" below |
| 자료 링크 (Material link) | url | A single URL string (e.g. a course page, video, or article) |
| 출처 (Source) | text | Plain string — where the material/course comes from (a platform, book, instructor) |
| 등록보고서 제목 (Registered report title) | text | Plain string. Only set this if the user is registering a study *report/write-up* they've produced, not for a plain study goal — see note below |
| 완료작업 (Completed work) | relation | Links to the 완료작업 database. Not used when registering a new study entry |

### Setting the target date

`notion-create-pages` uses expanded column names rather than a single `목표일` key:

- `"date:목표일:start"`: an ISO-8601 date or datetime string (e.g. `"2026-10-31"`)
- `"date:목표일:is_datetime"`: `1` if a specific time was given, `0` or omitted for a date-only value
- `"date:목표일:end"`: only set for a ranged value; leave out for a single date

Resolve any relative date the user gives ("by the end of next month", "in 3 weeks") to an absolute date against today's date before formatting it this way. If the user doesn't mention a target date at all, leave it unset rather than inventing one — an open-ended learning goal is fine.

### Inferring field and difficulty

If the user states the field or difficulty explicitly, use it. If not:
- `분야` can usually be inferred confidently from the topic (e.g. "토익", "일본어" → `"어학"`; "정보처리기사", "AWS 자격증" → `"자격증"`; "React", "파이썬" → `"개발"`). Only fall back to `"기타"` when the topic genuinely doesn't fit the other three.
- `난이도` is a personal judgment call — leave it unset unless the user states it themselves.

### About 등록보고서 제목

This field is distinct from 제목: it holds the title of a study *report or summary write-up* linked to this entry (e.g. after finishing a chapter and writing notes), not the study goal itself. Leave it empty when simply registering a new learning goal; only fill it in if the user is explicitly logging a report they've already written.

## Registration steps

1. Call `notion-fetch` on the "학습" database to confirm the current data source URL and the 진행상태/난이도/분야 option lists.
2. Extract from the user's message: title (required), target date if given, field (infer if the topic makes it clear), difficulty if stated, material link if given, source if mentioned.
3. Call `notion-create-pages` with `parent` set to `{"type": "data_source_id", "data_source_id": "<the data source ID confirmed above>"}`.
4. Report the created page's URL back to the user, along with a short summary of what was set (title/field/target date/difficulty).
5. If the user later asks to update an entry's progress status, difficulty, or target date, find it with `notion-search` or `notion-query-data-sources`, then apply the change with `notion-update-page`.

## Example

**Input**: "정보처리기사 필기 준비 시작했어, 다음달 말까지가 목표야. 노션 학습에 등록해줘"

**Processing**:
- Title: "정보처리기사 필기 준비"
- 진행상태: left unset (defaults to "시작 전")
- 분야: "자격증" (inferred from "정보처리기사")
- 목표일: resolve "by the end of next month" to its absolute date; `date:목표일:start` = that date, `date:목표일:is_datetime` = 0
- 난이도: left unset (not stated)

**Output**: the created Notion page URL, plus a confirmation such as "정보처리기사 필기 준비를 학습 DB에 등록했습니다 — 분야 '자격증', 목표일 10월 말."
