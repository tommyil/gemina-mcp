# Changelog

All notable changes to this repository — and to the Gemina MCP server's public contract — will be documented here. We follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for the server's response shape.

## [Unreleased]

## [2.0.2] - 2026-08-30

- Registry description repositioned from "invoice OCR" to any-document extraction, search and tagging (custom templates); canonical listing copy in `docs/outreach/listing-copy.md` (data residency: EU, US, Israel, Asia).

## [2.0.1] - 2026-08-28

### Changed
- Registry manifest: icon and documentation now point at the live website (`www.gemina.co/assets/gemina-logo.png`, `www.gemina.co/docs/mcp`) instead of the 2.0.0 stand-ins. No server changes.

## [2.0.0] - 2026-08-27

### Changed
- **OAuth 2.1 sign-in (DCR + CIMD) is the default; API key remains supported.** README, `llms-install.md`, the Claude Desktop walkthrough, and the integration-help issue template now lead with the OAuth form of every client snippet (no headers — the client discovers the authorization server via RFC 9728/8414 and prompts a browser sign-in) and keep the `X-API-Key` snippet as the headless lane. Claude Desktop / claude.ai install through **Settings → Connectors → Add custom connector** with no `mcp-remote`; the bridge stays documented as the API-key fallback. Reverses the 2026-05 'Connectors UI cannot be used' guidance (33ff119). Each connected app gets its own key, `<app> (OAuth)`, under Console → API Keys → Connected apps.
- CI (`validate.yml`): the trailing-slash guard now exempts the RFC 9728/8414 discovery URLs (`/.well-known/oauth-protected-resource/api/v1/mcp` and `/.well-known/oauth-authorization-server/api/v1/mcp`), whose resource path legitimately has no trailing slash.
- **Rebrand: the server is "Gemina" (FileTag = free tier).** All prose now names the product "Gemina" — one unified MCP server whose free tier is FileTag (`tag_file`/`tag_url`) and whose paid tiers add extraction and document intelligence. Tool names, the `/api/v1/filetag` REST path, the `GeminaFileTagReader`/`GeminaFileTagLoader` classes, the `filetag_document_id` metadata key, and the `FileTag/*` Gmail labels are user-facing contracts and are unchanged. Commit 2f19d3d already renamed the config identifier to `gemina` for this reason.
- Documented the full tool surface: 13 tools across three groups (FileTag, Extraction, Document Intelligence) plus 2 prompts, in README, `llms-install.md`, and the Claude Desktop walkthrough. Previously only the three FileTag tools were listed.
- The "1,500/month" claim is now scoped to the free tier's FileTag tags rather than the server as a whole. Paid pricing lives at https://www.gemina.co/pricing.
- Removed `assets/filetag-og.png` (byte-identical duplicate of `assets/social-preview.png`, unreferenced).
- CI (`validate.yml`): new guard fails on any `/api/v1/mcp/` URL missing its trailing slash; JSON-snippet validation now covers README.md code blocks as well as `llms-install.md`.

### Added
- Registry manifests for the rename: `server.json` is now `co.gemina/gemina` 2.0.0 (OAuth-first, `X-API-Key` optional); `server.legacy.json` republishes `co.gemina/filetag` as 1.0.3 pointing at the new name. `glama.json` lists all 13 tools grouped free/paid plus OAuth metadata. `docs/publish-checklist.md` and `docs/outreach/` hold the publish-day runbook and directory drafts.
- HEIC, HEIF, and AVIF input support (`image/heic`, `image/heif`, `image/avif`; extensions `.heic`, `.heif`, `.hif`, `.avif`). Advertised in `glama.json` `supportedFileTypes`, README, `llms-install.md`, and all example scripts. Enriched copies of HEIC/AVIF inputs are returned renamed but without embedded metadata.

### Fixed
- Cline install snippet now includes `"type": "streamableHttp"` (required for Cline to recognize the remote MCP server). README and `llms-install.md` both updated; `llms-install.md` gains a dedicated Cline section.
- Claude Desktop install instructions rewritten end-to-end. Confirmed via live testing:
    - Custom Connectors UI (**Customize → Connectors**) is OAuth-only and does not accept `X-API-Key` — it cannot authenticate against Gemina. README and `llms-install.md` drop the UI path entirely and make the `mcp-remote` stdio bridge the only documented option. *(Superseded in this same release: OAuth via Connectors is now the default install path; `mcp-remote` remains the API-key fallback — see Changed above.)*
    - Added prerequisites: Node.js 18+ and the **Settings → Capabilities → Allow network egress** toggle (with `storage.googleapis.com` in the allowlist or "All domains" selected). Without egress, tag results return correctly but Claude can't download the enriched-file URL — fails with "Host not in allowlist". Capability changes only apply to new chats.
    - Added Windows-specific guidance for `spawn npx ENOENT`: replace `"command": "npx"` with the absolute path from `where npx`.

### Changed
- Renamed the MCP server identifier back to `gemina` (from the short-lived `FileTag`). Lowercase matches the ecosystem convention used in every official MCP example (`filesystem`, `brave-search`, `github`, `postgres`) and aligns with the endpoint URL (`api.gemina.co`). Future-proofs the local-config key for when the MCP surface expands beyond FileTag to cover the full Gemina platform — by then a per-feature identifier would be misleading. Affects every install snippet (Claude Desktop, Cursor, Claude Code CLI, VS Code, Cline, Codex CLI, Windsurf, OpenClaw, Hermes-Agent); endpoint URL and product naming unchanged.

## [1.0.2] — 2026-05-19

### Changed
- Moved registry icon from `raw.githubusercontent.com/tommyil/gemina-mcp/...` to `https://www.gemina.co/assets/filetag-logo.png`. Stable, branded URL that survives any future repo rename or org move.

## [1.0.1] — 2026-05-19

### Added
- `icons` array on `server.json` pointing at the 400×400 logo so registry-aware clients (Smithery, Glama, Cline) can render it in listings.

### Changed
- Bumped `server.json` schema to `2025-12-11/server.schema.json` (was draft `2025-06-18`).
- Stripped `server.json` to schema-compliant fields only; trimmed `description` to ≤100 chars to pass registry validation.
- Migrated the rich metadata (vendor, tools, supported file types, rate limits, pricing, keywords) into `glama.json`.

## [1.0.0] — 2026-05-19

### Added
- Initial public release of the discovery and install repository.
- README with quick install snippets for nine MCP clients (Claude Desktop, Cursor, Claude Code, VS Code, Cline, Windsurf, Codex CLI, OpenClaw, Hermes-Agent).
- `llms-install.md` for AI agent auto-discovery.
- MCP registry manifest (`server.json`) and Glama manifest (`glama.json`).
- Example workflows: `curl-quickstart`, `bulk-tag-folder`, `claude-desktop`, `gmail-attachment-triage`, `llamaindex-reader`, `langchain-loader`.
- GitHub Actions workflows for linting examples, validating install snippets, and weekly link checks.
- 400×400 PNG logos (`assets/logo.png` and `assets/logo-dark.png`) for marketplace listings.
- Synthetic sample PDFs (`assets/sample-input/{invoice,receipt,contract}.pdf`) and a ReportLab generator script.

## Server contract — release history

The Gemina MCP server is a hosted service; only server-side changes that affect clients or break backward compatibility are recorded here.

- **2026-08** — Tool surface expanded from 3 to 13 tools (+ 2 prompts) on the same endpoint. Added Extraction: `files_create_extraction_upload`, `extract_document`, `get_extraction_result`, `list_extractions`, `get_extraction`, `get_document`, `submit_extraction_feedback`; Document Intelligence: `query_documents`, `aggregate_documents`, `index_document`. Prompts: `explain_filename_patterns`, `explain_upload_flow`. FileTag tools and auth unchanged.
- **2026-05** — Public launch. Endpoint: `https://api.gemina.co/api/v1/mcp/`. Tools: `files_create_upload`, `tag_file`, `tag_url`. Auth: `X-API-Key` or `Authorization: Bearer`. Free tier: 1,500 calls/month.

[Unreleased]: https://github.com/tommyil/gemina-mcp/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/tommyil/gemina-mcp/compare/v1.0.2...v2.0.0
[1.0.2]: https://github.com/tommyil/gemina-mcp/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/tommyil/gemina-mcp/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/tommyil/gemina-mcp/releases/tag/v1.0.0
