# Claude Desktop walkthrough

A click-by-click guide to installing the Gemina FileTag MCP server in Claude Desktop and tagging your first document.

**Time:** ~5 minutes.

## Step 1 — Get an API key

Open https://console.gemina.co/registration/create-account in your browser. Create an account (no credit card). You'll land on the dashboard with your API key visible. Copy it.

> The free tier includes 1,500 tags per month. The same key works for both MCP and the REST API.

## Step 2 — Locate Claude Desktop's config file

Claude Desktop reads MCP server config from a single JSON file:

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

If the file doesn't exist, create it with `{}` as its only content.

## Step 3 — Add the Gemina server entry

Open the config file in any editor and add the `mcpServers.gemina` block. If you already have other MCP servers configured, add Gemina alongside them.

```json
{
  "mcpServers": {
    "gemina": {
      "url": "https://api.gemina.co/api/v1/mcp/",
      "headers": {
        "X-API-Key": "paste-your-key-here"
      }
    }
  }
}
```

Save the file.

## Step 4 — Restart Claude Desktop

**Fully quit Claude Desktop and reopen it.** A reload doesn't pick up MCP config changes — you need a full restart.

## Step 5 — Verify the connection

In a new chat, click the **hammer icon** (or paperclip, depending on version) next to the input box. You should see three Gemina tools available:

- `files_create_upload`
- `tag_file`
- `tag_url`

If you don't see them, see [Troubleshooting](#troubleshooting) below.

## Step 6 — Tag your first document

Drag a PDF or image into the chat, then ask Claude:

> "Tag this file using the Gemina MCP server. Show me the structured metadata and the suggested filename."

Claude will call `files_create_upload`, upload the file, call `tag_file`, and return the JSON response with metadata, six filename patterns, and a download URL for the enriched copy.

## Troubleshooting

**The Gemina tools don't appear after restart.**
1. Confirm the config file path matches your OS (see Step 2).
2. Validate the JSON — a missing comma or trailing comma breaks the whole file. Try `python -m json.tool < claude_desktop_config.json` (or paste it into [jsonlint.com](https://jsonlint.com)).
3. Check Claude Desktop's logs: macOS `~/Library/Logs/Claude/`, Windows `%APPDATA%\Claude\logs\`. Look for `MCP server "gemina"` entries.

**Tools appear but every call returns 401.**
- The API key is wrong or has a stray space/newline. Re-copy it from the Gemina console and replace it in the config.

**Tools appear but every call hangs.**
- Some networks block streaming HTTP. Try from a different network, or test the endpoint directly with the curl smoke-test in [curl-quickstart](../curl-quickstart).

**Out of free tier.**
- Free tier resets monthly. Upgrade at https://www.gemina.co/pricing if you need more.

## What's next

- Bulk-tag a folder: [bulk-tag-folder](../bulk-tag-folder)
- Use FileTag for RAG ingestion: [llamaindex-reader](../llamaindex-reader) · [langchain-loader](../langchain-loader)
- Read the full docs: https://www.gemina.co/docs/filetag

## Screenshots

> _Coming soon — screenshots of each step. PRs welcome (see [CONTRIBUTING.md](../../CONTRIBUTING.md))._
