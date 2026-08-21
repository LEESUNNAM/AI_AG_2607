"""Create a Gmail draft via the Gmail API (does not send anything).

Reuses the OAuth client created for this project's GWS integration
(credentials/gws_oauth_client_secret.json). Uses the gmail.compose
scope (create/read/update/delete drafts, send drafts — but not read
or modify the rest of the mailbox), so on first run it opens a
browser for the user to grant that scope; the granted token is
cached to credentials/gws_gmail_compose_token.json for reuse.

This is a separate, compose-scoped token from the send-only one used
by gws_gmail_send.py (gmail.send) — kept isolated since drafting and
immediate-sending are different risk levels.

Usage:
    python scripts/gws_gmail_draft_create.py --to someone@example.com --subject "제목" --body-file path/to/body.txt
    python scripts/gws_gmail_draft_create.py --to someone@example.com --subject "제목" --body "본문 텍스트"

The draft is created in the user's actual Gmail Drafts folder — it is
NOT sent. Prints the draft's ID to stdout; pass that ID to
gws_gmail_draft_send.py to actually send it once approved.
"""

import argparse
import base64
import os
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "gws_oauth_client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gws_gmail_compose_token.json")


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


def create_draft(to: str, subject: str, body: str, cc: str | None = None) -> dict:
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(body, "plain", "utf-8")
    message["to"] = to
    message["subject"] = subject
    if cc:
        message["cc"] = cc

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    draft = (
        service.users()
        .drafts()
        .create(userId="me", body={"message": {"raw": raw}})
        .execute()
    )
    return {"draftId": draft["id"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", default=None)
    parser.add_argument("--body-file", default=None)
    parser.add_argument("--cc", default=None)
    args = parser.parse_args()

    if not args.body and not args.body_file:
        parser.error("--body 또는 --body-file 중 하나는 필수입니다.")

    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            body = f.read()
    else:
        body = args.body

    result = create_draft(args.to, args.subject, body, args.cc)
    print(f"draftId: {result['draftId']}")


if __name__ == "__main__":
    main()
