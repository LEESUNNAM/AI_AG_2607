"""Set sharing permissions on a Drive/Docs file via the Drive API.

Reuses the OAuth client created for this project's GWS integration
(credentials/gws_oauth_client_secret.json). Uses the full drive scope
because the target file (e.g. a Doc created via the Docs API) may not
have been created under the drive.file scope's app-created-file grant.
On first run it opens a browser for the user to grant the drive scope;
the granted token is cached to credentials/gws_drive_permission_token.json
for reuse.

Usage:
    python scripts/gws_drive_set_permission.py --file-id FILE_ID [--role reader] [--type anyone]

Prints the resulting permission id and a confirmation to stdout.
"""

import argparse
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "gws_oauth_client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gws_drive_permission_token.json")


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


def set_permission(file_id: str, role: str, permission_type: str) -> dict:
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    permission = (
        service.permissions()
        .create(
            fileId=file_id,
            body={"type": permission_type, "role": role},
            fields="id",
        )
        .execute()
    )

    return {"permissionId": permission["id"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-id", required=True)
    parser.add_argument("--role", default="reader")
    parser.add_argument("--type", default="anyone")
    args = parser.parse_args()

    result = set_permission(args.file_id, args.role, args.type)
    print(f"permissionId: {result['permissionId']}")
    print(f"role: {args.role}")
    print(f"type: {args.type}")


if __name__ == "__main__":
    main()
