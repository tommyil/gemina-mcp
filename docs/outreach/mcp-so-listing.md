# mcp.so listing

**Title:** Gemina

**Tagline (short):** Invoice OCR, document extraction, search and free FileTag tagging for AI agents.

**Server URL:** https://api.gemina.co/api/v1/mcp/
**Transport:** Streamable HTTP (remote, hosted)
**Repository:** https://github.com/tommyil/gemina-mcp
**Homepage:** https://www.gemina.co/product/agents
**Docs:** https://www.gemina.co/docs/mcp
**Logo:** https://www.gemina.co/assets/gemina-logo.png
**Registry name:** co.gemina/gemina
**Tags:** invoice-ocr, document-extraction, document-search, oauth, pdf, metadata, tagging, rag, document-ai

**Description:**

Gemina is a hosted MCP server for document-heavy agent workflows. One
Streamable HTTP endpoint, 13 tools in three groups:

- **FileTag (free tier, 1,500 tags/month, no credit card):** turn any PDF or
  image into structured metadata, six suggested filenames, and a
  metadata-embedded copy. Upload a file (`files_create_upload` → `tag_file`)
  or point at a public URL (`tag_url`).
- **Extraction:** OCR, invoice headers, invoice line items, Hebrew document
  details/line items, and custom templates (`extract_document`,
  `get_extraction_result`, `list_extractions`, `get_extraction`,
  `get_document`, `submit_extraction_feedback`).
- **Document Intelligence:** search your indexed documents with structured,
  semantic, or hybrid queries (`query_documents`), run sums/averages/counts
  grouped by vendor, currency, type or month (`aggregate_documents`), and
  (re)index documents (`index_document`).

Sign in with **OAuth 2.1** (no headers; works with Claude Code `/mcp`,
claude.ai / Claude Desktop connectors, Cursor, VS Code) or send an
**`X-API-Key`** header for headless use. Supports PDF, PNG, JPEG, GIF, WebP,
HEIC/HEIF and AVIF up to 50 MB. Anonymous `tools/list` at
`https://api.gemina.co/api/v1/mcp/public/`.
