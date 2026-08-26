# Contributing to gemina-mcp

Thanks for the interest. This repo is the install, discovery, and examples surface for Gemina's MCP server — not the server code itself. That shapes what PRs we accept.

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

## Publishing to the MCP Registry (maintainers)

There are **two** registry entries, both proven by the same `gemina.co` DNS
namespace:

| File | Registry name | Purpose |
|---|---|---|
| `server.json` | `co.gemina/gemina` | The live entry. Bump on every release. |
| `server.legacy.json` | `co.gemina/filetag` | The pre-2.0 name. Republished once as 1.0.3 whose description points at `co.gemina/gemina`, then marked `deprecated`. Do not bump it again unless the pointer text changes. |

The `co.gemina/*` namespace is proven by an Ed25519 key whose public half is in
a DNS TXT record on the `gemina.co` apex. The private key lives **outside git**
at `key.pem` (gitignored) and is backed up in Google Secret Manager
(`mcp-registry-ed25519`, project `gemina-production`).

The full publish-day runbook (pre-flight curls, exact commands, GitHub release
and repo-metadata steps) is `docs/publish-checklist.md`. The short form:

1. Edit `server.json`: bump `version`, keep `description` ≤ 100 characters,
   keep every `/api/v1/mcp/` URL with its trailing slash.
2. `python -m json.tool server.json > /dev/null` (and `server.legacy.json` if touched).
   Optional stricter check: validate both against
   `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`
   with `python -c "import json,jsonschema,urllib.request; ..."` (see the checklist).
3. `mcp-publisher login dns --domain gemina.co --private-key "$(openssl pkey -in key.pem -outform DER | tail -c 32 | xxd -p -c 64)"`
4. Publish **the new name first**, then the legacy pointer:
   `mcp-publisher publish` (defaults to `./server.json`), then
   `mcp-publisher publish server.legacy.json`.
   Order matters: the legacy description tells people to install
   `co.gemina/gemina`, so that entry must already resolve.
5. Mark the legacy name deprecated (see "Deprecation" below).
6. Verify: `curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=co.gemina" | jq '.servers[] | {name: .server.name, version: .server.version, status: ._meta["io.modelcontextprotocol.registry/official"].status, latest: ._meta["io.modelcontextprotocol.registry/official"].isLatest}'`
7. Commit the bumped manifests, tag `vX.Y.Z`, and create a GitHub Release.

### Deprecation / status (registry API findings, 2026-08-26)

- A `name` change publishes a *new* server; there is no rename and the old
  entry stays listed. Hence the pointer republish above.
- The registry **does** support lifecycle status. Every listed version carries
  `_meta["io.modelcontextprotocol.registry/official"]` with `status`,
  `statusChangedAt`, `publishedAt`, `updatedAt`, `isLatest` (and `statusMessage`
  when set). Today all three `co.gemina/filetag` versions show `status: active`.
- Status enum: `active | deprecated | deleted`. `deprecated` keeps the entry
  visible **with a warning** (what we want for the pointer); `deleted` hides it
  from default listings. `statusMessage` is optional, ≤ 500 chars, and not
  allowed when setting `active`.
- Endpoints (Bearer registry JWT from `mcp-publisher login`):
  `PATCH /v0.1/servers/{serverName}/versions/{version}/status` (one version) and
  `PATCH /v0.1/servers/{serverName}/status` (all versions), body
  `{"status":"deprecated","statusMessage":"..."}`. There is also
  `PUT /v0.1/servers/{serverName}/versions/{version}` (edit) and `DELETE`.
- The CLI wraps this: `mcp-publisher status --status deprecated --all-versions --message "Renamed to co.gemina/gemina. Install that instead." co.gemina/filetag`
  (`--yes` skips the confirmation). Requires `publish` or `edit` permission on
  the namespace, i.e. the same DNS login.
- Sources: `docs/reference/api/openapi.yaml` and `docs/reference/cli/commands.md`
  in https://github.com/modelcontextprotocol/registry.

Notes: the registry rejects non-standard fields and silently strips
`documentationUrl` (it is not in the 2025-12-11 schema, which only tolerates it
because the schema does not set `additionalProperties: false`). Keep it in the
file anyway; sub-registries such as Glama read it.

