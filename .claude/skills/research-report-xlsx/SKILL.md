---
name: research-report-xlsx
description: Turns a bare topic into a researched, table-first .xlsx workbook, or takes an existing .xlsx/.csv file the user references and analyzes/reformats it into a new .xlsx — both paths built on scripts/create_xlsx.py's SheetBuilder/format_workbook/load_and_format, which auto-add an ID column, bold headers, italic quotes, a normalized 10pt body font, and growth/comparison charts. Use this whenever the user names a topic and wants it researched into a spreadsheet — phrases like "~주제로 조사해서 엑셀로 줘", "~ 자료조사해서 xlsx로 정리해줘", "~ 비교표 만들어줘", "~ 시장 데이터 스프레드시트로 줘", "research X and put it in a spreadsheet" — even without saying "excel" or "xlsx" explicitly, whenever a table/spreadsheet deliverable fits better than prose (rankings, comparisons, year-over-year numbers). Also trigger whenever the user references a specific existing .xlsx or .csv file and asks to analyze it, clean it up, format it, add a chart, or turn it into a report — phrases like "이 엑셀 파일 분석해줘", "이 csv 파일로 표 만들어줘", "다운로드 폴더에 있는 파일 정리해서 새 파일로 줘", "add a chart to this spreadsheet", "clean up this xlsx". Do not trigger for prose-only research requests where a Word document is wanted (use research-report-docx instead) or for Canva/visual design requests.
---

# Research Report (xlsx)

Produce a formatted, sourced `.xlsx` workbook — either from a bare topic (research mode) or from an existing spreadsheet file the user points at (analysis mode). Both modes go through `scripts/create_xlsx.py` (repo root), which already solves Korean-font rendering, ID-column insertion, header/quote/body styling, and auto-charting for growth or comparison data, so don't hand-roll openpyxl calls for those.

## Why this shape

A spreadsheet deliverable is only useful if a reader can scan it fast (a numbered ID column, bold headers) and trust the numbers (real sources, correctly-scaled percentages, a chart when there's a trend worth seeing at a glance). `create_xlsx.py`'s `SheetBuilder.save()` and `format_workbook()` already apply that formatting automatically to anything written through them — your job is to get good data into a table, not to reimplement styling.

## 0. Decide the mode

- **Research mode**: the user names a topic ("2026 AI 에이전트 시장", "국내 OTT 서비스 요금제 비교") with no specific file attached. Go to §1.
- **Analysis mode**: the user references a specific `.xlsx` or `.csv` file that already exists (a path, "다운로드 폴더에 있는 파일", an attachment). Go to §4.

If a request plausibly wants prose (an explanation, a narrative report) rather than a table, prefer the `research-report-docx` skill instead — don't force a spreadsheet on content that isn't tabular.

## 1. Pin down the topic (research mode)

Don't ask about things you can infer or default:
- **Language**: match the language the user is asking in (default Korean for this project).
- **Table scope**: default to one overview table plus one comparison table per major sub-theme (e.g. by year, by company, by region) unless the user asks for more or less. If the topic is too broad to table sensibly in one pass (e.g. bare "AI"), ask the user to narrow it rather than guessing.
- **Sources sheet**: always include one — a table isn't trustworthy without traceable numbers.

## 2. Research with WebSearch/WebFetch

Same discipline as any research task: use `WebSearch` to find sources, then `WebFetch` promising results for real content rather than writing from snippets. Since the output here is numeric tables, pay extra attention to:

- **Getting the actual numbers**, not just claims — a comparison table with vague text in a numeric column is useless.
- **Units and scale**: note whether a figure is ₩억/조, %, YoY vs QoQ, etc. — this determines the `number_format` you'll use (see §3).
- **Publish dates** for anything time-sensitive; if sources disagree on a number, keep both and note the discrepancy in the table rather than silently picking one.
- Keep a running `(source_title, url)` list as you go — you need it verbatim for the sources sheet.

## 3. Build the workbook (research mode)

```python
import sys
sys.path.insert(0, "scripts")
from create_xlsx import SheetBuilder

wb = SheetBuilder(title="AI 에이전트 시장 조사", main_color="1F4E79")
wb.add_title("연도별 시장 규모")
wb.write_table(
    headers=["연도", "시장 규모(억 달러)", "전년 대비 성장률"],
    rows=[
        [2023, 51, 0.28],
        [2024, 78, 0.53],
        [2025, 121, 0.55],
    ],
)

wb.add_sheet("기업별 비교")
wb.add_title("주요 기업 비교")
wb.write_table(
    headers=["기업", "주요 제품", "2025 매출(억 달러)"],
    rows=[
        ["OpenAI", "ChatGPT / Agents SDK", 37],
        ["Anthropic", "Claude / Agent SDK", 20],
    ],
)

wb.add_sheet("참고자료")
wb.add_title("참고자료")
wb.write_table(
    headers=["제목", "URL"],
    rows=[
        ["OpenAI 2025 revenue report", "https://..."],
        ["Anthropic funding announcement", "https://..."],
    ],
)

wb.save("research/AI_에이전트_시장_조사.xlsx")
```

Notes:
- `wb.save()` runs the full auto-formatting pass for you: an `ID` column on every table, bold headers, a normalized 10pt body font, and — this is the important part for research data — it scans each sheet's headers for growth/rate keywords (성장률, 증가율, 전년 대비, 점유율, ...) or a year/month/quarter-like category column and **automatically adds a line or bar chart**. So if a table shows a trend worth visualizing, just name the column so it's recognizable (e.g. "전년 대비 성장률", not "YoY") and the chart appears without extra code.
- Decimal growth values (`0.28`) get formatted as `28.0%` automatically; if your source numbers are already scaled (e.g. `28` meaning 28%), leave them as-is — the auto-formatter detects the scale and won't double-convert.
- One sheet per major theme keeps tables readable; don't cram unrelated comparisons into one sheet just to avoid `add_sheet`.
- Always end with a 참고자료 sheet (title, URL columns) — it's the receipts for every number above it.

## 4. Read and understand the file (analysis mode)

Locate the file the user pointed at and open it before deciding what to build:

```python
from openpyxl import load_workbook

wb_in = load_workbook("다운로드/판매실적.xlsx")
for ws in wb_in.worksheets:
    print(ws.title, ws.dimensions)
```

For `.csv`, use the standard library `csv` module to read headers and rows.

Then pick the right move:

- **The file just needs cleanup/formatting** ("정리해줘", "표 예쁘게 만들어줘", "차트 추가해줘") and its existing structure is already reasonable (one header row, tabular data): use `load_and_format` directly — it's built exactly for this and already handles the missing-file, same-path, and can't-save error cases.

  ```python
  import sys
  sys.path.insert(0, "scripts")
  from create_xlsx import load_and_format

  load_and_format("다운로드/판매실적.xlsx", "research/판매실적_분석.xlsx")
  ```

- **The file needs real analysis first** (totals, averages, a derived comparison, combining multiple sheets/files) — compute the numbers in Python, then write them into a workbook the normal way and let `format_workbook` style everything, including the source data you also want to carry over:

  ```python
  import sys
  sys.path.insert(0, "scripts")
  from create_xlsx import SheetBuilder, format_workbook
  from openpyxl import load_workbook

  wb_in = load_workbook("다운로드/판매실적.xlsx")
  src = wb_in.active
  # ... compute a summary from src's rows in plain Python ...

  wb = SheetBuilder(title="판매실적 분석")
  wb.write_table(headers=["부서", "총 매출", "평균 매출"], rows=summary_rows)
  wb.save("research/판매실적_분석.xlsx")
  ```

  `format_workbook(some_workbook)` is also directly importable if you're assembling a `Workbook` object by hand (e.g. appending a summary sheet onto a copy of the loaded file) rather than building fresh through `SheetBuilder` — call it once before `.save()` and every sheet gets the same ID/header/quote/body/chart treatment.

- For CSV input, it's simplest to read the rows and feed them straight into `SheetBuilder.write_table` — you get the full formatting/charting pipeline for free rather than reimplementing it for a plain CSV.

## 5. Save and report back

Save research-mode and analysis-mode outputs to `research/`, matching the project convention already used for `.docx` reports (`research/<주제>_조사_보고서.xlsx`, `research/<원본파일명>_분석.xlsx`). Create the folder if needed — `SheetBuilder.save()` and `load_and_format()` already create parent directories.

After saving, tell the user in chat: the file path, which sheets it contains, a 1-2 sentence summary of what the data shows, whether a chart was generated, and how many sources were used (research mode) or what changed (analysis mode). Don't paste table contents into the chat — the `.xlsx` is the deliverable.

## Edge cases

- **Topic has little reliable numeric data**: say so in the sources sheet and chat summary rather than inventing plausible-looking numbers — a fabricated table is worse than no table.
- **Conflicting figures across sources**: keep both in the table (e.g. two rows, or a note column) rather than silently picking one.
- **Referenced file doesn't exist**: `load_and_format` already reports this clearly; if you're reading the file manually first, check `Path.exists()` before opening and tell the user rather than letting a traceback surface.
- **File has multiple sheets or no clear header row**: process each sheet independently; `format_workbook` already skips sheets where it can't find a header row instead of failing the whole file.
- **Ambiguous mode** (user gives both a topic and a file, e.g. "이 파일 참고해서 이 주제로 조사해줘"): treat the file as a primary source alongside web research, and say so in the 참고자료 sheet.
- **User wants a non-Korean workbook**: keep the same structure but translate headers/sheet names too, not just cell values.
