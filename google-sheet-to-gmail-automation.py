from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import gspread
import os

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.send"
]

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )
        creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

client = gspread.authorize(creds)

SPREADSHEET_ID = "1L3hQZkZX7ooUZr2jYWZ0FeKwnHp8y1X0noLmZwp1v3s"

sheet = client.open_by_key(SPREADSHEET_ID).sheet1

rows = sheet.get_all_records()

print("Google Sheet connected successfully!")
print(f"Number of rows: {len(rows)}")

for row in rows:
    print(row)

gmail_service = build("gmail", "v1", credentials=creds)

message = MIMEText(
    "Hello! This is a test email sent from Python using Gmail API."
)

message["to"] = "pandeeswari.learning@gmail.com"
message["subject"] = "Python Gmail API Test"

raw_message = base64.urlsafe_b64encode(
    message.as_bytes()
).decode()

gmail_service.users().messages().send(
    userId="me",
    body={"raw": raw_message}
).execute()

print("Test email sent successfully!")
