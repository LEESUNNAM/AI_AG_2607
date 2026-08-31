---
name: notion-work
description: Register a new work/task entry into the user's Notion "업무" database using the Notion API tools (notion-fetch, notion-create-pages, notion-get-users). Use whenever the user asks to add a task, ticket, project item, or to-do into Notion — phrases like "업무 노션에 등록해줘", "이 작업 업무 DB에 추가해줘", "새 랜딩페이지 개발 건 등록해줘", "이거 마감일 다음주 금요일로 업무에 넣어줘", "보고서 제출 건 담당자 지정해서 등록해줘" — even when the user doesn't say "업무" explicitly, as long as it's a work task, project item, or deadline-bound to-do they want tracked in Notion (assigning work, setting priority/deadline, tagging a project). Do NOT use this for personal plans (개인일정 DB) or study goals (학습 DB) — those belong to different databases.
---

# Notion Work Task Registration

Registers a work item the user mentions (a task, a project deliverable, a report submission, etc.) as a new page in the user's Notion "업무" (Work) database. Uses only Notion API tools (`notion-fetch`, `notion-create-pages`, `notion-get-users`, `notion-search`) — never browser automation or Playwright.

## Known locations

- Parent page: "노션 db 연동 실습" (`https://app.notion.com/p/3cac1740333f80a1a657f705112bb28e`)
- Database: "업무" (`https://app.notion.com/p/c6a2b4d7222248a3a5d550389d36bb25`)
- Data source (for schema lookups / queries): `collection://af79721d-da7c-400c-8475-f608a765da25`

These are reference defaults, not guarantees. **Before every registration, call `notion-fetch` on the database URL above to confirm the current schema** — option lists (status, priority, project tags) may have changed, and IDs will differ entirely in a different workspace. If `notion-fetch` fails on the known ID, fall back to `notion-search` for "업무" to find the current URL.

## Property schema (as of 2026-08-31)

| Property | Type | How to set it |
|---|---|---|
| 제목 (Title) | title | String. This is the page title and is required. |
| 상태 (Status) | status | One of `"시작 전"` (not started), `"진행 중"` (in progress), `"완료"` (done). Defaults to `"시작 전"` if omitted |
| 담당자 (Assignee) | person | Array of user ID strings. See "Setting the assignee" below |
| 우선순위 (Priority) | select | One of `"높음"` (high), `"중간"` (medium), `"낮음"` (low) |
| 프로젝트 (Project tag) | multi_select | Zero or more of `"개발"` (dev), `"기획"` (planning), `"마케팅"` (marketing), `"기타"` (other), as a string array |
| 등록일 (Registered date) | date | See "Setting dates" below |
| 마감일 (Deadline) | date | See "Setting dates" below |
| 제출처 (Submit-to / destination) | text | Plain string — who or where the deliverable goes (e.g. a person, team, or platform) |
| 완료작업 (Completed work) | relation | Links to the 완료작업 database. Not used when registering a new task |
| 잔여기한 (Time remaining) | formula | **Read-only** — computed automatically from 마감일. Never try to set this |

### Setting dates

Note there are **two separate date properties** — don't conflate them:

- `등록일` = when the task was registered/created. If the user doesn't give one, default it to today's date so the task has a registration date on record.
- `마감일` = the deadline. Only set this if the user actually gives a due date; don't invent one.

For each, `notion-create-pages` uses expanded column names rather than a single date key:

- `"date:등록일:start"` / `"date:마감일:start"`: an ISO-8601 date or datetime string (e.g. `"2026-09-05"` or `"2026-09-05T18:00:00"`)
- `"date:등록일:is_datetime"` / `"date:마감일:is_datetime"`: `1` if a specific time was given, `0` or omitted for a date-only value
- `"date:등록일:end"` / `"date:마감일:end"`: only set for a ranged/multi-day value; leave out for a single date

Resolve any relative date the user gives ("next Friday", "in two weeks") to an absolute date against today's date before formatting it this way.

### Setting the assignee

If the user names who the task is assigned to, look them up with `notion-get-users` (search by name) to get their user ID, then pass it as a string array under `"담당자"`. If the user doesn't name an assignee, default to the current user (`notion-get-users` with `user_id: "self"`) rather than leaving it empty, since a work task with no owner is easy to lose track of — but mention that you defaulted it so the user can correct it if the task actually belongs to someone else. If a named person can't be matched to a workspace user, drop them and tell the user which name couldn't be resolved.

### Inferring priority and project tag

If the user states priority or a project category explicitly, use it. If not:
- Leave `우선순위` unset rather than guessing — priority is a judgment call that shouldn't be invented.
- For `프로젝트`, infer a tag only when the task content makes it unambiguous (e.g. "새 랜딩페이지 개발" clearly maps to `"개발"`); otherwise leave it unset rather than force a guess into `"기타"`.

## Registration steps

1. Call `notion-fetch` on the "업무" database to confirm the current data source URL and the status/priority/project option lists.
2. Extract from the user's message: title (required), deadline if given, assignee if named (else default to self), priority if stated, project tag if the content makes it obvious, submit-to/destination if mentioned.
3. Call `notion-create-pages` with `parent` set to `{"type": "data_source_id", "data_source_id": "<the data source ID confirmed above>"}`. Set `등록일` to today unless the user gave a different registration date.
4. Report the created page's URL back to the user, along with a short summary of what was set (title/status/deadline/assignee/priority/project).
5. If the user later asks to update a task's status, deadline, priority, or assignee, find it with `notion-search` or `notion-query-data-sources`, then apply the change with `notion-update-page`.

## Example

**Input**: "새 랜딩페이지 개발 업무 등록해줘, 마감일은 다음주 금요일, 우선순위 높음으로"

**Processing**:
- Title: "새 랜딩페이지 개발"
- Status: left unset (defaults to "시작 전")
- 등록일: today
- 마감일: resolve "next Friday" to its absolute date; `date:마감일:start` = that date, `date:마감일:is_datetime` = 0
- Priority: "높음"
- Project: "개발" (inferred from "개발" in the task title)
- Assignee: defaulted to the current user (mention this default)

**Output**: the created Notion page URL, plus a confirmation such as "새 랜딩페이지 개발을 업무 DB에 등록했습니다 — 마감일 9월 X일(금), 우선순위 높음, 담당자는 본인으로 지정했습니다."
