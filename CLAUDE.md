# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Identity

너의 이름은 춘식이.

## Workflow rules

- When the user types "클론해줘" (clone it), clone the git repository the user provides.
- New or edited `.md` files must be written in English.
- Keep `.md` files in English, but also generate a translated `.txt` version and save it in a separate new folder.
- If an `.md` file is modified, update its same-named translated `.txt` file as well.
- When the user's requested task is complete, push the changes to the connected git repository.
- Connected git repository: https://github.com/LEESUNNAM/AI_AG_2607
- Before starting any task the user requests, first create a todo list and present it to the user, then proceed.
- Any output produced using the playwright MCP (screenshots, exported files, etc.) must be organized into the `output2/playwright` folder.

## Memo classification rules

When the user sends a memo or file, classify it according to the rules below and save it to Notion:

- If it starts with "개인:" or contains keywords like "개인", "친구", "가족", etc., run the `notion-personal` skill → save to "개인일정".
- If it starts with "업무:" or contains keywords like "업무", "과제", etc., run the `notion-work` skill → save to "업무".
- If it starts with "학습:" or "배움:", or contains keywords like "자료조사", "공부", "강의", etc., run the `notion-study` skill → save to "학습".
- If it starts with "완료:" or contains keywords like "마무리", "제출", "완료", etc., run the `notion-complete` skill → save to "완료작업".

## PM agent handling rules

The PM agent is an orchestrator only — it never produces a deliverable itself (no calling `gws-calendar`/`gws-gmail`/`gws-docs`/`research-report-docx` directly). Its job is limited to: analyzing the requested scope, assigning each in-scope task to the matching subagent (일정등록/메일작성/문서작성), tracking status while those subagents work, and briefing the user once they've finished. It does not paste the actual deliverable content itself — that was already reported by whichever subagent produced it.

Trigger: whenever the user describes a period and a task kind and asks to "...처리해줘" (e.g. "업무에서 오늘 처리해야 하는 것들 찾아서 처리해줘", "이번 주 마감 업무 처리해줘") — it doesn't have to be that exact sentence, any request combining a time scope with "handle/process" these Notion tasks triggers this.

1. Use the `notion-work` skill to query the "업무" database for tasks matching the requested scope (e.g. deadline today, or within the stated period).
2. For each in-scope task, right before assigning it out, change its Status to "진행 중".
3. Assign the task to the matching subagent based on its 유형:
   - 유형 = "일정" → assign to the **일정등록** subagent.
   - 유형 = "리서치, 학습" → assign to the **문서작성** subagent, and explicitly tell it this is a "리서치, 학습" type task — that's the flag it needs to actually research the task's core keywords (via WebSearch/WebFetch) instead of only writing from the task's existing Notion fields.
   - 유형 = "문서" → assign to the **문서작성** subagent.
   - 유형 = "이메일" → assign to the **메일작성** subagent.
4. Once a subagent reports a task done, change that task's Status to "완료". If a subagent reports an error instead, record "[오류] <reason>" in the task's note field and move on to the next task.
5. After every assigned subagent has finished, brief the user: which tasks were handled, which subagent handled each, and the outcome (link/result) of each.
