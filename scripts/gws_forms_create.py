"""Create a Google Form via the Forms API.

Reuses the OAuth client created for this project's GWS integration
(credentials/gws_oauth_client_secret.json). On first run it opens a
browser for the user to grant the forms.body scope; the granted
token is cached to credentials/gws_forms_token.json for reuse.

Usage:
    python scripts/gws_forms_create.py --title "제목" [--questions-file path/to/questions.json]

questions.json is a JSON array, each item shaped like:
    {"title": "질문 내용", "type": "TEXT", "required": true}
    {"title": "질문 내용", "type": "PARAGRAPH_TEXT", "required": false}
    {"title": "질문 내용", "type": "MULTIPLE_CHOICE", "options": ["A", "B"], "required": true}
    {"title": "질문 내용", "type": "CHECKBOX", "options": ["A", "B"], "required": false}

Prints the created form's ID and URLs (edit + responder) to stdout.
"""

import argparse
import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/forms.body"]
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "gws_oauth_client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gws_forms_token.json")

CHOICE_TYPES = {"MULTIPLE_CHOICE": "RADIO", "CHECKBOX": "CHECKBOX"}


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds


def build_question_item(index: int, question: dict) -> dict:
    q_type = question["type"]
    required = question.get("required", False)

    if q_type in ("TEXT", "PARAGRAPH_TEXT"):
        question_body = {
            "required": required,
            "textQuestion": {"paragraph": q_type == "PARAGRAPH_TEXT"},
        }
    elif q_type in CHOICE_TYPES:
        question_body = {
            "required": required,
            "choiceQuestion": {
                "type": CHOICE_TYPES[q_type],
                "options": [{"value": opt} for opt in question["options"]],
            },
        }
    else:
        raise ValueError(f"지원하지 않는 질문 유형: {q_type}")

    return {
        "createItem": {
            "item": {
                "title": question["title"],
                "questionItem": {"question": question_body},
            },
            "location": {"index": index},
        }
    }


def create_form(title: str, questions: list) -> dict:
    creds = get_credentials()
    service = build("forms", "v1", credentials=creds)

    form = service.forms().create(body={"info": {"title": title}}).execute()
    form_id = form["formId"]

    if questions:
        requests = [build_question_item(i, q) for i, q in enumerate(questions)]
        service.forms().batchUpdate(
            formId=form_id, body={"requests": requests}
        ).execute()

    return {
        "formId": form_id,
        "editUrl": f"https://docs.google.com/forms/d/{form_id}/edit",
        "responderUri": form.get("responderUri", f"https://docs.google.com/forms/d/{form_id}/viewform"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--questions-file", default=None)
    args = parser.parse_args()

    questions = []
    if args.questions_file:
        with open(args.questions_file, "r", encoding="utf-8") as f:
            questions = json.load(f)

    result = create_form(args.title, questions)
    print(f"formId: {result['formId']}")
    print(f"editUrl: {result['editUrl']}")
    print(f"responderUri: {result['responderUri']}")


if __name__ == "__main__":
    main()
