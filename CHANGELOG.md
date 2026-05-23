# Changelog

All notable changes to this repository — and to the Gemina FileTag MCP server's public contract — will be documented here. We follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for the server's response shape.

## [Unreleased]

### Fixed
- Cline install snippet now includes `"type": "streamableHttp"` (required for Cline to recognize the remote MCP server). README and `llms-install.md` both updated; `llms-install.md` gains a dedicated Cline section.

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

The Gemina FileTag MCP server is a hosted service; only server-side changes that affect clients or break backward compatibility are recorded here.

- **2026-05** — Public launch. Endpoint: `https://api.gemina.co/api/v1/mcp/`. Tools: `files_create_upload`, `tag_file`, `tag_url`. Auth: `X-API-Key` or `Authorization: Bearer`. Free tier: 1,500 calls/month.

[Unreleased]: https://github.com/tommyil/gemina-mcp/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/tommyil/gemina-mcp/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/tommyil/gemina-mcp/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/tommyil/gemina-mcp/releases/tag/v1.0.0
