# Install Gemina (MCP)

> Machine-readable install guide for AI agents. Connect Gemina to any MCP-compatible client — tag, rename, and enrich any PDF or image (FileTag, free tier), run Core-OCR extraction, and search your indexed documents. Free tier: 1,500 FileTag tags/month, no credit card.

**Canonical location:** This file is the single source of truth for installing the Gemina MCP server. The website's `/llms.txt` points here. Agents should ingest the raw markdown at:

`https://raw.githubusercontent.com/tommyil/gemina-mcp/main/llms-install.md`

- Source repository: https://github.com/tommyil/gemina-mcp
- Product page: https://www.gemina.co/filetag
- Full docs (markdown): https://www.gemina.co/docs/filetag.md
- MCP manifest (JSON): https://www.gemina.co/.well-known/mcp.json
- Site index: https://www.gemina.co/llms.txt

---

## 1. Prerequisites

- An MCP-compatible client that speaks **Streamable HTTP** (Claude Desktop, Cursor, Claude Code, VS Code, Cline, Codex CLI, Windsurf, OpenClaw, Hermes-Agent, MCP Inspector — or any other client supporting the spec).
- A Gemina account. Create one free (no credit card) at: https://console.gemina.co/registration/create-account
- **Default auth is OAuth sign-in** — the client discovers the authorization server from the MCP URL and the user signs in from the app. No key to paste.
- **Headless (CI, servers, scripts, or a client that doesn't prompt to sign in):** an API key from the console, sent as a header.

## 2. Endpoint

| Field | Value |
|---|---|
| MCP URL | `https://api.gemina.co/api/v1/mcp/` |
| Transport | Streamable HTTP |
| Auth (default) | OAuth 2.1 sign-in — discovery via RFC 9728 / RFC 8414; Dynamic Client Registration (DCR) and Client ID Metadata Documents (CIMD) both accepted; scope `mcp`; access tokens 1 h, rotating refresh tokens 30 d |
| OAuth discovery | `https://api.gemina.co/.well-known/oauth-protected-resource/api/v1/mcp` and `https://api.gemina.co/.well-known/oauth-authorization-server/api/v1/mcp` |
| Connected apps | Each OAuth-connected app gets its own API key named `<app> (OAuth)`; list and revoke under Console → API Keys → Connected apps (https://console.gemina.co) |
| Auth header (headless) | `X-API-Key: <your-api-key>` *(or)* `Authorization: Bearer <your-api-key>` |
| Free tier | 1,500 FileTag tags/month (extraction and document intelligence are paid — see https://www.gemina.co/pricing) |
| Rate limit | ~10 calls/second per API key (OAuth-connected apps count against their own key) |
| File types | PDF, PNG, JPEG, GIF, WebP, HEIC, AVIF — up to 50 MB |

## 3. Tools exposed

One server, 13 tools in three groups, plus 2 prompts. Anonymous discovery (`tools/list`, `prompts/list`) is served at `https://api.gemina.co/api/v1/mcp/public/`.

**FileTag (free tier)**

- **`files_create_upload`** — Reserve a pre-signed upload slot. Returns `file_id`, a PUT URL, and the headers to echo on the PUT (slot expires in 5 minutes).
- **`tag_file`** — Tag a previously-uploaded file by `file_id`. Returns metadata, six suggested filename patterns, and a short-lived enriched-file URL.
- **`tag_url`** — Fetch and tag a publicly-accessible HTTPS URL server-side (no private IPs, no redirects, 50 MB cap). Same response shape as `tag_file`.

**Extraction (Core-OCR, paid)**

- **`files_create_extraction_upload`** — Reserve a pre-signed upload slot for extraction (distinct from the FileTag slot). Follow the returned `next_tool_call` into `extract_document`.
- **`extract_document`** — Run extraction on an uploaded slot with one or more `extraction_types`: `ocr`, `invoice_headers`, `invoice_line_items`, `document_details_hebrew`, `document_line_items_hebrew`, or `custom_template`.
- **`get_extraction_result`** — Poll an asynchronous extraction by `meta.correlationId`; returns the result or `IN_PROCESS`.
- **`list_extractions`** — List past extractions, newest first; filter by `external_id`, `end_user_id`, or date window; paginate with `skip`/`limit`.
- **`get_extraction`** — Fetch one extraction by id, including the full extracted data.
- **`get_document`** — Fetch one document by id, including all of its extractions.
- **`submit_extraction_feedback`** — Submit verified/corrected field values for a completed extraction (`label:<human label>|ptr:/<json pointer>` keys); returns a per-field comparison summary.

**Document Intelligence (paid)**

- **`query_documents`** — Search the indexed document collection: `structured` (exact field filters), `semantic` (natural-language similarity), or `hybrid` (keyword + semantic, best default).
- **`aggregate_documents`** — Sums/averages/min/max/counts over indexed documents, optionally grouped (vendor, currency, document type, month, ...) and filtered like `query_documents`.
- **`index_document`** — (Re)index one document into the searchable index — after corrections, or to backfill documents processed before indexing was enabled.

**Prompts**

- **`explain_filename_patterns`** — The six filename patterns FileTag returns and how to choose between them.
- **`explain_upload_flow`** — The three-step upload flow: `files_create_upload` → PUT → `tag_file`.

All tools are listed for every key; the extraction and document-intelligence groups require a paid plan — see https://www.gemina.co/pricing.

## 4. Client-specific install snippets

Each client has two forms. **OAuth (default):** no header — the client discovers Gemina's authorization server from the MCP URL and prompts the user to sign in. **API key (headless):** the `X-API-Key` header variant; replace `<paste-your-key-here>` with the actual API key. `Authorization: Bearer <key>` works equivalently if the client prefers bearer tokens. OAuth support varies by client version — if the client does not prompt to sign in, use the API-key form.

### Claude Desktop / claude.ai

**OAuth (default):** claude.ai and Claude Desktop use the same Connectors flow — no config file, no `mcp-remote`, no API key. Gemina creates a key for the app when the user approves it.

```text
URL: https://api.gemina.co/api/v1/mcp/

1. Settings → Connectors
2. Add custom connector
3. Paste the URL
4. Sign in
```

Sign in with the Gemina account when prompted and approve the consent page. Tools appear in new chats immediately.

**API key (fallback):** Claude Desktop's `claude_desktop_config.json` does not support remote HTTP MCP servers directly — the file schema is stdio-only — and the Connectors UI cannot supply an `X-API-Key` header. To use a specific API key, go through the `mcp-remote` stdio bridge.

**Prerequisites**

- Node.js 18+ (on PATH, or use the absolute path to `npx` in the `command` field).
- In Claude Desktop, **Settings → Capabilities**, enable: *Code execution and file creation* → *Allow network egress* → *Domain allowlist: All domains* (or add `storage.googleapis.com` explicitly, where signed enriched-file URLs live). Without egress, tag results return correctly but Claude can't download the enriched-file URL — error: "Host not in allowlist". Capability changes only apply to new chats.

**Config**

File: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows). In Claude Desktop, **Settings → Developer → Edit Config** opens it.

```json
{
  "mcpServers": {
    "gemina": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://api.gemina.co/api/v1/mcp/",
        "--header",
        "X-API-Key:${GEMINA_API_KEY}"
      ],
      "env": {
        "GEMINA_API_KEY": "<paste-your-key-here>"
      }
    }
  }
}
```

**Notes**

- No space after `X-API-Key:` in the `--header` arg — `npx` shell-split workaround.
- Env-var indirection keeps the literal API key out of `args` (where it would otherwise show in process listings).
- Windows + `spawn npx ENOENT`: replace `"command": "npx"` with the absolute path from `where npx` (forward slashes work in JSON, e.g. `"C:/Program Files/nodejs/npx.cmd"`).

### Claude Code

**OAuth (default):** register, then run `/mcp` and sign in — Claude Code opens the Gemina sign-in in the browser.

```bash
claude mcp add --transport http gemina https://api.gemina.co/api/v1/mcp/
# then run /mcp and sign in
```

In Claude Code: `/mcp` → select **gemina** → **Authenticate** → browser sign-in → approve consent.

**API key (headless):**

```bash
claude mcp add --transport http gemina https://api.gemina.co/api/v1/mcp/ \
  --header "X-API-Key: <paste-your-key-here>"
```

### Cursor

File: `~/.cursor/mcp.json`. Cursor accepts remote Streamable HTTP servers directly.

**OAuth (default):**

```json
{
  "mcpServers": {
    "gemina": {
      "url": "https://api.gemina.co/api/v1/mcp/"
    }
  }
}
```

**API key (headless):**

```json
{
  "mcpServers": {
    "gemina": {
      "url": "https://api.gemina.co/api/v1/mcp/",
      "headers": {
        "X-API-Key": "<paste-your-key-here>"
      }
    }
  }
}
```

### VS Code

File: `.vscode/mcp.json` per workspace.

**OAuth (default):**

```json
{
  "servers": {
    "gemina": {
      "type": "http",
      "url": "https://api.gemina.co/api/v1/mcp/"
    }
  }
}
```

**API key (headless):**

```json
{
  "servers": {
    "gemina": {
      "type": "http",
      "url": "https://api.gemina.co/api/v1/mcp/",
      "headers": {
        "X-API-Key": "<paste-your-key-here>"
      }
    }
  }
}
```

### Cline

In Cline's MCP settings (gear icon → MCP Servers → Edit Config). The `type` field is required for Cline to recognize a remote Streamable HTTP server:

**OAuth (default):**

```json
{
  "mcpServers": {
    "gemina": {
      "type": "streamableHttp",
      "url": "https://api.gemina.co/api/v1/mcp/"
    }
  }
}
```

**API key (headless):**

```json
{
  "mcpServers": {
    "gemina": {
      "type": "streamableHttp",
      "url": "https://api.gemina.co/api/v1/mcp/",
      "headers": {
        "X-API-Key": "<paste-your-key-here>"
      }
    }
  }
}
```

### Codex CLI

Append to `~/.codex/config.toml`:

**OAuth (default):**

```toml
[mcp_servers.gemina]
url = "https://api.gemina.co/api/v1/mcp/"
```

**API key (headless):**

```toml
[mcp_servers.gemina]
url = "https://api.gemina.co/api/v1/mcp/"
http_headers = { "X-API-Key" = "<paste-your-key-here>" }
```

### Windsurf

File: `~/.codeium/windsurf/mcp_config.json`. Note: the field is `serverUrl`, not `url`.

**OAuth (default):**

```json
{
  "mcpServers": {
    "gemina": {
      "serverUrl": "https://api.gemina.co/api/v1/mcp/"
    }
  }
}
```

**API key (headless):**

```json
{
  "mcpServers": {
    "gemina": {
      "serverUrl": "https://api.gemina.co/api/v1/mcp/",
      "headers": {
        "X-API-Key": "<paste-your-key-here>"
      }
    }
  }
}
```

### OpenClaw

**OAuth (default):**

```bash
openclaw mcp set gemina '{"url":"https://api.gemina.co/api/v1/mcp/","transport":"streamable-http"}'
```

**API key (headless):**

```bash
openclaw mcp set gemina '{"url":"https://api.gemina.co/api/v1/mcp/","transport":"streamable-http","headers":{"X-API-Key":"<paste-your-key-here>"}}'
```

### Hermes-Agent

Append under `mcp_servers` in `~/.hermes/config.yaml`:

**OAuth (default):**

```yaml
mcp_servers:
  gemina:
    url: "https://api.gemina.co/api/v1/mcp/"
```

**API key (headless):**

```yaml
mcp_servers:
  gemina:
    url: "https://api.gemina.co/api/v1/mcp/"
    headers:
      X-API-Key: "<paste-your-key-here>"
```

### MCP Inspector (debugging)

**OAuth:**

```bash
npx @modelcontextprotocol/inspector

# Then in the Inspector UI:
#   Transport: Streamable HTTP
#   URL:       https://api.gemina.co/api/v1/mcp/
#   Auth:      Open Auth Settings → Quick OAuth Flow, then sign in
```

**API key:**

```bash
npx @modelcontextprotocol/inspector

# Then in the Inspector UI:
#   Transport: Streamable HTTP
#   URL:       https://api.gemina.co/api/v1/mcp/
#   Header:    X-API-Key: <paste-your-key-here>
```

## 5. Verify the install

Smoke-test the endpoint directly with curl. curl has no browser to sign in with, so this uses an API key — a valid response confirms the key, the network path, and the MCP server are all working. (OAuth clients discover the authorization server at `https://api.gemina.co/.well-known/oauth-authorization-server/api/v1/mcp`.)

```bash
curl -X POST https://api.gemina.co/api/v1/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "X-API-Key: <paste-your-key-here>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"curl","version":"1"}}}'
```

Then, from your agent, try the end-to-end flow:

```python
# 1. Reserve an upload slot
upload = mcp.call("files_create_upload", filename="invoice.pdf")

# 2. PUT the file to the signed URL
upload_to(upload.url, file_bytes)

# 3. Tag it
result = mcp.call("tag_file", file_id=upload.file_id)
# → metadata, six filename patterns, enriched-file URL

# Or, if the file is already at a public HTTPS URL:
result = mcp.call("tag_url", url="https://example.com/invoice.pdf")
```

A successful call returns this JSON envelope:

```json
{
  "document_id": "abc-123",
  "suggested_filename": "2026-02-15_Acme-Corp_Invoice_12345.pdf",
  "metadata": {
    "document_type": "invoice",
    "vendor": "Acme Corp",
    "date": "2026-02-15",
    "amount": 7200,
    "currency": "ILS",
    "document_number": "12345",
    "title": "Invoice",
    "tags": ["vendor", "invoice"]
  },
  "filename_patterns": {
    "date_first": "2026-02-15_Invoice_12345.pdf",
    "type_first": "Invoice_12345_2026-02-15.pdf",
    "vendor_first": "Acme-Corp_Invoice_2026-02-15.pdf",
    "date_vendor": "2026-02-15_Acme-Corp.pdf",
    "vendor_date": "Acme-Corp_2026-02-15.pdf",
    "compact": "Acme-Corp_Invoice.pdf"
  },
  "enriched_file_url": "https://api.gemina.co/files/tmp_abc123.pdf",
  "enriched_file_expires_at": "2026-02-15T12:15:00Z"
}
```

## 6. REST alternative

If your client doesn't speak MCP, the same API is available via REST. One call, same response shape:

```bash
curl -X POST https://api.gemina.co/api/v1/filetag \
  -H "X-API-Key: <paste-your-key-here>" \
  -F "file=@invoice.pdf"
```

The same API key works for both MCP and REST.

## 7. Privacy & retention

- Files are deleted within 7 days of upload (configurable per plan).
- Documents are never used to train AI models — Gemina's or anyone else's.
- AES-256 at rest, TLS 1.3 in transit.
- GDPR & CCPA compliant. Configurable data residency on paid plans.

## 8. Troubleshooting

- **401 / auth errors (API key)** — Confirm the key is pasted without quotes inside the value, and that the header name is exactly `X-API-Key` (case-insensitive) or `Authorization: Bearer <key>`.
- **OAuth: "Dynamic Client Registration rejected" / registration failed** — Make sure the URL ends with the trailing slash (`/api/v1/mcp/`) and update the client to a version that supports MCP OAuth (DCR or CIMD).
- **OAuth: token expired / calls start failing with 401 after a while** — Access tokens last 1 hour and refresh tokens 30 days; if the refresh lapsed, re-authenticate (Claude Code: `/mcp` → gemina → Authenticate; other clients: reconnect the server).
- **OAuth: key revoked** — If the app's key was revoked under Console → API Keys → Connected apps, reconnect the server from the app to get a new one.
- **OAuth: consent page says the request expired** — Start the sign-in again from the app (not by reloading the consent page).
- **Client can't connect to MCP** — Verify your client supports **Streamable HTTP** transport (not stdio). The endpoint URL must end with a trailing slash: `/api/v1/mcp/`.
- **Out of credits** — The free tier resets monthly. Upgrade at https://www.gemina.co/pricing or wait for reset.
- **File too large / unsupported type** — Limit is 50 MB. Supported: PDF, PNG, JPEG, GIF, WebP, HEIC, AVIF.

## 9. Get help

- Email: info@gemina.co
- Docs: https://www.gemina.co/docs/filetag
- Console (manage API keys, connected apps, billing, usage): https://console.gemina.co
