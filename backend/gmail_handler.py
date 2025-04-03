import os
import json
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask import Flask, jsonify, request
import re

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

app = Flask(__name__)

def get_gmail_service():
    """Authenticate and return Gmail API service instance."""
    creds = None

    # Load existing token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8000, redirect_uri_trailing_slash=False)

        # Save new token
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def categorize_priority(subject, snippet):
    """Categorize email priority based on subject and content."""
    subject_lower = subject.lower() if subject else ""
    snippet_lower = snippet.lower() if snippet else ""

    if "urgent" in subject_lower or "asap" in snippet_lower:
        return "Urgent"
    elif "follow-up" in subject_lower or "reminder" in snippet_lower:
        return "Follow-up"
    else:
        return "Low Priority"

def generate_summary(snippet):
    """Generate a brief summary of an email."""
    return snippet[:80] + "..." if len(snippet) > 80 else snippet

def suggest_quick_reply(priority):
    """Suggest quick replies based on priority."""
    if priority == "Urgent":
        return "Got it! I'll handle this ASAP."
    elif priority == "Follow-up":
        return "Thanks! I'll check and get back to you."
    else:
        return "Noted, I'll review this when I get time."

def fetch_gmail_messages():
    """Fetch recent Gmail messages and return them as a structured list."""
    service = get_gmail_service()
    
    try:
        results = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=10).execute()
        messages = results.get("messages", [])

        email_data = []
        for msg in messages:
            message = service.users().messages().get(userId="me", id=msg["id"], format="metadata").execute()

            # Extract email details
            headers = message.get("payload", {}).get("headers", [])
            email_info = {h["name"]: h["value"] for h in headers}

            sender = email_info.get("From", "Unknown Sender")
            subject = email_info.get("Subject", "No Subject")
            date = email_info.get("Date", "Unknown Date")
            snippet = message.get("snippet", "")
            email_id = msg["id"]  # Unique Gmail message ID

            # Process email details
            priority = categorize_priority(subject, snippet)
            summary = generate_summary(snippet)
            quick_reply = suggest_quick_reply(priority)

            # Construct Gmail link
            gmail_link = f"https://mail.google.com/mail/u/0/#inbox/{email_id}"

            email_data.append({
                "From": sender,
                "Subject": subject,
                "Date": date,
                "Snippet": snippet,
                "Priority": priority,
                "Summary": summary,
                "Quick Reply": quick_reply,
                "GmailLink": gmail_link
            })

        return email_data
    
    except Exception as e:
        print(f"❌ Error fetching emails: {e}")
        return []

@app.route('/fetch/gmail', methods=['GET'])
def fetch_gmail():
    """API endpoint to fetch emails"""
    emails = fetch_gmail_messages()
    return jsonify({"emails": emails})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
