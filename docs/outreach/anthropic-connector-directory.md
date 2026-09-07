# Anthropic Connectors Directory submission notes

Source: https://claude.com/docs/connectors/building/submission and
https://claude.com/docs/connectors/building/review-criteria (fetched
2026-08-26). Submission is a portal, not a form/email:
**https://claude.ai/admin-settings/directory/submissions/new**. Escalations:
`mcp-review@anthropic.com`.

## Access prerequisites

- A **Team or Enterprise** Claude organisation (not an individual plan).
- Submitter must be an org **Owner / Primary owner** (Team has no custom
  roles; Enterprise can delegate a "Directory" role).
- No DNS / `.well-known` domain proof is required (that is only for the open
  MCP Registry).

## Blockers to clear BEFORE submitting (status 2026-08-26)

| Requirement | Status | Action |
|---|---|---|
| Privacy policy URL, HTTPS, covering collection, usage/storage, third-party sharing, retention, contact. "Missing or incomplete privacy policies result in immediate rejection." | ✓ https://www.gemina.co/privacy-policy returns 200 (verified 2026-08-26) | Confirm it covers collection/retention/contact before submitting. |
| Every tool must have `title` and `readOnlyHint: true` (read-only) or `destructiveHint: true` (writes/deletes). The portal auto-flags missing ones and blocks. | ✗ `tools/list` on `/api/v1/mcp/public/` shows **no `title` and no `annotations` on any of the 13 tools** | Add annotations server-side (api-v2 MCP tool definitions). Suggested: read-only = `get_extraction_result`, `list_extractions`, `get_extraction`, `get_document`, `query_documents`, `aggregate_documents`; write = `files_create_upload`, `files_create_extraction_upload`, `tag_file`, `tag_url`, `extract_document`, `submit_extraction_feedback`, `index_document` (none destructive; use `destructiveHint: false`, `idempotentHint` where true). |
| OAuth 2.0 for authenticated services | ✓ on staging; ✗ prod 401 lacks `WWW-Authenticate` and discovery URLs 404 | Deploy OAuth to prod (see `docs/publish-checklist.md` step 0). |
| Public documentation live by publish date | ✗ https://www.gemina.co/docs/mcp 404 | Website branch. |
| Fully populated **test account** with credentials + step-by-step reviewer instructions | pending | Create `mcp-review@` user on prod with a paid-tier plan and a handful of indexed sample documents so `query_documents` / `aggregate_documents` return data. |
| Separate read vs write tools (no catch-all `api_request`) | ✓ | None. |
| Tool names ≤ 64 chars | ✓ (longest: `files_create_extraction_upload`, 30) | None. |
| Server domain matches the service, first-party API | ✓ `api.gemina.co` | None. |
| Not money transfer / not AI media generation | ✓ | None. |

## Portal steps and what to enter

1. **Introduction**: acknowledge.
2. **Connection**: URL `https://api.gemina.co/api/v1/mcp/` (https, streamable
   HTTP), same URL for every user.
3. **Tools**: synced from the live server; grouped by annotation. Must show
   no "missing title/annotations" flags.
4. **Listing**
   - Name (≤100): `Gemina`
   - One-liner (≤200 in the portal, 2026-08-30): `Extract, search and tag any document — invoices, receipts, contracts, forms, or your own templates. 14 tools, one sign-in, free FileTag tier, data residency in the EU, US, Israel or Asia.`
   - Description (≤2000): reuse `docs/outreach/mcp-so-listing.md` description.
   - Categories (1–5): Productivity, Data & Analytics, Developer Tools,
     Finance (pick whatever the portal offers closest to these).
   - Documentation URL: `https://www.gemina.co/docs/mcp`
   - Privacy policy URL: `https://www.gemina.co/privacy-policy`
   - Support contact: `info@gemina.co` (or a dedicated `support@gemina.co`
     if one exists; confirm mailbox before submitting)
   - Icon: `assets/logo.png` (400x400 PNG; same as
     https://www.gemina.co/assets/gemina-logo.png)
   - Slug (permanent): `gemina`
5. **Use cases**: invoice/receipt data extraction into accounting and ERP
   flows; classifying and renaming inbound document drops; searching and
   aggregating a company's indexed invoices ("total spend with vendor X in
   Q2"); RAG ingestion metadata via FileTag. Users need a Gemina account
   (free tier covers FileTag; extraction and document intelligence need a
   paid plan). Reads **and** writes (uploads, extractions, indexing, feedback).
6. **Company**: Gemina, https://www.gemina.co, contact Tomer Sasson.
7. **Authentication**: OAuth with **Dynamic Client Registration** and
   **Client ID Metadata Documents** (both supported; no static client ID
   needed). Authorization server metadata at
   `https://api.gemina.co/.well-known/oauth-authorization-server/api/v1/mcp`,
   protected-resource metadata at
   `https://api.gemina.co/.well-known/oauth-protected-resource/api/v1/mcp`,
   scope `mcp`. The server does not start unauthenticated.
8. **Data handling**: first-party API (our own); no personal health data; no
   sponsored content. Documents users upload are processed by Gemina; see the
   privacy policy for retention.
9. **Test & launch**: test-account credentials + steps: sign in via OAuth,
   run `tag_url` on `https://www.gemina.co/samples/invoice.pdf` (or the repo
   `assets/sample-input/invoice.pdf` raw URL), then `extract_document` on an
   uploaded slot, then `query_documents`. Confirm every tool was exercised
   via MCP Inspector and as a custom connector in Claude.
10. **Compliance**: seven acknowledgments (directory guidelines, first-party
    API usage, financial transactions, AI media generation, prompt injection,
    conversation data collection, public documentation). All required.
11. **Review**: submit. Default outcome is a **Community** listing; Anthropic
    may escalate to Verified review automatically.

## Egress note (for the description / docs, not a portal field)

Tool results include short-lived `storage.googleapis.com` URLs for the
enriched file / extraction artefacts. Claude Desktop needs
**Settings → Capabilities → Allow network egress** with
`storage.googleapis.com` allowed (or "All domains") to download them;
otherwise the tool call succeeds but the download fails with "Host not in
allowlist". Capability changes only apply to new chats. `ui/open-link` is not
used, so no "allowed link URIs" entry is needed.
