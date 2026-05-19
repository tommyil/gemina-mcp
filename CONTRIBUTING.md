# Contributing to gemina-mcp

Thanks for the interest. This repo is the install, discovery, and examples surface for Gemina FileTag — not the server code itself. That shapes what PRs we accept.

## What we welcome

- **Example contributions.** New use cases under `examples/` (e.g., a workflow for a tool we haven't covered, a recipe for a specific framework). One folder per example, with its own `README.md` and runnable code.
- **Fixes to existing examples.** Broken scripts, outdated dependencies, unclear instructions — all welcome.
- **Doc improvements.** README clarifications, install snippet fixes for clients we've gotten wrong, better explanations of edge cases.
- **Bug reports against the live server.** File an issue with the [bug template](./.github/ISSUE_TEMPLATE/bug.yml) — we treat them as production incident input.
- **Integration help requests.** Stuck installing in a specific client? Open an issue with the [integration help template](./.github/ISSUE_TEMPLATE/integration_help.yml).
- **New client install snippets.** If you've successfully connected a client we haven't documented, send a PR adding the snippet to `README.md` and `llms-install.md`.

## What we don't accept

- **PRs to the actual MCP server implementation.** The server lives in a private repository at Gemina. Open an issue or email info@gemina.co if you want to discuss server behavior.
- **PRs that change pricing, the free tier, the auth flow, or terms.** Those are policy decisions, not code changes. Open an issue first.

## Workflow

1. **Open an issue first** for anything bigger than a typo fix. Saves both of us time if we need to discuss direction.
2. **Fork → branch → PR.** Use a descriptive branch name like `example/n8n-workflow` or `fix/cursor-snippet-trailing-slash`.
3. **Keep PRs focused.** One example or one fix per PR. We'd rather merge five small PRs than one large one.
4. **Run your example end-to-end** before submitting — with a real free-tier API key against production. The CI smoke-tests catch some drift but can't replace human verification.

## Style

- **Examples are Python by default** unless the use case is inherently JavaScript/curl/shell.
- **Use `python -m venv .venv`** or `uv`. Don't pin exact versions in `requirements.txt` unless there's a known incompatibility.
- **Lint Python with `ruff`** (matches the CI config).
- **Format Markdown** with sane line breaks (don't hard-wrap unless the file is meant for terminal display).

## llms-install.md

This file is the canonical install reference for AI agents. It must stay in sync with the install snippets in `README.md`. If you change one, change both. CI checks that the JSON snippets parse.

## Code of conduct

This project follows the [Contributor Covenant](./CODE_OF_CONDUCT.md). Be kind. Disagree with the technical decision, not the person making it.

## Questions

- Issues: https://github.com/tommyil/gemina-mcp/issues
- Email: info@gemina.co
