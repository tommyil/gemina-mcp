# Glama: rename slug + re-scan

**To:** support@glama.ai
**Subject:** Rename `co.gemina/filetag` → `co.gemina/gemina` (OAuth now supported) and re-run health check

Hi Glama team,

We maintain the Gemina remote MCP server, currently listed from
https://github.com/tommyil/gemina-mcp under the slug `co.gemina/filetag`.

We have just published version 2.0.0 to the official MCP Registry under a new
name, **`co.gemina/gemina`**, and republished `co.gemina/filetag` as 1.0.3
with a description pointing at the new name (it is marked `deprecated` in the
registry). Same server, same endpoint (`https://api.gemina.co/api/v1/mcp/`),
new name because the product outgrew FileTag: it now exposes 13 tools in three
groups (FileTag, Extraction, Document Intelligence) plus 2 prompts.

Could you please:

1. **Rename the listing slug** from `co.gemina/filetag` to `co.gemina/gemina`
   (display name "Gemina"), or point the old slug at the new one so existing
   links and the README badge keep resolving.
2. **Note that OAuth 2.1 is now supported.** Clients can connect with no
   headers; the server returns a 401 with `WWW-Authenticate` +
   `resource_metadata` (RFC 9728) and supports Dynamic Client Registration and
   Client ID Metadata Documents. The `X-API-Key` header remains as the
   headless alternative. `glama.json` in the repo describes both.
3. **Re-run the health / introspection scan.** Anonymous `initialize`,
   `tools/list` and `prompts/list` are served at
   `https://api.gemina.co/api/v1/mcp/public/` (the repo `Dockerfile` targets it),
   so the scan needs no credentials. If you would rather scan the
   authenticated endpoint, reply and we will issue a test API key for your
   scanner.

Updated metadata: homepage https://www.gemina.co/product/agents, docs
https://www.gemina.co/docs/mcp, logo
https://www.gemina.co/assets/gemina-logo.png (400x400).

Thanks,
Tomer Sasson
CTO, Gemina · info@gemina.co
