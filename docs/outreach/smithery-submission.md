# Smithery submission notes

Source: https://smithery.ai/docs/build/publish (fetched 2026-08-26).

## How external (hosted) servers are listed

1. Go to https://smithery.ai/new, enter the public HTTPS URL
   `https://api.gemina.co/api/v1/mcp/`, complete the flow.
2. Requirements: Streamable HTTP transport ✓; **OAuth if authentication is
   required** (Smithery does not support header-only auth for hosted servers).
3. Smithery scans the server to extract metadata. **OAuth detection is the
   401 response**: the MCP authorization spec's 401 (not 403) with
   `WWW-Authenticate` → Smithery registers a client automatically via Client
   ID Metadata Documents and prompts the submitter to sign in during the scan.
   This is exactly what `api.staging.gemina.co` returns today and what prod
   must return before submitting (see `docs/publish-checklist.md` step 0).
4. Scanner user agent is `SmitheryBot/1.0`. If Cloudflare / WAF returns 403,
   allow that UA or fall back to the static server card.

## Static server card fallback: `/.well-known/mcp/server-card.json`

Served at `https://api.gemina.co/.well-known/mcp/server-card.json` (currently
**404**). Only needed if the authenticated scan cannot complete. Shape follows
the MCP SDK types:

- `serverInfo` (**required**): `{ "name": "gemina", "version": "2.0.0" }`
  (add `title: "Gemina"` — allowed by the `Implementation` type).
- `authentication` (optional): auth requirements and supported schemes, e.g.
  `{ "required": true, "schemes": ["oauth2"], "oauth2": { "resourceMetadata": "https://api.gemina.co/.well-known/oauth-protected-resource/api/v1/mcp" } }` plus a note that `X-API-Key` is accepted as an alternative.
- `tools` (optional): the 13 `Tool` objects exactly as `tools/list` returns
  them (name, description, inputSchema, annotations).
- `resources` (optional): none today (`[]`).
- `prompts` (optional): the 2 `Prompt` objects from `prompts/list`.

Cheapest implementation: have api-v2 serve the card by running the same
handler that answers the anonymous `/api/v1/mcp/public/` `tools/list` and
`prompts/list`, wrapped with `serverInfo` + `authentication`. Keep the
`Content-Type: application/json` and no auth on that path.

## Listing text

- Name: Gemina
- Summary: Extract, search and tag any document — invoices, receipts, contracts, forms, or your own templates. 13 tools, one sign-in, free FileTag tier, data residency in the EU, US, Israel or Asia.
- Homepage: https://www.gemina.co/product/agents
- Docs: https://www.gemina.co/docs/mcp
- Repo: https://github.com/tommyil/gemina-mcp
- Icon: https://www.gemina.co/assets/gemina-logo.png
- Long description: reuse `docs/outreach/mcp-so-listing.md`.

## Open items

- Smithery's OAuth scan will create a "Smithery (OAuth)" connected-app key
  under the submitter's Console → API Keys → Connected apps. Use a dedicated
  Gemina account for the submission, not a personal one.
- Confirm whether Smithery's dashboard lets us pick the "remote/external"
  release type explicitly (its API `POST /servers` supports `external` (URL)
  releases; the web flow should do the same).
