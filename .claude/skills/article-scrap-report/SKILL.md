---
name: article-scrap-report
description: Uses the Playwright MCP browser tools to scrape one or more articles (navigate, read the content, save a screenshot), then analyzes the scraped material into a python-docx report and/or a python-pptx slide deck built with scripts/create_docx.py's DocBuilder and scripts/create_pptx.py's PptxBuilder. Use this whenever the user wants an article (or several) captured from the web and turned into a written report or presentation — phrases like "이 기사 스크랩해서 보고서로 만들어줘", "네이버 뉴스 기사들 모아서 발표자료 만들어줘", "이 페이지 캡처해서 분석 문서로 정리해줘", "scrape this article and write it up", "turn these news articles into a deck" — even if they only ask for the scrape first and mention the report/deck later in the same thread. Also trigger when the user is mid-session already browsing articles via Playwright MCP (as in "5번째 기사 스크린샷 찍어줘" earlier in a conversation) and then asks for a summary, report, or presentation built from what was captured.
---

# Article Scrap Report

Turn one or more web articles into a screenshot-backed archive plus (on request) a written report and/or slide deck. The pipeline has three stages that are useful independently but compound well together: **scrape** (Playwright MCP navigates and screenshots), **analyze** (read the actual article text, not just the screenshot), and **produce** (docx report and/or pptx deck, whichever the user actually asked for).

## Why this shape

A screenshot alone documents that an article existed and what it looked like, but it isn't analyzable prose — the report/deck needs real extracted text (headline, byline, body, key figures) to summarize accurately and quote correctly. Skipping straight from screenshot to "write a report" produces a report that either hallucinates content or just describes the screenshot. Always read the page content before writing anything about it.

## 1. Pin down what to scrape

This skill is site-agnostic — don't assume a fixed source. Figure out the target from the request or the conversation:

- If the user gives a URL or names a site/section, navigate there directly.
- If the user is already mid-session on an article (e.g. they just had you browse to it with Playwright MCP), use that page — don't re-navigate from scratch.
- If they want multiple articles (a topic, a list, "이 5개 기사"), scrape each one in turn; keep the list explicit so nothing gets dropped when you move to the analysis stage.
- If the target is genuinely ambiguous (no URL, no site named, no prior browsing in this session), ask rather than guessing a site.

Also confirm — if not already obvious from the request — which deliverable(s) they want: **just the scrape/screenshots**, a **docx report**, a **pptx deck**, or both. Don't build a deliverable nobody asked for; it's wasted work and something to review that wasn't wanted.

## 2. Scrape with Playwright MCP

Load the Playwright MCP tools if not already loaded (`ToolSearch` with `select:mcp__playwright__browser_navigate,mcp__playwright__browser_snapshot,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_click`, adding others as needed). For each article:

1. `browser_navigate` to the article (or click through from a listing page, same as browsing normally).
2. `browser_snapshot` (not just a screenshot) to get the actual accessibility-tree text — this is what you'll read for the headline, byline, publish date, and body text. A screenshot is a picture; the snapshot (or `get_page_text` if using claude-in-chrome instead) is what you can actually analyze.
3. `browser_take_screenshot` with `fullPage: true` so the capture is a complete visual record, not just the first viewport.

**Save screenshots to `output2/playwright/<topic-slug>/`** — this project's CLAUDE.md requires all Playwright MCP output to live under `output2/playwright`; nest it under a topic-slug subfolder (e.g. `output2/playwright/ai-반도체-동향/기사1.png`) so a multi-article scrape doesn't dump loose files next to unrelated captures. Pick the topic-slug from the user's subject/request, transliterated to something filesystem-safe.

Record, per article, as you go: title, source/outlet, URL, publish date if shown, the body text you read, and the screenshot path. You'll need all of it in the next stage — don't rely on re-reading the snapshot later, since the page may have moved on (infinite scroll, ads rotating, session timeout).

## 3. Analyze

Once every article is scraped, read back over what you collected before writing anything:

- What's the actual story/claim in each article — not just the headline.
- Where articles overlap or disagree (multiple articles on one topic often cite different numbers or angles — note the discrepancy rather than silently picking one, same principle as this project's research-report skills).
- What's genuinely worth reporting vs. incidental (ads, unrelated sidebar links, cookie banners captured incidentally in the screenshot aren't content).

This analysis is what turns a folder of screenshots into a report — the outline for step 4/5 should come from what you actually found, not a template imposed in advance.

## 4. Build the docx report (if requested)

Import `DocBuilder` from `scripts/create_docx.py` (repo root) — same builder this project's research-report-docx skill uses, so reports stay visually consistent across the project. See that skill for full method docs; the shape for a scrape-based report is simpler than a full market report:

```python
import sys
sys.path.insert(0, "scripts")
from create_docx import DocBuilder

doc = DocBuilder(title="<주제> 기사 스크랩 분석", main_color="1F4E79")
doc.add_subtitle("스크랩 일자: 2026년 8월 12일")
doc.add_divider()

doc.add_heading("[개요]", level=1)
doc.add_paragraph("이 문서는 스크랩한 N건의 기사를 분석한 내용입니다...")

doc.add_heading("1. <기사 제목>", level=1)
doc.add_paragraph("출처: <매체명> | 원문: <URL>")
doc.add_paragraph("<핵심 요약 및 분석>")
# repeat per article, or group by theme if articles cluster around one topic

doc.add_heading("종합", level=1)
doc.add_paragraph("<기사들을 종합했을 때의 시사점>")

doc.add_references([("<기사 제목> (<매체명>)", "<원문 URL>") for each article])
doc.save(f"output2/reports/<topic-slug>/<주제>_스크랩_분석.docx")
```

Embedding a screenshot inline isn't a built-in `DocBuilder` method — if the user wants the actual screenshot images in the docx (not just the analysis), add it with raw python-docx (`doc.document.add_picture(path, width=Inches(6))`) after `doc.document` is accessible; ask if unclear whether they want images inline or just cited by path.

## 5. Build the pptx deck (if requested)

Import `PptxBuilder` from `scripts/create_pptx.py` (repo root) — a widescreen (16:9), Korean-font-safe deck builder matching this project's other document scripts' color theming.

```python
import sys
sys.path.insert(0, "scripts")
from create_pptx import PptxBuilder

deck = PptxBuilder(main_color="1F4E79")
deck.add_title_slide("<주제> 기사 스크랩 브리핑", subtitle="2026년 8월 12일 기준")

deck.add_section_slide("1. <기사 제목 또는 테마>")
deck.add_content_slide("핵심 요약", ["요약 포인트 1", "요약 포인트 2", "요약 포인트 3"])
deck.add_image_slide("스크린샷", "output2/playwright/<topic-slug>/기사1.png", caption="출처: <매체명>, <URL>")
# repeat per article/theme

deck.add_content_slide("종합 시사점", ["...", "..."])
deck.save(f"output2/reports/<topic-slug>/<주제>_브리핑.pptx")
```

Available `PptxBuilder` methods: `add_title_slide`, `add_section_slide` (full-bleed divider), `add_content_slide(title, bullets, notes=None)`, `add_image_slide(title, image_path, caption=None)` (auto-scales and centers the image), `add_table_slide(title, headers, rows)`, `add_quote_slide(quote, attribution=None)` (good for pulling a striking line straight from an article). Keep one article or theme per section rather than cramming everything onto one slide — a deck is skimmed, not read line by line.

## 6. Save locations and reporting back

- Screenshots: `output2/playwright/<topic-slug>/` (per this project's standing Playwright MCP rule).
- docx/pptx deliverables: `output2/reports/<topic-slug>/` — kept separate from the raw screenshots so the finished deliverables aren't mixed in with capture artifacts.

After saving, tell the user in chat: which files were produced and their paths, how many articles were covered, and a 2-3 sentence summary of the content — not the full report/deck text. If any article failed to scrape (login wall, removed, JS error), say so explicitly rather than silently omitting it from the output.

## Edge cases

- **Paywalled or login-required article**: say so and ask whether to proceed with what's visible (headline/summary only) or skip it — don't attempt to bypass a login wall.
- **User only wants the scrape, no report**: stop after step 2; don't build documents nobody asked for.
- **Single article vs. many**: the pipeline is the same either way, but for a single article `add_section_slide`/multiple docx headings are usually overkill — one content slide and one docx section is enough; use judgment on scale.
- **User wants the screenshots embedded in the docx**, not just cited: see the note at the end of step 4.
- **Articles conflict or one is clearly biased/opinion vs. news**: note the distinction in the analysis rather than blending everything into one flat summary.
