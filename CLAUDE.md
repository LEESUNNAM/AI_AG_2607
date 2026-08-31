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

When the user issues the command "업무에서 오늘 처리해야 하는 것들 찾아서 처리해줘" (find and handle today's due work items):

1. Use the `notion-work` skill to query the "업무" database for tasks whose 마감일 (deadline) is today.
2. Process each task in order.
3. Right before starting a task, change its Status to "진행 중".
4. Right after finishing a task, change its Status to "완료".
5. If an error occurs, record "[오류] <reason>" in the task's note field, then move on to the next task.

Skill to run per task type:
- 유형 = "일정" → `gws-calendar` skill: identify the schedule from the task name and register it on the calendar.
- 유형 = "리서치, 학습" → `research-report-docx` skill: research the core keywords and save the results in the task's note field.
- 유형 = "문서" → `gws-docs` skill: create a sheet organizing the related data.
- 유형 = "이메일" → `gws-gmail` skill: draft and send an email based on the task name.
