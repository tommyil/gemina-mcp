# Changelog

All notable changes to this repository — and to the Gemina FileTag MCP server's public contract — will be documented here. We follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for the server's response shape.

## [Unreleased]

### Added
- Initial public release of the discovery and install repository.
- README with quick install snippets for nine MCP clients (Claude Desktop, Cursor, Claude Code, VS Code, Cline, Windsurf, Codex CLI, OpenClaw, Hermes-Agent).
- `llms-install.md` for AI agent auto-discovery.
- MCP registry manifest (`server.json`) and Glama manifest (`glama.json`).
- Example workflows: `curl-quickstart`, `bulk-tag-folder`, `claude-desktop`, `gmail-attachment-triage`, `llamaindex-reader`, `langchain-loader`.
- GitHub Actions workflows for linting examples, validating install snippets, and weekly link checks.

## Server contract — release history

The Gemina FileTag MCP server is a hosted service; only server-side changes that affect clients or break backward compatibility are recorded here.

- **2026-05** — Public launch. Endpoint: `https://api.gemina.co/api/v1/mcp/`. Tools: `files_create_upload`, `tag_file`, `tag_url`. Auth: `X-API-Key` or `Authorization: Bearer`. Free tier: 1,500 calls/month.

[Unreleased]: https://github.com/tommyil/gemina-mcp/commits/main
