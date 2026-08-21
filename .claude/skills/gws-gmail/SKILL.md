---
name: gws-gmail
description: Drafts an email based on the user's request and saves it as a real Gmail draft using this project's GWS CLI tool (scripts/gws_gmail_draft_create.py), then only sends it (scripts/gws_gmail_draft_send.py) after the user explicitly approves — never sends on the first pass. Use this whenever the user asks to write, draft, or send an email/메일/이메일 — phrases like "~한테 메일 하나 써줘", "이 내용으로 이메일 작성해줘", "answer 정중하게 메일 보내줘", "write an email to X about Y" — even if they say "보내줘" (send) outright, since this skill always drafts first and confirms before the actual send step. Also trigger for follow-up requests to revise a draft this skill already created, or to finally send one that's been sitting pending approval.
---

# GWS Gmail (draft → approve → send)

Turn a request into a real Gmail draft first — never send in the same step the user asks for the email. Sending is the one action here a person outside this conversation actually receives; everything before that (drafting, revising) is safe and reversible, so keep as much of the work as possible on that side of the line.

## Why draft-then-approve, always

Even if the user's request sounds like "그냥 보내줘" (just send it), you don't yet know the email is right until they've seen the actual text — recipient, tone, and facts are all things a first draft can get wrong. Creating a Gmail draft costs nothing (it just sits in their Drafts folder, visible in their own Gmail too), while sending a wrong or premature email to someone else is hard to take back. So the flow is always: draft → show the user → get explicit approval → send. Don't skip the approval step even for a short, low-stakes-sounding email.

## 1. Gather what the email needs

Ask for whatever isn't already clear from the request: recipient email address(es), subject (or infer a reasonable one from the purpose), and the key points/purpose. Match the tone to context — default to polite/professional Korean (존댓말) unless the user's own request or the recipient relationship implies otherwise. Don't invent factual claims the user didn't give you (dates, figures, commitments) — ask rather than guess.

## 2. Create the draft (safe — doesn't send)

Write the body to a temp file, then from the repo root:

```bash
python scripts/gws_gmail_draft_create.py --to "받는사람@example.com" --subject "제목" --body-file <path> [--cc "참조@example.com"]
```

This prints `draftId: <id>` — keep track of it, you'll need it in step 4. This step only writes to the user's Drafts folder; nothing is emailed yet.

## 3. Show the draft and get explicit approval

Paste the drafted subject + body into the chat (don't make the user open Gmail just to see what you wrote) and ask clearly whether to send it. Look for an unambiguous go-ahead — "보내줘", "전송해줘", "이대로 보내" — before proceeding. A vague positive reaction ("좋아", "고마워") isn't necessarily approval to send; if it's not clear whether they mean "looks good, send it" or just "thanks for drafting," ask directly: "지금 바로 전송할까요?"

If the user asks for changes instead, don't try to edit the existing draft in place — just create a new draft with the revised content (repeat step 2) and treat its `draftId` as the current one; the old draft can just sit unused in Drafts. If the user decides not to send at all, stop here — leaving an unsent draft in their Drafts folder is a perfectly fine outcome, not a failure to clean up.

## 4. Send only on approval

```bash
python scripts/gws_gmail_draft_send.py --draft-id <id-from-step-2>
```

This delivers the draft's current content immediately — only run it once you have that explicit go-ahead from step 3.

## 5. First-time auth

Both scripts share a compose-scoped token (`credentials/gws_gmail_compose_token.json`, scope `gmail.compose`) separate from the plain `gmail.send` token used elsewhere in this project — drafting and sending need read/write access to Drafts, which `gmail.send` alone doesn't grant. On first use, either script opens a browser for OAuth consent — run via Bash with `run_in_background: true`, tell the user a browser approval is needed, and pick up the result from the background task output once it completes.

## 6. Report back

After sending, confirm to the user: recipient(s), subject, and that it was sent (the `messageId` printed is your evidence). If it's still just a pending draft (not yet approved), say so plainly rather than implying it already went out.

## Edge cases

- **Multiple recipients**: pass a comma-separated list to `--to` (or use `--cc` for CC-only recipients) — Gmail accepts either in the same header.
- **User wants only a draft, no send at all** ("초안만 만들어줘"): stop after step 2, don't ask about sending.
- **User asks to send something drafted earlier in the conversation**: reuse that `draftId` if you still have it rather than recreating the draft; if you've lost track of it, just create a fresh draft with the same content and send that one.
- **Ambiguous or missing recipient**: never guess an email address — ask.
