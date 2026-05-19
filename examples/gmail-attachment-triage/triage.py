"""Pull Gmail attachments, tag them with Gemina FileTag, and label by document type.

Usage:
    python triage.py [--query <gmail-search>] [--dry-run]

Prerequisites:
    - GEMINA_API_KEY env var (get a free key at https://console.gemina.co/registration/create-account)
    - credentials.json in this directory (Google OAuth client, type "Desktop app")
"""

from __future__ import annotations

import argparse
import base64
import csv
import os
import sys
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]
TAG_ENDPOINT = "https://api.gemina.co/api/v1/filetag"
SUPPORTED_MIME = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
}
LABEL_MAP = {
    "invoice": "FileTag/Invoices",
    "receipt": "FileTag/Receipts",
    "contract": "FileTag/Contracts",
    "purchase_order": "FileTag/POs",
}
DEFAULT_LABEL = "FileTag/Other"


def gmail_service():
    """Authenticate (cached) and return a Gmail API client."""
    creds = None
    token_path = Path("token.json")
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def ensure_label(service, name: str, cache: dict) -> str:
    """Return the label ID for name, creating it if needed."""
    if name in cache:
        return cache[name]
    existing = service.users().labels().list(userId="me").execute().get("labels", [])
    by_name = {lab["name"]: lab["id"] for lab in existing}
    if name in by_name:
        cache[name] = by_name[name]
        return by_name[name]
    created = (
        service.users()
        .labels()
        .create(
            userId="me",
            body={
                "name": name,
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show",
            },
        )
        .execute()
    )
    cache[name] = created["id"]
    return created["id"]


def iter_attachments(service, query: str):
    """Yield (message_id, sender, attachment_id, filename, mime_type) tuples."""
    resp = service.users().messages().list(userId="me", q=query).execute()
    for entry in resp.get("messages", []):
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=entry["id"], format="full")
            .execute()
        )
        sender = next(
            (
                h["value"]
                for h in msg.get("payload", {}).get("headers", [])
                if h["name"].lower() == "from"
            ),
            "",
        )
        for part in walk_parts(msg.get("payload", {})):
            if part.get("filename") and part.get("body", {}).get("attachmentId"):
                mime = part.get("mimeType")
                if mime in SUPPORTED_MIME:
                    yield (
                        entry["id"],
                        sender,
                        part["body"]["attachmentId"],
                        part["filename"],
                        mime,
                    )


def walk_parts(payload):
    yield payload
    for child in payload.get("parts") or []:
        yield from walk_parts(child)


def fetch_attachment(service, message_id: str, attachment_id: str) -> bytes:
    blob = (
        service.users()
        .messages()
        .attachments()
        .get(userId="me", messageId=message_id, id=attachment_id)
        .execute()
    )
    return base64.urlsafe_b64decode(blob["data"])


def tag_bytes(filename: str, content: bytes, api_key: str) -> dict:
    response = requests.post(
        TAG_ENDPOINT,
        headers={"X-API-Key": api_key},
        files={"file": (filename, content)},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--query",
        default="has:attachment newer_than:7d",
        help='Gmail search query. Default: "has:attachment newer_than:7d"',
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Tag attachments but don't apply Gmail labels.",
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=Path("output") / "triage.csv",
        help="CSV path for the activity log. Default: output/triage.csv",
    )
    args = parser.parse_args()

    api_key = os.environ.get("GEMINA_API_KEY")
    if not api_key:
        print("error: set GEMINA_API_KEY", file=sys.stderr)
        return 2
    if not Path("credentials.json").exists():
        print("error: credentials.json not found (see README)", file=sys.stderr)
        return 2

    service = gmail_service()
    args.log.parent.mkdir(parents=True, exist_ok=True)

    label_cache: dict = {}
    seen = 0
    tagged = 0

    with args.log.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["message_id", "sender", "filename", "document_type", "vendor", "date", "amount", "applied_label"]
        )

        for message_id, sender, att_id, filename, _mime in iter_attachments(
            service, args.query
        ):
            seen += 1
            content = fetch_attachment(service, message_id, att_id)
            try:
                result = tag_bytes(filename, content, api_key)
            except requests.HTTPError as e:
                print(f"  FAIL {filename}: {e}", file=sys.stderr)
                continue

            metadata = result.get("metadata", {})
            doc_type = metadata.get("document_type", "")
            label_name = LABEL_MAP.get(doc_type, DEFAULT_LABEL)
            applied = label_name if not args.dry_run else f"(dry-run) {label_name}"

            if not args.dry_run:
                label_id = ensure_label(service, label_name, label_cache)
                service.users().messages().modify(
                    userId="me",
                    id=message_id,
                    body={"addLabelIds": [label_id]},
                ).execute()

            writer.writerow(
                [
                    message_id,
                    sender,
                    filename,
                    doc_type,
                    metadata.get("vendor", ""),
                    metadata.get("date", ""),
                    metadata.get("amount", ""),
                    applied,
                ]
            )
            tagged += 1
            print(f"  ok   {filename} → {doc_type or '?'} → {applied}")

    print(f"\nDone. seen={seen} tagged={tagged}  log={args.log}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
