"""Read a Google Docs document's plain text content via the Google Docs API.

Reuses the OAuth client and cached token created for gws_docs_create.py
(credentials/gws_docs_token.json).

Usage:
    python scripts/gws_docs_read.py --document-id <id>
    python scripts/gws_docs_read.py --url https://docs.google.com/document/d/<id>/edit

Prints the document's plain text content to stdout.
"""

import argparse
import os
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/documents"]
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "gws_oauth_client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gws_docs_token.json")


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


def extract_document_id(value: str) -> str:
    match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", value)
    return match.group(1) if match else value


def extract_text(document: dict) -> str:
    lines = []
    for element in document.get("body", {}).get("content", []):
        paragraph = element.get("paragraph")
        if not paragraph:
            continue
        line = "".join(
            run.get("textRun", {}).get("content", "")
            for run in paragraph.get("elements", [])
        )
        lines.append(line)
    return "".join(lines)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--document-id")
    group.add_argument("--url")
    parser.add_argument("--out-file")
    args = parser.parse_args()

    document_id = args.document_id or extract_document_id(args.url)

    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)
    document = service.documents().get(documentId=document_id).execute()

    text = extract_text(document)
    if args.out_file:
        with open(args.out_file, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        import sys
        sys.stdout.buffer.write(text.encode("utf-8"))


if __name__ == "__main__":
    main()
