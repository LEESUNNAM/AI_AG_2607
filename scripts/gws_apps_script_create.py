"""Create (or update) a standalone Google Apps Script project via the
Apps Script API, uploading a given .gs source file as its content.

This does NOT execute the script — it only creates the project and
uploads code, so the user can open it in the Apps Script editor and
click Run themselves. That keeps auth simple: the script's own
permissions (e.g. FormApp, DriveApp) are granted by the user through
Google's normal in-editor authorization prompt when they run it, not
through this project's OAuth client.

Reuses the OAuth client created for this project's GWS integration
(credentials/gws_oauth_client_secret.json). On first run it opens a
browser for the user to grant the script.projects scope; the granted
token is cached to credentials/gws_appsscript_token.json for reuse.

Usage:
    python scripts/gws_apps_script_create.py --title "제목" --code-file path/to/code.gs

Prints the created project's script ID and editor URL to stdout.
"""

import argparse
import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/script.projects"]
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "gws_oauth_client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gws_appsscript_token.json")

MANIFEST = json.dumps(
    {
        "timeZone": "Asia/Seoul",
        "exceptionLogging": "STACKDRIVER",
        "runtimeVersion": "V8",
    }
)


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


def create_project(title: str, code: str) -> dict:
    creds = get_credentials()
    service = build("script", "v1", credentials=creds)

    project = service.projects().create(body={"title": title}).execute()
    script_id = project["scriptId"]

    service.projects().updateContent(
        scriptId=script_id,
        body={
            "files": [
                {"name": "Code", "type": "SERVER_JS", "source": code},
                {"name": "appsscript", "type": "JSON", "source": MANIFEST},
            ]
        },
    ).execute()

    return {
        "scriptId": script_id,
        "editorUrl": f"https://script.google.com/d/{script_id}/edit",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--code-file", required=True)
    args = parser.parse_args()

    with open(args.code_file, "r", encoding="utf-8") as f:
        code = f.read()

    result = create_project(args.title, code)
    print(f"scriptId: {result['scriptId']}")
    print(f"editorUrl: {result['editorUrl']}")


if __name__ == "__main__":
    main()
