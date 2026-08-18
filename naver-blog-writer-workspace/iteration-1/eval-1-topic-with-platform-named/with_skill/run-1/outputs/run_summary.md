# Naver Blog Writer — Skill Test Run Summary

**Test scenario:** topic-with-platform-named / with_skill
**User request (verbatim):** "이번 여름 휴가철 국내 여행지 추천 주제로 네이버 블로그에 글 써줘"
(Translation: "Write a Naver Blog post recommending domestic summer vacation travel spots.")

## 1. Skill loaded

Read `.claude/skills/naver-blog-writer/SKILL.md` in full before acting, per the skill-creator test protocol. The skill's flow is: login handoff → topic → template → research → draft → temp-save → approval → publish, and it explicitly says never touch the user's Naver password.

The user's request already names both the topic ("이번 여름 휴가철 국내 여행지 추천") and the platform ("네이버 블로그"), so per §3 of the skill, the topic should NOT be re-requested from the user once login completes.

## 2. Tools used, in order

1. **`ToolSearch`** — `select:mcp__playwright__browser_navigate,mcp__playwright__browser_snapshot,mcp__playwright__browser_click,mcp__playwright__browser_type,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_find` — loaded the Playwright MCP tool schemas per skill §1. Playwright MCP tools were available.
2. **`mcp__playwright__browser_navigate`** → `https://blog.naver.com` — landed on `https://section.blog.naver.com/BlogHome.naver` ("네이버 블로그" home).
3. **`mcp__playwright__browser_snapshot`** — attempted a full accessibility snapshot to check login state; the result exceeded the tool's max output size (89,759 characters) and was rejected, so a full snapshot wasn't usable directly.
4. **`mcp__playwright__browser_find`** (text: `"로그인"`) — found a "로그인" link pointing to `https://nid.naver.com/nidlogin.login`, and the page text **"로그아웃 상태입니다. 로그인하여 이웃새글을 확인해보세요."** ("You are logged out. Log in to see your neighbors' new posts.") — a clear, explicit logged-out signal.
5. **`mcp__playwright__browser_find`** (text: `"내 블로그"`) — no matches, confirming the "내 블로그" / profile-icon cue the skill uses for "already logged in" was absent.
6. **`mcp__playwright__browser_navigate`** → `https://nid.naver.com/nidlogin.login` — landed on the NAVER 로그인 (login) page.
7. **`mcp__playwright__browser_take_screenshot`** → saved as `naver-login-page.png`, then copied into this outputs folder.

At this point the flow reached skill §2, step 2: **"Stop here and tell the user the login page is open, and ask them to log in themselves."** I stopped exactly here, per the explicit test constraint — no ID, password, or 2FA code was entered or even attempted, real or placeholder.

## 3. Exact stopping point

Stopped immediately after confirming the Naver login form was loaded and visible in the browser (`https://nid.naver.com/nidlogin.login`, title "NAVER 로그인"). No further navigation, clicks, or typing were performed on this page.

## 4. Exact message I would show the user

> 네이버 블로그 로그인 페이지를 열어놨어요. 지금 로그아웃 상태라, 직접 아이디/비밀번호(및 2단계 인증이 있다면 그것도)를 입력해서 로그인해 주세요. 로그인 정보는 제가 대신 입력하지 않습니다 — 브라우저 창에서 사용자님이 직접 로그인해 주시면 됩니다. 로그인이 끝나면 "로그인했어" 라고 알려주세요. 그러면 이어서 진행할게요.
>
> (English: I've opened the Naver Blog login page. You're currently logged out — please enter your own ID/password, and complete 2-factor auth if prompted, directly in the browser window. I won't enter your login info for you. Once you're logged in, just let me know and I'll continue.)

Note: since the topic ("이번 여름 휴가철 국내 여행지 추천") and platform (Naver Blog) were already given in the original request, this handoff message does **not** ask for the topic again — it only asks the user to complete login. This matches skill §3, which says to ask for the topic "unless they already gave a topic in their original request."

## 5. Planned next steps once login is confirmed (not executed in this test)

1. **Re-check login** — take a snapshot/find for the "내 블로그" / profile-icon cue to confirm login succeeded before proceeding (skill §2, step 3).
2. **Skip re-asking for topic** — proceed directly using "이번 여름 휴가철 국내 여행지 추천" as the topic, since it was already given.
3. **Open the editor and browse templates** (skill §4) — click "글쓰기" from the user's own blog, open the **템플릿** panel, and look in categories like 여행 (travel) or 정보·노하우 for 2-3 templates whose layout suits a travel-recommendation listicle (e.g. a template with repeated per-destination photo+text blocks). Describe the shortlist to the user and wait for approval before applying one.
4. **Research** (skill §5) — use `WebSearch`/`WebFetch` to pull current, real information on well-regarded domestic (Korean) summer vacation destinations — e.g. coastal areas, mountain valleys/계곡, islands — favoring recent sources for things like festival dates or seasonal conditions, rather than inventing details.
5. **Draft the post** — write a title front-loading a searchable keyword (e.g. "2026 여름휴가 국내 여행지 추천 BEST 5"), a short hook opening, short skimmable paragraphs per destination with `[사진: ...]` placeholders, a conversational -해요/-습니다 tone, a closing wrap-up, and relevant hashtags (e.g. #국내여행 #여름휴가 #휴가지추천).
6. **Type into the editor and 저장 (temp-save) only** — never click 발행 (publish) at this stage; show the user the draft and ask for explicit approval plus a visibility choice (전체공개/이웃공개/서로이웃공개/비공개).
7. **Publish only after approval** — click 발행, set the confirmed visibility (and category/tags if given), confirm, then navigate to the live post to verify it loaded and report back the live URL.

None of steps 1–7 above were executed in this test run — they are the documented next actions only.

## 6. Availability note

Playwright MCP tools (`mcp__playwright__*`) **were available** in this session via `ToolSearch`, so no fallback/simulated description was needed for the browser-driving portion — the login-page navigation and screenshot above are real tool outputs, not fabricated.

## Files in this folder

- `run_summary.md` — this file.
- `naver-login-page.png` — screenshot of the NAVER 로그인 (login) page at `https://nid.naver.com/nidlogin.login`, taken at the exact stopping point.
