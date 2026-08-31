---
name: notion-complete
description: Register, look up, or update entries in the user's Notion "완료작업" (completed-work archive) database using the Notion API tools (notion-fetch, notion-create-pages, notion-update-page, notion-search, notion-get-users). Use whenever the user says they finished something that came from the 개인일정, 업무, or 학습 databases and wants it logged as done — phrases like "완료작업에 등록해줘", "이거 완료작업 DB에 추가해줘", "방금 끝낸 업무 완료작업에 넣어줘", "이 학습 완료 처리하고 완료작업에 기록해줘", "치과 예약 다녀왔어 완료 처리해줘" — even without saying "완료작업" explicitly, whenever the user is marking a personal-schedule, work, or study item as finished. Also use when the user wants to review what's been completed recently, check how long something took, or update a completed entry's retrospective, time spent, or data location.
---

# Notion Completed-Work Archive

Logs a finished item into the user's Notion "완료작업" (Completed Work) database, and links it back to the entry it came from in 개인일정 (personal schedule), 업무 (work), or 학습 (study). Uses only Notion API tools (`notion-fetch`, `notion-create-pages`, `notion-update-page`, `notion-search`, `notion-query-data-sources`, `notion-get-users`) — never browser automation or Playwright.

## Why this DB is different from the other three

개인일정/업무/학습 each hold *open* items — things still to do or in progress. 완료작업 is the archive they graduate into: it doesn't just record a title, it links back to the original page via a relation property, records how long it took and when it finished, and optionally holds a retrospective note. So registering a completed item is a two-part job: (1) find the original entry so you can link to it and mark it done there too, and (2) create the archive record here. Skipping part (1) leaves the source page stuck showing as unfinished even though the user considers it done.

## Known locations

- Parent page: "노션 db 연동 실습" (`https://app.notion.com/p/3cac1740333f80a1a657f705112bb28e`)
- Database: "완료작업" (`https://app.notion.com/p/9fddb21213b34ca3b8c3ded5e184997a`)
- Data source (for schema lookups / queries): `collection://5a6642c4-6001-4615-94fa-eb560e8e892b`
- Source databases it links to:
  - 개인일정: `collection://191e7deb-2d91-45c3-88e3-3e5c3afe7dc7` (relation property: `개인일정 연결`)
  - 업무: `collection://af79721d-da7c-400c-8475-f608a765da25` (relation property: `업무 연결`)
  - 학습: `collection://6f22d7c7-a820-4cd3-b04c-ce065418cefa` (relation property: `학습 연결`)

These are reference defaults, not guarantees. **Before every registration, call `notion-fetch` on the 완료작업 database URL to confirm the current schema** — IDs will differ entirely in a different workspace, and option lists may have changed. If a known ID fails, fall back to `notion-search`.

## Property schema (as of 2026-08-31)

| Property | Type | How to set it |
|---|---|---|
| 제목 (Title) | title | String. This is the page title and is required. |
| 원본유형 (Origin type) | select | One of `"개인일정"`, `"업무"`, `"학습"` — which source database this came from |
| 완료일 (Completion date) | date | See "Setting the completion date" below |
| 담당자 (Owner) | person | Array of user ID strings. Default to the current user if not stated (via `notion-get-users` with `user_id: "self"`), the same way notion-work does, and mention the default |
| 소요시간 (Time spent) | number | A plain number (e.g. hours). Only set if the user gives a value — don't estimate one |
| 소요기간 (Duration/period) | number | A plain number (e.g. days elapsed from start to finish). Only set if the user gives or it can be computed from known start/end dates — don't guess |
| 자료위치 (Data location) | text | Plain string — where related files/notes live (a folder, doc link, etc.). Only if mentioned |
| 회고 (Retrospective) | text | Plain string — a short reflection on how it went. Only if the user gives one |
| 개인일정 연결 / 업무 연결 / 학습 연결 (Source link) | relation | Set **only the one matching 원본유형**, to the source page's URL/ID. See "Linking back to the source" below |

### Setting the completion date

`notion-create-pages` uses expanded column names rather than a single `완료일` key:

- `"date:완료일:start"`: an ISO-8601 date or datetime string. Default to today if the user doesn't specify when it finished.
- `"date:완료일:is_datetime"`: `1` if a specific time was given, `0` or omitted otherwise
- `"date:완료일:end"`: only for a ranged value; normally omit this

### Linking back to the source

1. Figure out which source database the item came from (개인일정/업무/학습). The user's phrasing usually makes this obvious ("치과 예약" → 개인일정, "랜딩페이지 개발" → 업무, "React 강의" → 학습); ask only if genuinely ambiguous.
2. Use `notion-search` (or `notion-query-data-sources` against the matching data source) to find the specific existing page in that database. Match by title/content the user described. If you can't find a matching page, still create the 완료작업 entry but skip the relation link and tell the user you couldn't find the original to connect it to.
3. In `notion-create-pages`, set the one relation property that matches 원본유형 (e.g. `"업무 연결": ["<found page URL or ID>"]`) — this is a two-way relation, so linking from this side automatically shows up on the source page's own 완료작업 field too.
4. Separately, mark the source page itself as done: for a 개인일정 entry set `"완료여부": "__YES__"`; for a 업무 or 학습 entry set its status property (`상태` or `진행상태`) to `"완료"`. Do this with `notion-update-page` on the source page. This step matters because the relation link alone doesn't change the source's own completion status — without it, the task would show up as both "linked to a completed record" and "still not done," which is confusing.

## Registration steps

1. Call `notion-fetch` on the "완료작업" database to confirm the current data source URL and 원본유형 options.
2. From the user's message, determine: title, origin type (개인일정/업무/학습), completion date (default today), owner (default self), and any of 소요시간/소요기간/자료위치/회고 that were mentioned.
3. Find the source page as described above, and update its completion status.
4. Call `notion-create-pages` with `parent` set to `{"type": "data_source_id", "data_source_id": "<완료작업 data source ID>"}`, including the matching relation property if a source page was found.
5. Report the created page's URL back to the user, confirm whether the source entry's status was updated, and summarize what was logged.

## Looking up or updating completed entries

For requests like "최근에 완료한 거 뭐 있어?" or "그 완료작업 회고 좀 추가해줘":
- Use `notion-search` or `notion-query-data-sources` (SQL mode, e.g. filtering/sorting by `date:완료일:start`) against the 완료작업 data source to find entries.
- For updates (회고, 소요시간, 소요기간, 자료위치), use `notion-update-page` on the specific page found.

## Example

**Input**: "React 기초 강의 다 들었어, 완료작업에 등록해줘. 3일 걸렸고 총 6시간 정도 썼어"

**Processing**:
- Title: "React 기초 강의 수강 완료"
- 원본유형: "학습" (a course → study)
- Find the matching page in 학습 (e.g. "React 기초 강의") via search
- Update that 학습 page: `"진행상태": "완료"`
- 완료일: today
- 소요기간: 3, 소요시간: 6
- 담당자: defaulted to current user (mention this)
- 학습 연결: set to the found source page

**Output**: the created 완료작업 page URL, plus a confirmation such as "React 기초 강의를 완료작업에 기록하고, 학습 DB의 원본 항목도 '완료' 상태로 업데이트했습니다. 소요기간 3일, 소요시간 6시간."
