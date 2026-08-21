"""Create a Google Calendar event via the Calendar API.

Reuses the OAuth client created for this project's GWS integration
(credentials/gws_oauth_client_secret.json). Uses the calendar.events
scope (least privilege: can manage events but not calendar settings
or the calendar list), so on first run it opens a browser for the
user to grant that scope; the granted token is cached to
credentials/gws_calendar_events_token.json for reuse.

This is a separate, write-scoped token from the read-only one used by
gws_calendar_briefing.py (calendar.readonly) — kept isolated so a
briefing/read task never silently gains write access.

Usage:
    python scripts/gws_calendar_create.py \
        --summary "팀 미팅" \
        --start "2026-08-25T10:00:00+09:00" \
        --end "2026-08-25T11:00:00+09:00" \
        [--location "회의실 A"] [--description "..."] \
        [--attendees a@example.com,b@example.com] \
        [--calendar-id primary]

For an all-day event, pass --all-day and give --start/--end as plain
dates (YYYY-MM-DD).

If --attendees is given, invitees are emailed a real calendar invite
(sendUpdates=all) — confirm the recipient list with the user before
running this.

Prints the created event's ID and htmlLink (the Google Calendar URL)
to stdout.
"""

import argparse
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "credentials")
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "gws_oauth_client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "gws_calendar_events_token.json")


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


def create_event(
    summary: str,
    start: str,
    end: str,
    all_day: bool,
    calendar_id: str,
    location: str | None,
    description: str | None,
    attendees: list[str] | None,
) -> dict:
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    event = {"summary": summary}
    if location:
        event["location"] = location
    if description:
        event["description"] = description
    if all_day:
        event["start"] = {"date": start}
        event["end"] = {"date": end}
    else:
        event["start"] = {"dateTime": start}
        event["end"] = {"dateTime": end}
    if attendees:
        event["attendees"] = [{"email": email} for email in attendees]

    created = (
        service.events()
        .insert(
            calendarId=calendar_id,
            body=event,
            sendUpdates="all" if attendees else "none",
        )
        .execute()
    )

    return {"id": created["id"], "htmlLink": created["htmlLink"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--all-day", action="store_true")
    parser.add_argument("--calendar-id", default="primary")
    parser.add_argument("--location", default=None)
    parser.add_argument("--description", default=None)
    parser.add_argument("--attendees", default=None, help="comma-separated email list")
    args = parser.parse_args()

    attendees = None
    if args.attendees:
        attendees = [e.strip() for e in args.attendees.split(",") if e.strip()]

    result = create_event(
        summary=args.summary,
        start=args.start,
        end=args.end,
        all_day=args.all_day,
        calendar_id=args.calendar_id,
        location=args.location,
        description=args.description,
        attendees=attendees,
    )
    print(f"eventId: {result['id']}")
    print(f"htmlLink: {result['htmlLink']}")


if __name__ == "__main__":
    main()
