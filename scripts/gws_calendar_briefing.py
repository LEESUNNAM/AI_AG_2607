"""Fetch upcoming Google Calendar events for a weekly briefing.

Reuses the OAuth client created for this project's GWS integration
(credentials/gws_oauth_client_secret.json). On first run it opens a
browser for the user to grant the calendar.readonly scope; the granted
token is cached to credentials/gws_calendar_token.json for reuse.

Usage:
    python scripts/gws_calendar_briefing.py [--days 7] [--calendar-id primary]

Prints one JSON object per event to stdout (JSON Lines), each with:
    summary, start, end, all_day, location
"""

import argparse
import json
import os
from datetime import datetime, timedelta, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "gws_oauth_client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gws_calendar_token.json")


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


def fetch_events(days: int, calendar_id: str):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    now = datetime.now(timezone.utc)
    time_min = now.isoformat()
    time_max = (now + timedelta(days=days)).isoformat()

    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result.get("items", [])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--calendar-id", default="primary")
    args = parser.parse_args()

    events = fetch_events(args.days, args.calendar_id)

    for event in events:
        start = event.get("start", {})
        end = event.get("end", {})
        all_day = "date" in start
        record = {
            "summary": event.get("summary", "(제목 없음)"),
            "start": start.get("date") if all_day else start.get("dateTime"),
            "end": end.get("date") if all_day else end.get("dateTime"),
            "all_day": all_day,
            "location": event.get("location", ""),
        }
        print(json.dumps(record, ensure_ascii=False))


if __name__ == "__main__":
    main()
