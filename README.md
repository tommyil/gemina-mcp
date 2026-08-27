<div align="center">
  <img src="assets/logo/logo.svg" alt="Gemina" width="120" />

# Gemina — MCP server

**Tag, extract, and search your documents from any MCP client. Free tier: 1,500 FileTag tags/month, no credit card.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Free tier](https://img.shields.io/badge/free%20tier-1%2C500%20tags%2Fmonth-brightgreen.svg)](https://www.gemina.co/filetag)
[![MCP](https://img.shields.io/badge/MCP-Streamable%20HTTP-purple.svg)](https://modelcontextprotocol.io)
[![Last commit](https://img.shields.io/github/last-commit/tommyil/gemina-mcp.svg)](https://github.com/tommyil/gemina-mcp/commits/main)

[Install](#quick-install) • [Examples](./examples) • [Product page](https://www.gemina.co/filetag) • [Full docs](https://www.gemina.co/docs/filetag)

</div>

---

## What is this?

This repository is the **discovery, install, and examples surface** for Gemina's MCP server. The server itself is hosted at `https://api.gemina.co/api/v1/mcp/` — there is no daemon to run locally. Point your MCP-compatible client at the endpoint, sign in with your Gemina account (or paste an API key for headless use), and tag your first document in under a minute.

One server, three tool groups: **FileTag** (free tier — tag, rename, and enrich any PDF or image), **Extraction** (Core-OCR: invoice headers, line items, full text, custom templates), and **Document Intelligence** (search and aggregate over your indexed documents). See [Tools](#tools) for the full list.

The server itself is closed-source (operated by Gemina). Everything in this repo — install snippets, examples, integration code — is MIT-licensed and contributions are welcome.

## What you get

Send a PDF or image. Get back structured metadata, six suggested filenames, and a downloadable copy with metadata already embedded in the file itself.

<details>
<summary><b>Sample input → sample output</b> (click to expand)</summary>

**Input:** any PDF or image up to 50 MB (PDF, PNG, JPEG, GIF, WebP, HEIC, AVIF).

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

**Sign in with your Gemina account** — no API key to copy. Every snippet below points your client at the endpoint; the client discovers Gemina's authorization server and opens a browser sign-in. Don't have an account? Create one free (no credit card) at **https://console.gemina.co/registration/create-account**.

Running headless (CI, servers, scripts, or a client that doesn't prompt to sign in)? Use the **API-key form** shown under each client instead.

**Endpoint:** `https://api.gemina.co/api/v1/mcp/` · **Transport:** Streamable HTTP · **Auth:** OAuth 2.1 sign-in (default) *or* `X-API-Key` header (headless)

<details>
<summary><b>How OAuth sign-in works</b> (click to expand)</summary>

- Clients discover the authorization server from the MCP URL via RFC 9728 (protected-resource metadata) and RFC 8414 (authorization-server metadata):
  - `https://api.gemina.co/.well-known/oauth-protected-resource/api/v1/mcp`
  - `https://api.gemina.co/.well-known/oauth-authorization-server/api/v1/mcp`
- Dynamic Client Registration (DCR) and Client ID Metadata Documents (CIMD) are both supported — no pre-registration, no client ID/secret to paste.
- Scope: `mcp`. Access tokens last 1 hour; refresh tokens rotate and last 30 days.
- Each connected app gets its own API key named `<app> (OAuth)`. See and revoke them under **Console → API Keys → Connected apps** at https://console.gemina.co.

</details>

<details>
<summary><b>Claude Desktop / claude.ai</b></summary>

**Recommended: OAuth via Connectors.** claude.ai and Claude Desktop use the same flow — no config file, no `mcp-remote`, no API key. Gemina creates a key for the app when you approve it.

```text
URL: https://api.gemina.co/api/v1/mcp/

1. Customize → Connectors
2. Add → Add custom connector
3. Paste the URL
4. Sign in
```

Sign in with your Gemina account when prompted and approve the consent page. The Gemina tools appear in new chats immediately.

**Fallback: API key via `mcp-remote`.** Claude Desktop's Connectors UI doesn't accept custom headers, so an API key has to go through the `mcp-remote` stdio bridge. Use this only if you need a specific key (headless or shared machines).

**Prerequisites**

1. **Node.js 18+** — install from [nodejs.org](https://nodejs.org/) (Windows: ensure "Add to PATH" stays checked; macOS/Linux: standard installer).
2. **Claude Desktop capabilities** — open **Settings → Capabilities** and turn on:
    - Code execution and file creation
    - Allow network egress
    - Domain allowlist: **All domains** (or add `storage.googleapis.com` to the narrow allowlist — that's where signed enriched-file URLs are hosted).

   Without network egress, `tag_file`/`tag_url` return JSON correctly but Claude can't fetch the enriched-file URL from storage and you'll see "Host not in allowlist". Settings only apply to **new** chats — start a fresh conversation after toggling.

**Config**

In Claude Desktop, **Settings → Developer → Edit Config** opens `claude_desktop_config.json` at:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Merge the `mcpServers` block alongside any existing config:

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

Save → fully quit Claude Desktop (Cmd+Q / right-click tray → Quit) → relaunch. First launch may take 10–30s while `npx` downloads `mcp-remote`.

**Notes**

- No space after `X-API-Key:` in the `--header` arg — it's the documented workaround for `npx`'s shell-split parsing.
- The env-var indirection (`${GEMINA_API_KEY}`) keeps the literal key out of `args`, where it could leak via process listings.
- **Windows + `spawn npx ENOENT`**: Claude Desktop doesn't inherit your shell's PATH. Replace `"command": "npx"` with the absolute path from `where npx` in PowerShell (forward slashes work in JSON), e.g. `"C:/Program Files/nodejs/npx.cmd"`.

</details>

<details>
<summary><b>Claude Code (CLI)</b></summary>

**OAuth (default):** register the server, then run `/mcp` and sign in — Claude Code opens the Gemina sign-in in your browser.

```bash
claude mcp add --transport http gemina https://api.gemina.co/api/v1/mcp/
# then run /mcp and sign in
```

Inside Claude Code: `/mcp` → select **gemina** → **Authenticate** → sign in with your Gemina account in the browser → approve the consent page.

**API key (headless):**

```bash
claude mcp add --transport http gemina https://api.gemina.co/api/v1/mcp/ \
  --header "X-API-Key: <paste-your-key-here>"
```

</details>

<details>
<summary><b>Cursor</b></summary>

File: `~/.cursor/mcp.json` (all projects) or `.cursor/mcp.json` (one project). Cursor registers itself dynamically and opens your browser on the first 401 — no client ID or secret in the file.

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

</details>

<details>
<summary><b>VS Code</b></summary>

File: `.vscode/mcp.json` (per workspace), or run **MCP: Open User Configuration** from the Command Palette for all of them. VS Code registers dynamically and opens a browser on first connection; confirm the trust prompt, then find the account under **Accounts → Manage Trusted MCP Servers**.

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

</details>

<details>
<summary><b>Cline</b></summary>

In Cline's MCP settings (gear icon → MCP Servers → Edit Config), add:

**OAuth (default):**

> **Cline is API-key only.** As of 2026-08-27 Cline has no documented OAuth path
> for remote MCP servers — its MCP docs never mention OAuth, and the one release
> note that does (v4.1.7) names the legacy SSE transport, not `streamableHttp`.
> Use the API-key form below.


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

</details>

<details>
<summary><b>Windsurf</b></summary>

File: `~/.codeium/windsurf/mcp_config.json`, or the MCPs icon in the Cascade panel. Remote servers take `serverUrl` (`url` also works), then reload the MCP list. Now shipped as **Devin Desktop** — the Windsurf docs redirect there.

The docs say Cascade "supports OAuth for each transport type" but describe no explicit sign-in step, so if no browser prompt appears, use the API-key form.

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

</details>

<details>
<summary><b>Codex CLI</b></summary>

**OAuth (default):**

```bash
codex mcp add gemina --url https://api.gemina.co/api/v1/mcp/
codex mcp login gemina
```

`codex mcp add` detects OAuth on the URL and usually starts the browser sign-in by itself; `codex mcp login` is the documented guarantee. Do **not** paste a bare `[mcp_servers.gemina]` block for OAuth — Codex will connect to the server *unauthenticated* and every tool call fails. Verified against codex-cli 0.150.1 on 2026-08-27.

For the API-key lane, append to `~/.codex/config.toml`:

**API key (headless):**

```toml
[mcp_servers.gemina]
url = "https://api.gemina.co/api/v1/mcp/"
http_headers = { "X-API-Key" = "<paste-your-key-here>" }
```

</details>

<details>
<summary><b>OpenClaw</b></summary>

**OAuth (default):**

```bash
openclaw mcp set gemina '{"url":"https://api.gemina.co/api/v1/mcp/","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login gemina
```

Both lines are required. `mcp set` stores the server with `auth: "oauth"`; `mcp login` runs the flow — OpenClaw does not start OAuth off a 401 on its own. On a headless box, pass the code back with `openclaw mcp login gemina --code <code>`, and check it with `openclaw mcp doctor gemina --probe`.

**API key (headless):**

```bash
openclaw mcp set gemina '{"url":"https://api.gemina.co/api/v1/mcp/","transport":"streamable-http","headers":{"X-API-Key":"<paste-your-key-here>"}}'
```

</details>

<details>
<summary><b>Hermes-Agent</b></summary>

Append under `mcp_servers` in `~/.hermes/config.yaml`:

**OAuth (default):**

```yaml
mcp_servers:
  gemina:
    url: "https://api.gemina.co/api/v1/mcp/"
    auth: oauth
```

Then run `hermes mcp login gemina` from a **fresh** terminal, not inside a live session — the in-session config reload times out at 30s, too short for a browser sign-in. The `auth: oauth` line is what turns OAuth on; Hermes never infers it from a 401.

**API key (headless):**

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

**Free tier: 1,500 FileTag tags per month. No credit card required.** Sign up at [gemina.co/filetag](https://www.gemina.co/filetag), then sign in from your MCP client — or grab an API key for headless use. The same key works for both MCP and the REST API.

Need more? Paid plans add larger monthly allowances, the extraction and document-intelligence tools, configurable data residency, and longer retention. See [pricing](https://www.gemina.co/pricing).

## Tools

One endpoint, 13 tools in three groups, plus 2 prompts. Every tool is listed for every key; the extraction and document-intelligence groups require a paid plan (see [pricing](https://www.gemina.co/pricing)). Anonymous discovery (`tools/list`, `prompts/list`) is available at `https://api.gemina.co/api/v1/mcp/public/`.

**FileTag (free tier)**

| Tool | What it does |
|---|---|
| `files_create_upload` | Reserve a pre-signed PUT slot for a file you'll tag. Returns `file_id`, the upload URL, and the headers to echo on the PUT. |
| `tag_file` | Run the FileTag pipeline on an uploaded slot: metadata, six filename patterns, and a short-lived enriched-file URL. |
| `tag_url` | Fetch a public HTTPS URL server-side and tag it — the bytes never pass through the model context. |

**Extraction (Core-OCR)**

| Tool | What it does |
|---|---|
| `files_create_extraction_upload` | Reserve a pre-signed PUT slot for extraction (distinct from the FileTag slot). |
| `extract_document` | Run one or more extraction types on an uploaded slot: `ocr`, `invoice_headers`, `invoice_line_items`, `document_details_hebrew`, `document_line_items_hebrew`, `custom_template`. |
| `get_extraction_result` | Poll an asynchronous extraction by `meta.correlationId`. |
| `list_extractions` | List past extractions, newest first, with filters and pagination. |
| `get_extraction` | Fetch one extraction by id, including the full extracted data. |
| `get_document` | Fetch one document by id, including all of its extractions. |
| `submit_extraction_feedback` | Send verified/corrected field values back — the extraction-quality feedback loop. |

**Document Intelligence**

| Tool | What it does |
|---|---|
| `query_documents` | Search your indexed documents: `structured` filters, `semantic` similarity, or `hybrid` (best default). |
| `aggregate_documents` | Sums/averages/min/max/counts over indexed documents, grouped by vendor, currency, type, month, and more. |
| `index_document` | (Re)index one document into the searchable index — after corrections or to backfill. |

**Prompts:** `explain_filename_patterns` (the six filename patterns and when to use each) · `explain_upload_flow` (`files_create_upload` → PUT → `tag_file`).

The full reference for each group is in [`llms-install.md`](./llms-install.md#3-tools-exposed).

## Use cases

The same FileTag tools (`tag_file` or `tag_url`) power all of these. Each example has a dedicated walkthrough in [`examples/`](./examples).

| Use case | What it does | Example |
|---|---|---|
| 📥 **Email attachment triage** | Tag inbound attachments, route to folders by vendor/type | [`examples/gmail-attachment-triage`](./examples/gmail-attachment-triage) |
| 🔍 **RAG ingestion** | Attach structured metadata to vector store entries so retrieval can filter by vendor, date, or document type | [`examples/llamaindex-reader`](./examples/llamaindex-reader) · [`examples/langchain-loader`](./examples/langchain-loader) |
| 🧾 **Invoice automation** | Extract vendor, totals, line items; route to AP; export to accounting | [`examples/bulk-tag-folder`](./examples/bulk-tag-folder) |
| 📁 **Bulk document filing** | Walk a directory, rename every file to a consistent pattern | [`examples/bulk-tag-folder`](./examples/bulk-tag-folder) |
| ⚡ **Quickstart (curl)** | First tag in three minutes, no MCP client needed | [`examples/curl-quickstart`](./examples/curl-quickstart) |
| 🖥️ **Claude Desktop walkthrough** | Step-by-step setup with screenshots | [`examples/claude-desktop`](./examples/claude-desktop) |

## Why Gemina, not a raw LLM call?

A naive "ask GPT to tag this PDF" pipeline breaks in production: hallucinated vendor names, inconsistent date formats, no structured output, no PDF metadata embedding, no enriched-file roundtrip. FileTag is the harness around that call — specialized agents that **reason, cross-check, and refuse to guess** — wrapped in a single endpoint with a stable JSON contract.

| | Raw LLM | Gemina |
|---|---|---|
| Structured output | Free text, requires parsing | Stable JSON schema |
| Filename suggestions | None | Six patterns, ready to use |
| PDF metadata embedding | DIY | Returned as downloadable enriched copy |
| Hallucinations | Frequent | Cross-checked, refuses when unsure |
| Per-document cost | $$ per call | Free tier: first 1,500 FileTag tags/month |

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

## For aggregators and directory listings

The `Dockerfile` at the repo root is **not for end users.** It exists so directory operators (e.g. Glama's `/mcp/servers/` tier) can build a container that introspects the public tool surface without provisioning credentials. The container runs [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) against `https://api.gemina.co/api/v1/mcp/public/` — a read-only discovery endpoint that serves `initialize` / `tools/list` / `prompts/list` to anonymous callers but refuses `tools/call`. End users should follow the **Quick install** section above and connect to the authenticated endpoint by signing in (or with their personal API key).

## Contributing

Examples PRs welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md). The server itself is closed-source, so PRs that touch the actual MCP server logic will be declined, but bug reports against the live server are very welcome.

## License

The contents of this repository — install snippets, example code, documentation, configuration files, and sample assets — are released under the [MIT License](./LICENSE).

The Gemina MCP server itself is a hosted closed-source service operated by Gemina (https://gemina.co) and is **not** covered by this license. Use of the server is governed by [Gemina's Terms of Service](https://www.gemina.co/terms-of-service) and [Privacy Policy](https://www.gemina.co/privacy-policy).
