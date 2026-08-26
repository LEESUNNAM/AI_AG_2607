---
name: design-concept
description: Takes a bare topic (a product, brand, page, or app idea) and turns it into a researched web/app UI design concept — mood direction, color palette with hex values, typography, layout/UI pattern notes, and cited reference sites — saved as a Markdown document. Use this whenever the user gives a topic and wants a design concept, mood direction, or visual direction worked out before or without a full proposal — phrases like "~ 주제로 디자인 컨셉 잡아줘", "~ 앱 UI 컨셉 조사해줘", "이 주제 어떤 스타일/무드로 디자인하면 좋을지 리서치해줘", "give me a design concept for X", "what color palette and style would fit X" — even if they don't say "디자인 컨셉" explicitly, as long as they want a visual/style direction grounded in real research rather than a guess off the top of the head. This skill does its own topic research from scratch (no prior research file needed) and produces ONLY the design-concept portion — mood, palette, type, layout, references. Do NOT use this when the user wants a full web design proposal with personas, 정보구조도(sitemap), page-by-page wireframes, and a timeline — that heavier, full-proposal job belongs to the 웹 기획자 agent, which already includes a design-concept section as one part of a larger document built from existing research. If the user already has company/topic research in hand and wants the complete proposal, prefer 웹 기획자 instead of this skill.
---

# Design Concept

Turn a bare topic into a grounded design concept: a short concept statement, a color palette, type pairing, and layout/UI direction — each one traceable back to something real (a trend, a competitor, a cited reference site), not invented from vibes.

## Why this shape

A design concept that isn't backed by anything is just a color guess. The value of this skill is doing the trend/reference legwork first and then deriving the palette, type, and layout choices from what actually turned up — so every recommendation in the final document has a "because" behind it (a cited site, an observed trend, a property of the topic itself). This is a lighter, faster deliverable than a full web design proposal (see `웹 기획자` agent for that) — it skips personas, sitemap, wireframes, and timeline, and focuses entirely on the visual/style direction.

## 1. Pin down the target

Most requests already imply enough to proceed. Infer what's missing rather than interrogating the user, but state the assumption in the final document's overview line:
- **What kind of screen**: a marketing/landing page, a full site, a mobile app, a dashboard, etc. Default to "웹사이트" (a general site/landing page) if genuinely unstated.
- **Audience/tone hint**: pull this from the topic itself where possible (e.g. "키즈 교육 앱" implies a playful, high-contrast, large-touch-target direction; "법률 자문 서비스" implies a trust-first, restrained direction). Don't force a generic "clean and modern" tone onto every topic — the topic almost always suggests *something* more specific than that.
- **Language**: match the language the user asked in (default Korean for this project).

## 2. Research trends and references with WebSearch

Use `WebSearch` (and `WebFetch` on promising results) to ground the concept in things that actually exist right now, not in stale textbook design advice:

- Search for current design trends relevant to the topic's category (e.g. "2026 fintech app UI trends", "sustainable beauty brand web design 2026").
- Search for 3-5 real reference sites/apps in the same or an adjacent category that are well-regarded for their design — design gallery/award sites (Awwwards, CSS Design Awards, GDWEB/지디웹 for Korean-market references) and design write-ups are good sources. Verify each one is real; never fabricate a site, URL, or award.
- For each reference, note what it specifically does well and *why it's relevant to this topic* — tie it to a concrete, observable feature (e.g. "warm duotone photography + serif headlines signal an artisanal, non-mass-market feel"), not generic praise like "clean design."
- Keep a running `(name, url)` list as you go for the sources section — reconstructing it afterward leads to mismatched links.

If the topic is niche enough that trend/reference coverage is thin, say so in the document rather than padding with invented examples.

## 3. Derive the concept from the research

Don't pick a concept keyword first and then search for evidence to fit it — let the research (trend signals + the topic's own nature: audience, mission, category conventions or a deliberate break from them) determine the direction. A concept is usually expressible as:
- **1-2 mood/keyword phrases** (e.g. "Warm Minimalism", "Bold & Playful", "Quiet Confidence") — in both English and Korean if the doc is Korean-facing.
- **A one-paragraph rationale** connecting the keywords to specifics from the topic and research (not a dictionary definition of the keyword).

## 4. Build out the concrete design decisions

From the concept, work out:

- **Color palette**: primary, secondary, accent, and neutral/background colors, each as a hex value, with a one-line rationale per color (what it signals, where it's used). 4-6 colors is usually enough — resist padding the palette just to fill a table.
- **Typography**: a heading/body font pairing (real, available typefaces — e.g. Google Fonts, or Korean web-safe fonts like Pretendard/Noto Sans KR when the doc is Korean-facing), with a short rationale for the pairing.
- **Layout / UI pattern notes**: grid density (spacious vs. dense), navigation style (top nav, sidebar, tab bar for apps), key component conventions worth following or deliberately breaking (card-based, full-bleed imagery, bento grid, etc.), and how the layout should adapt across mobile/tablet/desktop at a high level (not full wireframes — that level of detail belongs to a full proposal, not this document).
- **Imagery / iconography direction**: photography vs. illustration vs. 3D, color treatment (duotone, high-saturation, muted), icon style (line vs. filled vs. custom).
- **Motion/interaction feel** (optional, keep light): a sentence or two on the general interaction feel (snappy micro-interactions vs. minimal motion) only if it's relevant to the concept — don't manufacture a motion section for a static print-style piece.

## 5. Write and save the document

Structure the Markdown document as:

1. Overview — topic, inferred target/screen type, any assumptions stated in step 1
2. Trend & Reference Research — summarized findings, plus the 3-5 reference sites with rationale and links
3. Design Concept Statement — the keyword(s)/phrase and the rationale paragraph
4. Color Palette — table or list of hex values with rationale
5. Typography — the pairing and rationale
6. Layout & UI Patterns
7. Imagery & Iconography
8. Motion/Interaction Notes (only if relevant)
9. Sources — every reference/trend source cited, nothing uncited

Save as a matched English/Korean pair, following this project's convention for new documents (see `web-design-proposal/` for the same pattern used by the 웹 기획자 agent):
- English original (Markdown): `design-concept/<topic>/en/<topic>_design_concept.md`
- Korean translation (plain text, same section content, not a summary): `design-concept/<topic>/ko/<topic>_design_concept.txt`

If the user asked in Korean, write the English version first anyway (per this project's rule that `.md` files stay in English), then produce the full Korean `.txt` translation alongside it. Keep both files' section structure and content identical. If asked to revise later, update both together so they don't drift.

After saving, report back in chat: both file paths, the concept keyword(s) in one line, and how many reference sites were used and from where. Don't paste the full document into chat — the two files are the deliverable.

## Constraints

- Never fabricate reference sites, URLs, awards, or trend claims. If coverage is thin, say so rather than inventing examples to fill the reference list.
- Don't default to generic "clean, modern, minimal" for every topic — derive the direction from what's actually distinctive about this topic and what the research turned up. If two different topics would get the same concept description, the concept isn't specific enough yet.
- This skill produces the design-concept portion only. If the user's request grows into wanting personas, a full sitemap, page-by-page wireframes, or a timeline, say that's a larger deliverable and point to the 웹 기획자 agent rather than trying to expand this document to cover it.
- Every color, font, and layout recommendation should have a stated reason. A palette or type pairing with no rationale line is a guess, not a concept.
