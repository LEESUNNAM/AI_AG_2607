---
name: tistory-blog-writer
description: Researches a topic and writes it up as a Tistory blog post — logs into the user's Tistory account via the claude-in-chrome browser extension, drafts the post, saves it as a temporary draft (임시저장), and asks the user to approve and choose 공개(public)/비공개(private) before actually publishing. Use this whenever the user wants a topic turned into a blog post on their Tistory — phrases like "~주제로 티스토리에 글 써줘", "블로그에 포스팅해줘", "이 내용 블로그에 올려줘", "~조사해서 내 블로그에 글로 작성", "티스토리에 발행해줘" — even if they don't say "티스토리" explicitly, since Tistory is this user's blog platform. Also trigger for requests to edit, unpublish, or change the visibility (공개/비공개) of an already-published Tistory post.
---

# Tistory Blog Writer

Turn a topic into a researched Tistory post, end to end: research → draft → login handoff → type into the Tistory editor → save as a draft → get the user's explicit go-ahead (and their public/private choice) → publish. The order matters — nothing goes live until the user has seen the draft and said so.

## Why this shape

Publishing to a real, public blog is a one-way door — once it's live, anyone can read it, and it can get indexed and shared before you'd notice a mistake. That's why this skill always stops at a draft and asks, rather than researching-then-publishing in one motion. It also means Claude never touches the user's Kakao/Tistory password: login is a deliberate handoff point, not a gap to work around. Treat both of these as load-bearing, not optional politeness.

## 1. Load the browser tools

If `mcp__claude-in-chrome__*` tools aren't loaded yet, load the core set in one `ToolSearch` call (see the claude-in-chrome skill/instructions for the exact query) before doing anything else. Then call `tabs_context_mcp{createIfEmpty: true}` to get a tab to work in.

## 2. Research the topic

Default to `WebSearch`/`WebFetch` for research — it's faster and doesn't burn screenshots on search result pages. Pull real content from promising results rather than writing from snippets alone (the same standard as the research-report skills in this project). Only fall back to researching via the Chrome browser itself (Google search + `get_page_text` on articles) if the user specifically asks for it, or if WebSearch isn't available.

- Aim for 3-5 independent, real sources for a topical roundup — enough to have something to say per section, not so many the post turns into a link dump.
- Note publish dates on anything time-sensitive; if sources disagree, say so rather than silently picking one.
- If the topic is too broad to research meaningfully in one pass (e.g. just "AI"), ask the user to narrow it before you start, the same way you would for a written report — a blog post on an unbounded topic ends up shallow.

## 3. Draft the post

Blog posts read differently from formal reports — write for a reader skimming a feed, not an analyst:

- **Title**: concrete and specific (include the topic and, for time-sensitive roundups, the date range), not a generic label.
- **Opening**: a short, conversational hook (1-2 sentences) that tells the reader what they're about to get and why it's worth their time — not a dry "this report covers...".
- **Body**: one section per major finding/theme, each with its own short heading (e.g. "1. ...", "2. ..."). Write in an approachable, first-person register (-습니다/-해요 tone in Korean) rather than formal report prose. Keep paragraphs short — 3-5 sentences each is plenty for a blog reader.
- **Closing**: a brief wrap-up that ties the sections together and, where relevant, notes what to watch next — not a restated list of the sections above.

Match the language the user is writing in (default Korean for this project). Don't fabricate sources or stats — if research came up thin on some point, say so plainly rather than padding.

## 4. Get into Tistory — hand off login to the user

Navigate to `tistory.com`. Check whether the account is already logged in (a "글쓰기" button and profile icon in the header means yes — skip straight to §5). If not:

1. Click through to the login flow (e.g. "카카오계정으로 시작하기").
2. **Stop here and tell the user the login page is open.** Entering an account password is something Claude must never do (this holds even if the user offers to share credentials) — the user has to type their own ID/password into the Kakao login form.
3. Wait for the user to say they're done, then screenshot to confirm login succeeded (same header cue as above) before moving on. If it's ambiguous, ask rather than assuming.

## 5. Open the post editor

Find the "글쓰기"/"쓰기" link on the logged-in Tistory homepage (via `find`) rather than guessing or hardcoding a blog subdomain — it resolves to the actual logged-in user's blog (`https://<their-subdomain>.tistory.com/manage/newpost`). Click it or navigate there directly once you have the URL. Remember the resolved blog subdomain — you'll need it again in §7 if the user asks to edit or change visibility later in the same session.

## 6. Type the post and save as a draft — never skip this

Click the title field, type the title, tab/click into the body, type the full post (a single `type` action with `\n\n` between paragraphs works fine in the Tistory editor). Leave the category as-is ("카테고리 없음") unless the user has told you which category to use.

Click **임시저장** (temporary save). Do not click 완료/발행 yet, even if the user's original request said "발행해줘" — the draft-then-approve gate applies regardless of how the request was phrased, because the user hasn't seen the actual text yet.

## 7. Ask for approval and publish

Tell the user the draft is saved and ask them to confirm before it goes live. If they haven't already told you 공개(public) or 비공개(private), ask — this is a real consequence (anyone can read a public post) so don't default it silently. Once you have both a yes and a visibility choice:

1. Click **완료** to open the 발행 dialog.
2. Select the matching radio button (공개 / 공개(보호) / 비공개) — the submit button's label changes to match ("공개 발행" / "비공개 저장" / etc.), which is a good confirmation you selected the right one before clicking it.
3. Click the submit button.
4. Report back the result and, if it went public, the post's live URL.

**Changing visibility on an already-published post** (a common follow-up): navigate to `https://<blog-subdomain>.tistory.com/manage/post/<id>` (the numeric ID is visible in the post's own URL or the 글 관리 list), click **완료** to reopen the same 발행 dialog, switch the radio button, and save. Same dialog, same flow as initial publish — no need to re-draft the content.

## Edge cases

- **User provides their own material instead of asking for research**: skip web research, build the post from what they gave you, and don't invent additional claims to pad it out.
- **User explicitly says "그냥 바로 발행해"** (skip the approval step): still save a draft first and show them the title + a short summary of the sections before publishing — the point of the gate is that mistakes in a live post are hard to undo, not procedural friction, so don't skip the confirmation itself even if they say to skip the draft step.
- **Multiple Tistory blogs on one account**: if more than one "내 블로그" appears, ask which one before opening the editor rather than guessing.
- **Login session expires mid-task**: if a navigation unexpectedly lands back on a login page, stop and hand off to the user again rather than retrying blindly.
