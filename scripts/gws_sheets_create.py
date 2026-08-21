"""Create a Google Sheets spreadsheet via the Sheets API.

Reuses the OAuth client created for this project's GWS integration
(credentials/gws_oauth_client_secret.json). On first run it opens a
browser for the user to grant the spreadsheets scope; the granted
token is cached to credentials/gws_sheets_token.json for reuse.

Usage:
    python scripts/gws_sheets_create.py --title "제목" [--csv-file path/to/data.csv]

If --csv-file is given, its rows are written starting at cell A1 of
the first sheet. Prints the created spreadsheet's ID and URL to stdout.
"""

import argparse
import csv
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "gws_oauth_client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gws_sheets_token.json")


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


def create_spreadsheet(title: str, csv_file: str | None) -> dict:
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)

    spreadsheet = (
        service.spreadsheets()
        .create(body={"properties": {"title": title}})
        .execute()
    )
    spreadsheet_id = spreadsheet["spreadsheetId"]

    if csv_file:
        with open(csv_file, "r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        if rows:
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range="A1",
                valueInputOption="USER_ENTERED",
                body={"values": rows},
            ).execute()

    return {
        "spreadsheetId": spreadsheet_id,
        "url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--csv-file", default=None)
    args = parser.parse_args()

    result = create_spreadsheet(args.title, args.csv_file)
    print(f"spreadsheetId: {result['spreadsheetId']}")
    print(f"url: {result['url']}")


if __name__ == "__main__":
    main()
