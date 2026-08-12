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
