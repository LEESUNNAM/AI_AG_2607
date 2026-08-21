"""Create a Google Docs document via the Google Docs API.

Reuses the OAuth client created for this project's GWS integration
(credentials/gws_oauth_client_secret.json). On first run it opens a
browser for the user to grant the documents scope; the granted token
is cached to credentials/gws_docs_token.json for reuse.

Usage:
    python scripts/gws_docs_create.py --title "제목" --content-file path/to/body.txt

Prints the created document's ID and URL to stdout.
"""

import argparse
import os

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


def create_document(title: str, content: str) -> dict:
    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)

    doc = service.documents().create(body={"title": title}).execute()
    document_id = doc["documentId"]

    if content:
        service.documents().batchUpdate(
            documentId=document_id,
            body={
                "requests": [
                    {
                        "insertText": {
                            "location": {"index": 1},
                            "text": content,
                        }
                    }
                ]
            },
        ).execute()

    return {
        "documentId": document_id,
        "url": f"https://docs.google.com/document/d/{document_id}/edit",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--content-file", required=True)
    args = parser.parse_args()

    with open(args.content_file, "r", encoding="utf-8") as f:
        content = f.read()

    result = create_document(args.title, content)
    print(f"documentId: {result['documentId']}")
    print(f"url: {result['url']}")


if __name__ == "__main__":
    main()
