"""Upload a local file to Google Drive via the Drive API.

Reuses the OAuth client created for this project's GWS integration
(credentials/gws_oauth_client_secret.json). Uses the drive.file scope
(least privilege: the app can only see files it creates), so on first
run it opens a browser for the user to grant that scope; the granted
token is cached to credentials/gws_drive_token.json for reuse.

Usage:
    python scripts/gws_drive_upload.py --file path/to/file.docx [--name "표시할 이름"] [--folder-id FOLDER_ID]

Prints the uploaded file's ID and URL to stdout.
"""

import argparse
import mimetypes
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "gws_oauth_client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gws_drive_token.json")


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


def upload_file(file_path: str, name: str | None, folder_id: str | None) -> dict:
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    metadata = {"name": name or os.path.basename(file_path)}
    if folder_id:
        metadata["parents"] = [folder_id]

    mime_type, _ = mimetypes.guess_type(file_path)
    media = MediaFileUpload(file_path, mimetype=mime_type or "application/octet-stream")

    uploaded = (
        service.files()
        .create(body=metadata, media_body=media, fields="id, webViewLink")
        .execute()
    )

    return {"fileId": uploaded["id"], "url": uploaded["webViewLink"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--name", default=None)
    parser.add_argument("--folder-id", default=None)
    args = parser.parse_args()

    result = upload_file(args.file, args.name, args.folder_id)
    print(f"fileId: {result['fileId']}")
    print(f"url: {result['url']}")


if __name__ == "__main__":
    main()
