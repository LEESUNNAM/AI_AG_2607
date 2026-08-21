---
name: gws-forms
description: Builds a Google Form from the user's requirements (question list, constraints, source material) by generating Google Apps Script code (FormApp) and uploading it as a real Apps Script project via this project's GWS CLI tool (scripts/gws_apps_script_create.py) — not the plain Forms API. Use this whenever the user asks to create, build, or make a Google Form / 구글 폼 / 설문지 / 신청서 — phrases like "이 조건으로 구글폼 만들어줘", "설문지 하나 만들어줘", "신청서 폼 제작해줘", "이 자료 기반으로 퀴즈 폼 만들어줘", "make a Google Form for X" — especially when the form needs anything beyond plain text/multiple-choice questions: quiz scoring, sections/page breaks, scale/date/time questions, email collection, a linked response spreadsheet, or a custom confirmation message. Always use the Apps Script route for every Google Form request in this project, even simple ones, for consistency.
---

# GWS Forms (Apps Script route)

Build the requested Google Form by writing Google Apps Script code that uses the `FormApp` service, then uploading it as a real Apps Script project via `scripts/gws_apps_script_create.py`. `FormApp` covers everything the raw Forms API struggles with — quiz mode with per-question points and feedback, sections/branching, scale/date/time/file-upload questions, linking responses to a spreadsheet, custom confirmation messages — so this is the one path this project uses for every form request, not just complex ones.

## Why the code isn't executed automatically

`gws_apps_script_create.py` only creates the Apps Script project and uploads your code — it deliberately does not run it. Running Apps Script code that calls `FormApp`/`DriveApp` requires the user to grant those permissions, and the cleanest way to get that consent is Google's own in-editor authorization prompt (the one that appears the first time you click Run on a new script) rather than trying to script it through this project's separate OAuth client. So the last mile — clicking Run once — is the user's, and that's fine: it's a single click with a permission popup they'll immediately recognize.

## 1. Gather the form's requirements

Don't guess a question list from a vague request — ask for (or extract from any material the user already gave you in the conversation):
- **Title** and, if useful, a short description shown at the top of the form.
- **Questions**, each with its type. Common `FormApp` item types: text (`addTextItem`), paragraph text (`addParagraphTextItem`), multiple choice (`addMultipleChoiceItem`), checkboxes (`addCheckboxItem`), linear scale (`addScaleItem`), date (`addDateItem`), time (`addTimeItem`), section header (`addSectionHeaderItem`), page break for multi-section forms (`addPageBreakItem`). Ask which are required (`.setRequired(true)`).
- **Quiz mode**: if the user wants scoring/correct answers, you need each question's point value and correct choice(s) — ask if not given. Don't invent "correct" answers for subjective content.
- **Response handling**: does the user want responses collected into a Google Sheet? If so, either use an existing spreadsheet ID they give you, or offer to create one first with `scripts/gws_sheets_create.py` and use its returned `spreadsheetId`.
- **Email collection / confirmation message**: only include if the user asks — don't default to collecting respondent emails without being asked, since that's a privacy-relevant default.

## 2. Write the Apps Script code

Generate a single `Code.gs`-style file with one entry-point function (always name it `createForm` so instructions to the user stay consistent across forms). Shape:

```javascript
function createForm() {
  var form = FormApp.create('설문 제목')
    .setDescription('설문 설명')
    .setCollectEmail(false)
    .setConfirmationMessage('응답해주셔서 감사합니다.');

  form.addTextItem()
    .setTitle('이름을 입력해주세요')
    .setRequired(true);

  var mc = form.addMultipleChoiceItem();
  mc.setTitle('가장 좋아하는 색은?')
    .setChoices([
      mc.createChoice('빨강'),
      mc.createChoice('파랑'),
      mc.createChoice('초록'),
    ])
    .setRequired(false);

  // Quiz mode example (omit setIsQuiz/points/feedback entirely if not a quiz):
  // form.setIsQuiz(true);
  // mc.setPoints(10).setFeedbackForCorrect(
  //   FormApp.createFeedback().setText('정답입니다!').build()
  // ).setAnswerCorrectAt = ... // use setChoiceValues with isCorrect flags instead, see reference below

  // Link responses to an existing spreadsheet, if requested:
  // form.setDestination(FormApp.DestinationType.SPREADSHEET, 'SPREADSHEET_ID');

  Logger.log('Form URL: ' + form.getPublishedUrl());
  Logger.log('Edit URL: ' + form.getEditUrl());
}
```

For quiz questions, build choices with correctness inline instead of `createChoice`:
```javascript
mc.setChoiceValues(['정답', '오답1', '오답2']); // simple, no scoring
// or, for scoring:
mc.setChoices([
  mc.createChoice('정답', true),
  mc.createChoice('오답1', false),
  mc.createChoice('오답2', false),
]).setPoints(10);
```
and call `form.setIsQuiz(true)` once, before any items are scored.

Always end the function with the two `Logger.log` lines above — that's how the user finds the form's URLs after running it (see §4).

## 3. Create the Apps Script project

Save the generated code to a temp file, then from the repo root:

```bash
python scripts/gws_apps_script_create.py --title "<폼 이름> 생성 스크립트" --code-file <path-to-code.gs>
```

This prints:
```
scriptId: <id>
editorUrl: https://script.google.com/d/<id>/edit
```

## 4. First-time auth and API activation

The Apps Script API has one extra setup step beyond this project's other GWS tools — expect to walk the user through all three, in order, the first time this skill runs on a given Google account:

1. **OAuth consent for `script.projects`**: opens a browser the first time. Run via Bash with `run_in_background: true`, tell the user to approve in the browser, pick up the result once the background task completes.
2. **`Google Apps Script API has not been used ... or it is disabled` (Cloud Console-level)**: surface the activation URL from the error (`https://console.developers.google.com/apis/api/script.googleapis.com/overview?project=...`), ask the user to enable it there, then re-run.
3. **`User has not enabled the Apps Script API` (personal account setting — distinct from step 2, confirmed by testing)**: this one isn't a Cloud project setting at all — it's a per-Google-account toggle. Send the user to `https://script.google.com/home/usersettings` and ask them to turn on "Google Apps Script API", then re-run the same command.

All three are one-time per Google account/project — once done, later `gws-forms` runs go straight through without any of this.

## 5. Hand off to the user

Tell the user, clearly, these steps (in Korean, matching the project's language):
1. `editorUrl`을 열어주세요.
2. 상단 함수 선택 드롭다운에서 `createForm`을 선택하고 실행(▶) 버튼을 누르세요.
3. 처음 실행하면 권한 승인 팝업이 뜹니다 — 본인 계정으로 승인해주세요.
4. 실행이 끝나면 상단 메뉴의 "실행 기록"(또는 보기 > Logs, `Ctrl+Enter`)에서 폼 URL을 확인할 수 있습니다.

If the user reports back the logged URL, you can help further (e.g. summarize the form, note anything to double check) — but you won't have it automatically, since the code only runs when they click it.

## Edge cases

- **User wants to edit a form already created this way**: don't create a duplicate project. Either (a) ask the user for the existing `scriptId` and call `service.projects().updateContent()` yourself with revised code (same API as `gws_apps_script_create.py` uses internally — you can invoke it via a short one-off Python snippet, or extend the script if this becomes a common request), or (b) tell them to edit the form directly in the Google Forms UI for small tweaks.
- **Quiz with no clear correct answers** (e.g. opinion questions): don't force quiz mode — ask whether it should really be scored, or just a plain form.
- **User wants a response spreadsheet but has none**: offer to create one first via `scripts/gws_sheets_create.py --title "<이름> 응답"` and plug the returned `spreadsheetId` into `setDestination`.
- **Very large question sets**: still fine — Apps Script has no meaningful item-count limit for this use case — but double check the requirement list with the user before generating code so you're not guessing at scale.
