# Install Gemina FileTag (MCP)

> Machine-readable install guide for AI agents. Connect Gemina FileTag to any MCP-compatible client — tag, rename, and enrich any PDF or image in one call. Free tier: 1,500 tags/month, no credit card.

**Canonical location:** This file is the single source of truth for installing the Gemina FileTag MCP server. The website's `/llms.txt` points here. Agents should ingest the raw markdown at:

`https://raw.githubusercontent.com/tommyil/gemina-mcp/main/llms-install.md`

- Source repository: https://github.com/tommyil/gemina-mcp
- Product page: https://www.gemina.co/filetag
- Full docs (markdown): https://www.gemina.co/docs/filetag.md
- MCP manifest (JSON): https://www.gemina.co/.well-known/mcp.json
- Site index: https://www.gemina.co/llms.txt

---

## 1. Prerequisites

- An MCP-compatible client that speaks **Streamable HTTP** (Claude Desktop, Cursor, Claude Code, VS Code, Cline, Codex CLI, Windsurf, OpenClaw, Hermes-Agent, MCP Inspector — or any other client supporting the spec).
- A Gemina API key. Get one free (no credit card) at: https://console.gemina.co/registration/create-account

## 2. Endpoint

| Field | Value |
|---|---|
| MCP URL | `https://api.gemina.co/api/v1/mcp/` |
| Transport | Streamable HTTP |
| Auth header | `X-API-Key: <your-api-key>` *(or)* `Authorization: Bearer <your-api-key>` |
| Free tier | 1,500 calls/month |
| Rate limit | ~10 calls/second per API key |
| File types | PDF, PNG, JPEG, GIF, WebP — up to 50 MB |

## 3. Tools exposed

- **`files_create_upload`** — Reserve a pre-signed upload slot. Returns `file_id` and a PUT URL to upload the document bytes to.
- **`tag_file`** — Tag a previously-uploaded file by `file_id`. Returns metadata, six suggested filename patterns, and a short-lived enriched-file URL.
- **`tag_url`** — Fetch and tag a publicly-accessible HTTPS URL directly. Same response shape as `tag_file`.

## 4. Client-specific install snippets

Each snippet uses the `X-API-Key` header variant. Replace `<paste-your-key-here>` with your actual API key. `Authorization: Bearer <key>` works equivalently if your client prefers bearer tokens.

### Claude Desktop

Claude Desktop's `claude_desktop_config.json` does not support remote HTTP MCP servers directly — the file schema is stdio-only. Two paths:

**For human users** — use the Custom Connectors UI: Settings → Connectors → Add custom connector → paste `https://api.gemina.co/api/v1/mcp/` → API key auth.

**For agents writing config files** — use the `mcp-remote` stdio bridge (requires Node.js 18+).

File: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows).

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

Note no space after `X-API-Key:` in the `--header` arg (shell-split workaround), and the env-var indirection keeps the literal key out of `args`.

### Cursor

File: `~/.cursor/mcp.json`. Cursor accepts remote Streamable HTTP servers directly.

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

### Claude Code

One-line CLI registration:

```bash
claude mcp add --transport http gemina https://api.gemina.co/api/v1/mcp/ \
  --header "X-API-Key: <paste-your-key-here>"
```

### VS Code

File: `.vscode/mcp.json` per workspace.

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

```toml
[mcp_servers.gemina]
url = "https://api.gemina.co/api/v1/mcp/"
http_headers = { "X-API-Key" = "<paste-your-key-here>" }
```

### Windsurf

File: `~/.codeium/windsurf/mcp_config.json`. Note: the field is `serverUrl`, not `url`.

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

```bash
openclaw mcp set gemina '{"url":"https://api.gemina.co/api/v1/mcp/","transport":"streamable-http","headers":{"X-API-Key":"<paste-your-key-here>"}}'
```

### Hermes-Agent

Append under `mcp_servers` in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  gemina:
    url: "https://api.gemina.co/api/v1/mcp/"
    headers:
      X-API-Key: "<paste-your-key-here>"
```

### MCP Inspector (debugging)

```bash
npx @modelcontextprotocol/inspector

# Then in the Inspector UI:
#   Transport: Streamable HTTP
#   URL:       https://api.gemina.co/api/v1/mcp/
#   Header:    X-API-Key: <paste-your-key-here>
```

## 5. Verify the install

Smoke-test the endpoint directly with curl — a valid response confirms the API key, the network path, and the MCP server are all working:

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

- **401 / auth errors** — Confirm the key is pasted without quotes inside the value, and that the header name is exactly `X-API-Key` (case-insensitive) or `Authorization: Bearer <key>`.
- **Client can't connect to MCP** — Verify your client supports **Streamable HTTP** transport (not stdio). The endpoint URL must end with a trailing slash: `/api/v1/mcp/`.
- **Out of credits** — The free tier resets monthly. Upgrade at https://www.gemina.co/pricing or wait for reset.
- **File too large / unsupported type** — Limit is 50 MB. Supported: PDF, PNG, JPEG, GIF, WebP.

## 9. Get help

- Email: info@gemina.co
- Docs: https://www.gemina.co/docs/filetag
- Console (manage API keys, billing, usage): https://console.gemina.co
