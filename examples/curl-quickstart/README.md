# curl-quickstart

**Goal:** make your first successful FileTag call in under three minutes, no MCP client needed.

## Prerequisites

- An API key. Get one free at https://console.gemina.co/registration/create-account.
- `curl` (already on macOS / Linux / WSL / any modern shell).
- A PDF or image file you want to tag.

## Setup

```bash
export GEMINA_API_KEY="paste-your-key-here"
```

## Tag a local file

```bash
# 1. Tag the file. Response includes metadata, filename suggestions, and a download URL.
curl -X POST https://api.gemina.co/api/v1/filetag \
  -H "X-API-Key: ${GEMINA_API_KEY}" \
  -F "file=@your-document.pdf"
```

Save the response to a file and pretty-print it:

```bash
curl -sX POST https://api.gemina.co/api/v1/filetag \
  -H "X-API-Key: ${GEMINA_API_KEY}" \
  -F "file=@your-document.pdf" \
  | jq .
```

## Tag a remote URL

If the file already lives at a public HTTPS URL, you can tag it without uploading:

```bash
curl -sX POST https://api.gemina.co/api/v1/filetag \
  -H "X-API-Key: ${GEMINA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/invoice.pdf"}' \
  | jq .
```

## Download the enriched copy

The response includes an `enriched_file_url` — a short-lived (15 minutes) signed URL that points to your file with metadata embedded into PDF properties or image EXIF.

```bash
# Pull the URL out of the response, then download it under its suggested filename
RESPONSE=$(curl -sX POST https://api.gemina.co/api/v1/filetag \
  -H "X-API-Key: ${GEMINA_API_KEY}" \
  -F "file=@your-document.pdf")

URL=$(echo "$RESPONSE" | jq -r .enriched_file_url)
NAME=$(echo "$RESPONSE" | jq -r .suggested_filename)
curl -sL "$URL" -o "$NAME"
echo "Downloaded $NAME"
```

## Smoke-test the MCP endpoint

If you're debugging an MCP client and want to confirm the server itself is reachable with your key:

```bash
curl -X POST https://api.gemina.co/api/v1/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "X-API-Key: ${GEMINA_API_KEY}" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"curl","version":"1"}}}'
```

A 200 response with a `result` object confirms auth + transport. If you see 401, the key is wrong. If you see 404, double-check the trailing slash on `/api/v1/mcp/`.

## What's next

- Try the same flow from an MCP client: [Claude Desktop walkthrough](../claude-desktop)
- Scale up to a whole directory: [bulk-tag-folder](../bulk-tag-folder)
- See the full response shape: [REST docs](https://www.gemina.co/docs/filetag)
