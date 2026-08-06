---
name: research-report-docx
description: Researches a given topic on the web and writes up the findings as a formatted .docx report (title page, overview, table of contents, numbered sections, sources), using scripts/create_docx.py's DocBuilder. Use this whenever the user names a topic and wants it researched, summarized, or written up as a document — phrases like "~주제로 조사해줘", "~ 자료조사해서 문서로 정리해줘", "~에 대해 리서치해서 워드파일로 줘", "~ 시장조사 보고서 만들어줘", "research X and write it up", "make me a report on X" — even if they don't say "docx" or "Word" explicitly, since a written research deliverable defaults to this format in this project. Also trigger when the user references the existing GPU market report in research/ as a style example and asks for a similar report on a new topic.
---

# Research Report (docx)

Turn a bare topic into a structured, sourced .docx report saved in `research/` — the same shape as `research/GPU_시장조사_보고서_2026.docx`: title page, overview, table of contents, numbered sections, and a linked source list.

## Why this shape

A research report is only useful if the reader can tell what's in it at a glance (title page + table of contents) and can verify the claims (a real source list, not vibes). The section structure mirrors how an actual analyst would organize findings: context first, then the substantive topic areas, then a synthesis, then receipts. Don't skip the sources section even for a casual request — a report with unlinked or invented claims isn't a report.

## 1. Pin down the topic

Most requests will already be specific enough ("2026년 GPU 시장 동향", "AI 에이전트 프레임워크 비교"). If the topic is genuinely too broad to research in one pass (e.g. just "AI" or "경제"), ask the user to narrow it rather than guessing — a report on an unbounded topic ends up shallow on everything. Don't ask for things you can infer or default:
- **Language**: match the language the user is asking in (default Korean for this project).
- **Depth/length**: default to a mid-depth report (roughly the GPU report's scope — 5-8 content sections, 15-25 sources) unless the user asks for something shorter or a deep-dive.
- **Audience/문서 구분**: default to "참고용" / general reference unless the user specifies (e.g. "교수님께 드릴 보고서").

## 2. Research with WebSearch/WebFetch

Use `WebSearch` to find sources, then `WebFetch` on the promising results to pull real content — don't write from search snippets alone. Aim for breadth across independent sources per major claim, not one article repeated five ways:

- Prefer primary sources and named outlets over aggregator spam.
- Note the publish date of anything time-sensitive (prices, market sizes, product roadmaps) — the reader needs to know how fresh a number is, and figures conflict across research firms often; when they do, say so rather than picking one silently (see the GPU report's "조사기관별로... 편차가 존재" caveat).
- Keep a running list of `(source_title, url)` as you go — you'll need it verbatim for the references section, and reconstructing it after the fact leads to mismatched or dead links.
- If a topic turns out to have little real coverage, say so in the report rather than padding with speculation.

## 3. Outline before writing

Group findings into sections *after* research, not before — let what you actually found determine the structure rather than forcing data into a template decided in advance. A typical shape:

1. 서론 (context: what this report covers and why)
2. — N-2. Topic-specific sections (one per major theme; use level-2 sub-sections like the GPU report's "3.1 NVIDIA" when a section has clear sub-topics)
3. 종합 시사점 및 전망 (synthesis — don't just restate section summaries, connect them)
4. 참고자료 (every source cited, nothing uncited)

Write the 목차 (table of contents) from this final outline, matching heading text exactly — a mismatched TOC is worse than no TOC.

## 4. Build the document

Import `DocBuilder` from `scripts/create_docx.py` (repo root) rather than writing python-docx calls by hand — it already handles the Malgun Gothic / Korean-font quirk, default sizing (40pt title / 20pt body), and main-color theming used across this project's documents.

```python
import sys
sys.path.insert(0, "scripts")
from create_docx import DocBuilder

doc = DocBuilder(title="그래픽카드(GPU) 시장조사 보고서", main_color="1F4E79")
doc.add_subtitle("2026년 최신 동향 분석")
doc.add_metadata([
    "작성일: 2026년 8월 6일",
    "문서 구분: 참고용",
])
doc.add_divider()

doc.add_heading("[개요]", level=1)
doc.add_paragraph("본 보고서는 ...")

doc.add_heading("[목차]", level=1)
doc.add_paragraph("1. 서론\n2. 시장 규모 및 성장 전망\n3. 주요 기업 동향\n   3.1 NVIDIA\n...")

doc.add_divider()
doc.add_heading("1. 서론", level=1)
doc.add_paragraph("...")

doc.add_heading("3. 주요 기업 동향", level=1)
doc.add_heading("3.1 NVIDIA", level=2)
doc.add_paragraph("...")

doc.add_references([
    ("NVIDIA Q2 FY26 Earnings Release", "https://..."),
    ("Tom's Hardware, \"Desktop GPU roadmap\"", "https://..."),
])

doc.save("research/GPU_시장조사_보고서_2026.docx")
```

Available `DocBuilder` methods relevant here: `add_title` (set via constructor), `add_subtitle`, `add_metadata` (small centered info lines), `add_divider` (section separator rule), `add_heading(level=1|2|3)`, `add_paragraph`, `add_bullet_list`/`add_numbered_list`, `add_table`, `add_references` (numbered, real clickable hyperlinks), `add_page_break`. Section numbers ("1.", "3.1") are literal text you write into the heading — the builder doesn't auto-number.

If the user asks for a specific brand/main color, pass it as `main_color="RRGGBB"` to the constructor; otherwise the script's default (`1F4E79`) is fine.

## 5. Save and report back

Save to `research/<주제>_조사_보고서.docx` (Korean topic in the filename, matching the existing `GPU_시장조사_보고서_2026.docx` naming), creating the `research/` folder if needed — `DocBuilder.save()` already creates parent directories.

After saving, tell the user in chat: the file path, a 2-3 sentence summary of what the report covers, how many sources were used, and flag anything the research came up thin on. Don't dump the full report text into the chat — the .docx is the deliverable.

## Edge cases

- **Topic has almost no reliable coverage**: say so explicitly in both the 서론 and the chat summary rather than stretching thin material into a full report.
- **Conflicting figures across sources**: report the range and cite both, don't silently pick one (see §2).
- **User provides their own source material** instead of asking for web research: skip WebSearch, build the report structure from what they gave you, and note in 서론 that it's based on user-provided material rather than independent research.
- **User wants a non-Korean-language report**: keep the same structure but translate section headers/labels too (e.g. "Overview" instead of "[개요]"), not just the body text.
