# Cline MCP Marketplace

## Comment for cline/mcp-marketplace#1646 (the open FileTag submission)

Update for the reviewer: this submission has been renamed. The server is now
**Gemina** (was "FileTag"; FileTag is its free tier).

- **Repo:** https://github.com/tommyil/gemina-mcp (unchanged). README and
  `llms-install.md` are updated; Cline installs it as a remote server with
  `"type": "streamableHttp"` per the README's Cline section.
- **Registry name:** `co.gemina/gemina` 2.0.0 in the official MCP Registry
  (`co.gemina/filetag` is deprecated and points at it).
- **Auth:** OAuth 2.1 (DCR + CIMD; connect with no headers and sign in) **or**
  an `X-API-Key` header for headless use. Free tier needs no credit card.
- **Tools:** 13 on one endpoint, `https://api.gemina.co/api/v1/mcp/`:
  - FileTag (free): `files_create_upload`, `tag_file`, `tag_url`
  - Extraction: `files_create_extraction_upload`, `extract_document`,
    `get_extraction_result`, `list_extractions`, `get_extraction`,
    `get_document`, `submit_extraction_feedback`
  - Document Intelligence: `query_documents`, `aggregate_documents`,
    `index_document`
  - plus 2 prompts: `explain_filename_patterns`, `explain_upload_flow`
- **Credential-free review:** `https://api.gemina.co/api/v1/mcp/public/`
  serves `initialize` / `tools/list` / `prompts/list` anonymously (refuses
  `tools/call`), so the tool surface can be inspected without an account.
- **Logo:** https://www.gemina.co/assets/gemina-logo.png (400x400 PNG).

Please treat this issue as the canonical submission and use the name
"Gemina". Happy to provide a test key if you want to exercise `tools/call`.

## Close comment for cline/mcp-marketplace#1617 (duplicate)

Duplicate of #1646 (same server, now named Gemina); closing this one so the
submission is tracked in a single issue.
