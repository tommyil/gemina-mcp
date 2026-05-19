<div align="center">
  <img src="assets/logo/logo.svg" alt="Gemina" width="120" />

# Gemina FileTag — MCP server

**Tag, rename, and enrich any PDF or image. One MCP call. Free tier: 1,500 tags/month, no credit card.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Free tier](https://img.shields.io/badge/free%20tier-1%2C500%20tags%2Fmonth-brightgreen.svg)](https://www.gemina.co/filetag)
[![MCP](https://img.shields.io/badge/MCP-Streamable%20HTTP-purple.svg)](https://modelcontextprotocol.io)
[![Last commit](https://img.shields.io/github/last-commit/tommyil/gemina-mcp.svg)](https://github.com/tommyil/gemina-mcp/commits/main)

[Install](#quick-install) • [Examples](./examples) • [Product page](https://www.gemina.co/filetag) • [Full docs](https://www.gemina.co/docs/filetag)

</div>

---

## What is this?

This repository is the **discovery, install, and examples surface** for Gemina FileTag's MCP server. The server itself is hosted at `https://api.gemina.co/api/v1/mcp/` — there is no daemon to run locally. Point your MCP-compatible client at the endpoint, paste an API key, and tag your first document in under a minute.

The server itself is closed-source (operated by Gemina). Everything in this repo — install snippets, examples, integration code — is MIT-licensed and contributions are welcome.

## What you get

Send a PDF or image. Get back structured metadata, six suggested filenames, and a downloadable copy with metadata already embedded in the file itself.

<details>
<summary><b>Sample input → sample output</b> (click to expand)</summary>

**Input:** any PDF or image up to 50 MB (PDF, PNG, JPEG, GIF, WebP).

**Output:**

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

Three uses out of one response — pick the one your code needs, ignore the rest.

</details>

## Quick install

You need an API key. Get one free (no credit card) at **https://console.gemina.co/registration/create-account**, then drop the snippet below into your MCP client's config and restart it.

**Endpoint:** `https://api.gemina.co/api/v1/mcp/` · **Transport:** Streamable HTTP · **Auth:** `X-API-Key` header

<details>
<summary><b>Claude Desktop</b></summary>

File: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows).

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

</details>

<details>
<summary><b>Cursor</b></summary>

File: `~/.cursor/mcp.json`.

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

</details>

<details>
<summary><b>Claude Code (CLI)</b></summary>

```bash
claude mcp add --transport http gemina https://api.gemina.co/api/v1/mcp/ \
  --header "X-API-Key: <paste-your-key-here>"
```

</details>

<details>
<summary><b>VS Code</b></summary>

File: `.vscode/mcp.json` (per workspace).

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

</details>

<details>
<summary><b>Cline</b></summary>

In Cline's MCP settings (gear icon → MCP Servers → Edit Config), add:

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

</details>

<details>
<summary><b>Windsurf</b></summary>

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

</details>

<details>
<summary><b>Codex CLI</b></summary>

Append to `~/.codex/config.toml`:

```toml
[mcp_servers.gemina]
url = "https://api.gemina.co/api/v1/mcp/"
http_headers = { "X-API-Key" = "<paste-your-key-here>" }
```

</details>

<details>
<summary><b>OpenClaw</b></summary>

```bash
openclaw mcp set gemina '{"url":"https://api.gemina.co/api/v1/mcp/","transport":"streamable-http","headers":{"X-API-Key":"<paste-your-key-here>"}}'
```

</details>

<details>
<summary><b>Hermes-Agent</b></summary>

Append under `mcp_servers` in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  gemina:
    url: "https://api.gemina.co/api/v1/mcp/"
    headers:
      X-API-Key: "<paste-your-key-here>"
```

</details>

For the full machine-readable install guide (used by agents), see [`llms-install.md`](./llms-install.md).

## Free tier

**1,500 tags per month. No credit card required.** Sign up at [gemina.co/filetag](https://www.gemina.co/filetag), grab an API key, paste it into your config. The same key works for both MCP and the REST API.

Need more? Paid plans add larger monthly allowances, configurable data residency, and longer retention. See [pricing](https://www.gemina.co/pricing).

## Use cases

The same MCP call (`tag_file` or `tag_url`) powers all of these. Each example has a dedicated walkthrough in [`examples/`](./examples).

| Use case | What it does | Example |
|---|---|---|
| 📥 **Email attachment triage** | Tag inbound attachments, route to folders by vendor/type | [`examples/gmail-attachment-triage`](./examples/gmail-attachment-triage) |
| 🔍 **RAG ingestion** | Attach structured metadata to vector store entries so retrieval can filter by vendor, date, or document type | [`examples/llamaindex-reader`](./examples/llamaindex-reader) · [`examples/langchain-loader`](./examples/langchain-loader) |
| 🧾 **Invoice automation** | Extract vendor, totals, line items; route to AP; export to accounting | [`examples/bulk-tag-folder`](./examples/bulk-tag-folder) |
| 📁 **Bulk document filing** | Walk a directory, rename every file to a consistent pattern | [`examples/bulk-tag-folder`](./examples/bulk-tag-folder) |
| ⚡ **Quickstart (curl)** | First tag in three minutes, no MCP client needed | [`examples/curl-quickstart`](./examples/curl-quickstart) |
| 🖥️ **Claude Desktop walkthrough** | Step-by-step setup with screenshots | [`examples/claude-desktop`](./examples/claude-desktop) |

## Why FileTag, not a raw LLM call?

A naive "ask GPT to tag this PDF" pipeline breaks in production: hallucinated vendor names, inconsistent date formats, no structured output, no PDF metadata embedding, no enriched-file roundtrip. FileTag is the harness around that call — specialized agents that **reason, cross-check, and refuse to guess** — wrapped in a single endpoint with a stable JSON contract.

| | Raw LLM | Gemina FileTag |
|---|---|---|
| Structured output | Free text, requires parsing | Stable JSON schema |
| Filename suggestions | None | Six patterns, ready to use |
| PDF metadata embedding | DIY | Returned as downloadable enriched copy |
| Hallucinations | Frequent | Cross-checked, refuses when unsure |
| Per-document cost | $$ per call | Free for first 1,500/month |

## Privacy & trust

- **No model training.** Your documents are never used to train AI models — Gemina's or anyone else's.
- **7-day deletion.** Files are deleted within 7 days of upload (configurable per plan).
- **Encryption.** AES-256 at rest, TLS 1.3 in transit.
- **Compliance.** GDPR and CCPA compliant. Configurable data residency on paid plans.

Full details on the [Gemina Trust Center](https://www.gemina.co/trust-center).

## Documentation

- 📖 **Full docs:** [gemina.co/docs/filetag](https://www.gemina.co/docs/filetag) — REST + MCP reference
- 🤖 **Agent install guide:** [`llms-install.md`](./llms-install.md) — machine-readable, used by AI agents auto-discovering the server
- 🔌 **MCP manifest:** [gemina.co/.well-known/mcp.json](https://www.gemina.co/.well-known/mcp.json)
- 🏷️ **REST endpoint reference:** [gemina.co/docs.md](https://www.gemina.co/docs.md)

## Community & support

- 🐛 [Bug reports](https://github.com/tommyil/gemina-mcp/issues/new?template=bug.yml)
- 🆘 [Integration help](https://github.com/tommyil/gemina-mcp/issues/new?template=integration_help.yml)
- 💬 [Discussions](https://github.com/tommyil/gemina-mcp/discussions)
- ✉️ Email: [info@gemina.co](mailto:info@gemina.co)
- 🔒 Security: see [SECURITY.md](./SECURITY.md)

## Contributing

Examples PRs welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md). The server itself is closed-source, so PRs that touch the actual MCP server logic will be declined, but bug reports against the live server are very welcome.

## License

MIT — see [LICENSE](./LICENSE). The MCP server itself is a hosted service governed by [Gemina's Terms of Service](https://www.gemina.co/terms-of-service).
