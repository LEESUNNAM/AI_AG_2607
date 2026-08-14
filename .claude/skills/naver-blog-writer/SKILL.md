---
name: naver-blog-writer
description: Writes and publishes a post to the user's own Naver Blog (네이버 블로그), driving the browser with the Playwright MCP tools so the user can watch every step happen live. ALWAYS use this skill when the user types the keyword "블로그 글 작성", or otherwise clearly asks to write a Naver Blog post — phrases like "네이버 블로그에 글 써줘", "네이버 블로그 포스팅해줘", "이 주제로 블로그 글 하나 작성해줘", "블로그에 이거 올려줘" (when Naver Blog is the platform in context). This is distinct from the tistory-blog-writer skill, which handles the user's Tistory blog instead — if the target platform is genuinely ambiguous, ask which blog before starting rather than guessing. The full flow: open Naver Blog via Playwright MCP and hand login off to the user, ask for the post topic once logged in, search the editor's built-in template panel for a fitting template and get the user's approval, research the topic and draft body copy in current Naver Blog style, save it as a temporary draft (임시저장) and get explicit user approval, then publish and open the live post. Trigger this whenever the user wants an actual post created on their Naver Blog — not for general web research or for writing a docx/pptx report about a topic.
---

# Naver Blog Writer

Turn a topic into a published Naver Blog post, end to end: login handoff → topic → template → research → draft → temp-save → approval → publish. The order matters — nothing goes live until the user has seen the actual draft and said so, and every browser action happens in a visible window the user can watch, not off-screen.

## Why this shape

Publishing to a real, public blog is a one-way door — once it's live, it can be read, indexed, and shared before a mistake would even be noticed. That's why this skill always stops at a draft and asks, rather than researching-then-publishing in one motion. It also means Claude never touches the user's Naver password: login is a deliberate handoff point, not a gap to script around. And because the whole point of the user's request was to *watch this happen*, everything runs through Playwright MCP's visible browser rather than a headless or background session — treat all three of these as load-bearing, not optional politeness.

## 1. Load the browser tools

Load the Playwright MCP tools if not already loaded (`ToolSearch` with `select:mcp__playwright__browser_navigate,mcp__playwright__browser_snapshot,mcp__playwright__browser_click,mcp__playwright__browser_type,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_find`, adding others as needed). Playwright MCP opens a real, visible browser window by default — don't add any headless flag or option that would hide it, since the user watching the progress unfold is the point of using this tool over a background API call.

## 2. Get into Naver Blog — hand off login to the user

Navigate to `https://blog.naver.com` (or straight to `https://nid.naver.com/nidlogin.login` if you already know login is needed). Take a snapshot to check whether the account is already logged in — a profile icon / "내 블로그" link in the header means yes, so skip straight to §3. If not logged in:

1. Land on or click through to the Naver login form.
2. **Stop here and tell the user the login page is open, and ask them to log in themselves.** Entering an ID or password (and any 2-factor step) is something Claude must never do, even if the user offers to share credentials — the user types their own credentials into the Naver form.
3. Wait for the user to say they're done, then snapshot again to confirm login succeeded (same header cue as above) before moving on. If it's ambiguous, ask rather than assuming.

## 3. Ask for the post topic

Once logged in, ask the user what the post should be about, unless they already gave a topic in their original request. If the topic is too broad to write something substantive about (e.g. just "여행"), ask them to narrow it — same reasoning as any research-driven write-up in this project: an unbounded topic produces a shallow post.

## 4. Find and recommend a template

Open the post editor (the "글쓰기" button, typically reachable from the user's own blog homepage or the header). In the editor, open the **템플릿** panel in the sidebar — this is Naver's built-in library of post layouts, grouped by category (e.g. 이야기, 정보·노하우, 리뷰, 맛집, 여행 등). Browse the categories that fit the topic and pick 2-3 templates whose structure genuinely suits it (a 리뷰 template for a product post, an 정보·노하우 template for a how-to, and so on) rather than defaulting to the first one in the list.

Describe the shortlisted templates to the user (name/category and what their layout emphasizes) and ask them to approve one, or say they'd rather write without a template. Don't apply a template the user hasn't approved — it changes the whole structure of what you write next.

## 5. Research and draft the body

Default to `WebSearch`/`WebFetch` for research on the topic itself — it's faster and doesn't burn screenshots on search result pages. Pull real content from promising results rather than writing from snippets alone. Aim for enough independent sources to have something real to say in each section; if the topic is more personal/experiential than research-driven (e.g. a travel diary), lean on what the user has told you instead of inventing sourced claims.

Write for how Naver Blog is actually read today, not like a formal report:

- **Title**: concrete and specific, ideally front-loading the keyword someone would search for — Naver's own search and recommendation surfaces reward a title that plainly states what the post is about over a clever-but-vague one.
- **Opening**: 1-2 short sentences that hook the reader immediately — Naver's mobile feed shows only the first line or two as a preview, so don't bury the point three sentences in.
- **Body**: short paragraphs (2-4 sentences), broken up with subheadings or numbered sections for anything with more than one distinct point, and a natural (not stuffed) repetition of the topic's key terms throughout — this is both easier to skim on mobile and how Naver's own ranking rewards a post that clearly, consistently covers its stated topic. Note in the text where a photo would naturally go (e.g. "[사진: ...]") if the post is the kind that normally carries images, since you can't upload images yourself in this flow unless the user provides files.
- **Tone**: conversational, first-person (-습니다/-해요 register), like a blog rather than a memo.
- **Closing**: a short wrap-up, and a line of relevant hashtags if the template/category conventions call for them (common on Naver Blog, e.g. review/맛집 posts).

If a chosen template has its own section placeholders, write into those rather than ignoring the structure you just got approved.

## 6. Type the post and save as a draft — never skip this

Click into the title field and type the title, then the body (a single `type` action with blank lines between paragraphs is fine). Click **저장** (temporary save — this is the equivalent of Tistory's 임시저장). Do not click **발행** yet, even if the user's original request said to publish outright — the draft-then-approve gate applies regardless of phrasing, because the user hasn't seen the actual text yet.

## 7. Ask for approval and publish

Tell the user the draft is saved and ask them to confirm before it goes live. Naver Blog's publish dialog offers finer-grained visibility than just public/private — 전체공개, 이웃공개, 서로이웃공개, 비공개 — so if the user hasn't already told you which one, ask; don't default it silently, since who can read the post is a real consequence. Once you have both a yes and a visibility choice:

1. Click **발행** to open the publish dialog.
2. Select the matching 공개 설정 option, and set category/태그 if the user specified any.
3. Click the final publish/confirm button in that dialog.
4. Navigate to the published post and confirm it loaded, then report back the result and the post's live URL — this satisfies "open the saved page" as well as giving the user something to click.

## Edge cases

- **User provides their own material instead of asking for research**: skip web research, build the post from what they gave you, and don't invent additional claims to pad it out.
- **No template feels like a good fit**: say so and offer to write without one rather than forcing a mismatched template on the topic.
- **User explicitly says "그냥 바로 발행해"** (skip the approval step): still save a draft first and show them the title + a short summary before publishing — the point of the gate is that a mistake on a live post is hard to undo, not procedural friction, so don't skip the confirmation itself even if they say to skip the draft step.
- **Login session expires mid-task**: if a navigation unexpectedly lands back on a login page, stop and hand off to the user again rather than retrying blindly.
- **User asks to edit or change visibility on an already-published post**: navigate to the post's own management/edit view (reachable from 내 블로그 → 글 관리, or directly by the post's URL), make the change, and save the same way — no need to re-run the whole topic/template/draft flow from scratch.
