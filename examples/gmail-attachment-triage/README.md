# gmail-attachment-triage

Pull PDF and image attachments from Gmail, tag them with Gemina FileTag, and apply Gmail labels based on the structured metadata. The headline email-automation use case.

## What it does

1. Authenticates with Gmail (OAuth2, read-only + labels scope).
2. Searches for messages matching a query (default: `has:attachment newer_than:7d`).
3. Downloads attachments, tags each one with FileTag.
4. Applies Gmail labels by document type — `Invoices`, `Contracts`, `Receipts`, etc.
5. Writes a CSV log of `message_id, sender, document_type, vendor, date, total`.

## Setup

```bash
cd examples/gmail-attachment-triage
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

You need two credentials:

1. **Gemina API key** — `export GEMINA_API_KEY="..."`. Free key at https://console.gemina.co/registration/create-account.
2. **Google OAuth credentials** — `credentials.json` in this directory. Create at https://console.cloud.google.com/apis/credentials → "OAuth client ID" → "Desktop app". Enable the Gmail API on the same project.

On first run, `triage.py` opens a browser for Google consent and caches a refresh token to `token.json`.

## Run

```bash
python triage.py

# Customize the search query:
python triage.py --query 'has:attachment from:billing@*'

# Dry-run (downloads + tags but doesn't apply labels):
python triage.py --dry-run
```

## Label mapping

The default mapping (edit `LABEL_MAP` in `triage.py` to customize):

| `metadata.document_type` | Gmail label |
|---|---|
| `invoice` | `FileTag/Invoices` |
| `receipt` | `FileTag/Receipts` |
| `contract` | `FileTag/Contracts` |
| `purchase_order` | `FileTag/POs` |
| _other_ | `FileTag/Other` |

Labels are created if they don't exist.

## Cost estimation

Each attachment counts as one FileTag call. With the free tier's 1,500 calls/month, this comfortably covers a small business mailbox. Heavy users (~50 attachments/day) will exhaust the free tier mid-month — see [pricing](https://www.gemina.co/pricing) for paid plans.

## Privacy

- The script never re-uploads message bodies to FileTag, only attachments.
- `token.json` stores the Google OAuth refresh token. Keep it out of version control (already in `.gitignore`).
- FileTag's privacy guarantees apply: documents never used for training, 7-day deletion, AES-256 at rest.

## What's next

- Schedule with cron / launchd / Task Scheduler to run every 15 minutes.
- Push the tagged metadata into your accounting system (QuickBooks, Xero, etc.).
- For Outlook/Microsoft 365, see [outlook-attachment-triage](../outlook-attachment-triage) _(coming soon)_.
