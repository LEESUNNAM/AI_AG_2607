"""Send an existing Gmail draft via the Gmail API.

Reuses the gmail.compose-scoped token created by
gws_gmail_draft_create.py (credentials/gws_gmail_compose_token.json).
Only run this after the user has explicitly approved sending — it
delivers the draft's current content to its recipients immediately.

Usage:
    python scripts/gws_gmail_draft_send.py --draft-id <id-from-draft-create>

Prints the sent message's ID to stdout.
"""

import argparse
import os

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


def send_draft(draft_id: str) -> dict:
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    sent = service.users().drafts().send(userId="me", body={"id": draft_id}).execute()
    return {"id": sent["id"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft-id", required=True)
    args = parser.parse_args()

    result = send_draft(args.draft_id)
    print(f"messageId: {result['id']}")


if __name__ == "__main__":
    main()
