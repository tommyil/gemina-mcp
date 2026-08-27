# Claude Desktop walkthrough

A click-by-click guide to installing the Gemina MCP server in Claude Desktop (or claude.ai) and tagging your first document.

**Time:** ~2 minutes with OAuth sign-in; ~5 minutes on the `mcp-remote` fallback.

## Step 1 — Create a Gemina account

Open https://console.gemina.co/registration/create-account in your browser. Create an account (no credit card). That's all you need for the recommended path — no API key to copy.

> The free tier includes 1,500 FileTag tags per month.

## Step 2 — Add Gemina as a connector (recommended: OAuth)

claude.ai and Claude Desktop use the same Connectors flow — no config file, no `mcp-remote`, no Node.js.

```text
URL: https://api.gemina.co/api/v1/mcp/

1. Customize → Connectors
2. Add → Add custom connector
3. Paste the URL
4. Sign in
```

When prompted, sign in with the account from Step 1 and approve the consent page. Gemina creates an API key for the app when you approve it — you can see it (named "Claude (OAuth)" or similar) and revoke it under **Console → API Keys → Connected apps**.

The Gemina tools are available in new chats immediately — skip to [Step 5](#step-5--verify-the-connection). Steps 3–4 are only for the API-key fallback.

## Step 3 — Fallback: API key via `mcp-remote`

Use this only if you need a specific API key (for example a shared or headless machine). Claude Desktop's config file is stdio-only — it can't point straight at a remote HTTP server — and the Connectors UI can't send an `X-API-Key` header, so the key goes through the [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) stdio bridge, which needs **Node.js 18+** ([nodejs.org](https://nodejs.org/); on Windows keep "Add to PATH" checked).

Copy an API key from the Gemina console (the same key works for both MCP and the REST API), then locate Claude Desktop's config file:

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

If the file doesn't exist, create it with `{}` as its only content.

Open the config file in any editor and add the `mcpServers.gemina` block. If you already have other MCP servers configured, add Gemina alongside them. Replace `<paste-your-key-here>` with your key.

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

Save the file. On Windows, if Claude Desktop later logs `spawn npx ENOENT`, replace `"command": "npx"` with the absolute path printed by `where npx`.

## Step 4 — Restart Claude Desktop (fallback path only)

**Fully quit Claude Desktop and reopen it** (Cmd+Q on macOS, or right-click the tray icon → Quit on Windows). A reload doesn't pick up MCP config changes — you need a full restart. Connectors added through the UI in Step 2 don't need a restart.

## Step 5 — Verify the connection

In a new chat, click the **hammer icon** (or paperclip, depending on version) next to the input box. You should see the Gemina tools listed — 13 in total. The three FileTag tools (free tier) are the ones this walkthrough uses:

- `files_create_upload`
- `tag_file`
- `tag_url`

The remaining ten are the extraction (`files_create_extraction_upload`, `extract_document`, `get_extraction_result`, `list_extractions`, `get_extraction`, `get_document`, `submit_extraction_feedback`) and document-intelligence (`query_documents`, `aggregate_documents`, `index_document`) tools, which need a paid plan — see the [tool reference](../../README.md#tools).

If you don't see them, see [Troubleshooting](#troubleshooting) below. On the `mcp-remote` fallback path, the first launch may take 10–30 seconds while `npx` downloads `mcp-remote`.

## Step 6 — Tag your first document

Drag a PDF or image into the chat, then ask Claude:

> "Tag this file using the Gemina MCP server. Show me the structured metadata and the suggested filename."

Claude will call `files_create_upload`, upload the file, call `tag_file`, and return the JSON response with metadata, six filename patterns, and a download URL for the enriched copy.

## Troubleshooting

**The connector won't sign in (OAuth path).**
- Make sure the URL ends with the trailing slash: `https://api.gemina.co/api/v1/mcp/`.
- If the consent page says the request expired, remove the connector and add it again from Claude — don't reload the consent page.
- If you revoked the app's key under Console → API Keys → Connected apps, reconnect the connector to get a new one.
- Access tokens last 1 hour and refresh tokens 30 days; if calls start failing with 401 after a long gap, reconnect the connector.

**The Gemina tools don't appear after restart (`mcp-remote` path).**
1. Confirm the config file path matches your OS (see Step 3).
2. Validate the JSON — a missing comma or trailing comma breaks the whole file. Try `python -m json.tool < claude_desktop_config.json` (or paste it into [jsonlint.com](https://jsonlint.com)).
3. Confirm `npx --version` works in a terminal (Node.js 18+ is required for `mcp-remote`).
4. Check Claude Desktop's logs: macOS `~/Library/Logs/Claude/`, Windows `%APPDATA%\Claude\logs\`. Look for `MCP server "gemina"` entries.

**Tools appear but every call returns 401.**
- OAuth path: the token expired or the app's key was revoked — reconnect the connector.
- `mcp-remote` path: the API key is wrong or has a stray space/newline. Re-copy it from the Gemina console and replace it in the config.

**Tools appear but every call hangs.**
- Some networks block streaming HTTP. Try from a different network, or test the endpoint directly with the curl smoke-test in [curl-quickstart](../curl-quickstart).

**Out of free tier.**
- Free tier resets monthly. Upgrade at https://www.gemina.co/pricing if you need more.

## What's next

- Bulk-tag a folder: [bulk-tag-folder](../bulk-tag-folder)
- Use Gemina tags for RAG ingestion: [llamaindex-reader](../llamaindex-reader) · [langchain-loader](../langchain-loader)
- Read the full docs: https://www.gemina.co/docs/filetag

## Screenshots

> _Coming soon — screenshots of each step. PRs welcome (see [CONTRIBUTING.md](../../CONTRIBUTING.md))._
