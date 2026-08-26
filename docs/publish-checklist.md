# Publish checklist: gemina-mcp 2.0.0 (`co.gemina/gemina`)

Run top to bottom on publish day, from the repo root on `main` (after
`feat/gemina-v2` is merged). Every step has a verification. Stop at the first
failure. Nothing here is idempotent-safe to re-run blindly except the curls.

Prerequisites on the machine: `mcp-publisher`, `gh` (logged in as `tommyil`),
`jq`, `openssl`, `xxd`, `python3` with `jsonschema`, and `key.pem` at the repo
root (gitignored; backup in GSM `mcp-registry-ed25519`, project
`gemina-production`).

## 0. Pre-flight: everything the manifests point at must be live

The manifests reference URLs that ship with the website branch and the API
OAuth deploy. As of 2026-08-26 the items marked ✗ were **not** live on prod.

```bash
for u in \
  https://www.gemina.co/assets/gemina-logo.png \
  https://www.gemina.co/product/agents \
  https://www.gemina.co/docs/mcp \
  https://www.gemina.co/privacy \
  https://www.gemina.co/assets/filetag-logo.png \
  https://api.gemina.co/.well-known/oauth-protected-resource/api/v1/mcp \
  https://api.gemina.co/.well-known/oauth-authorization-server/api/v1/mcp ; do
  printf '%-90s ' "$u"; curl -s -o /dev/null -w '%{http_code} %{content_type}\n' "$u"
done
```

Expected: all `200`. Status on 2026-08-26: `gemina-logo.png` ✗ 404,
`/product/agents` ✓, `/docs/mcp` ✗ 404, `/privacy` ✗ 404, `filetag-logo.png` ✓,
both OAuth discovery URLs ✗ 404 on prod (✓ on `api.staging.gemina.co`).

Icon dimensions (must be 400x400 to match `icons[0].sizes`):

```bash
curl -s https://www.gemina.co/assets/gemina-logo.png | python3 -c "import struct,sys; b=sys.stdin.buffer.read(); print(struct.unpack('>II', b[16:24]))"
```

OAuth must be live on **prod** before publishing a header marked optional.
The 401 must carry `WWW-Authenticate` with `resource_metadata`:

```bash
curl -s -D - -o /dev/null -X POST https://api.gemina.co/api/v1/mcp/ \
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}' \
  | grep -i 'HTTP/\|www-authenticate'
```

Expected: `HTTP/2 401` **and** a `www-authenticate: Bearer realm="mcp", resource_metadata="https://api.gemina.co/.well-known/oauth-protected-resource/api/v1/mcp", scope="mcp"` line (that is what staging returns today; prod returned a bare 401 on 2026-08-26).

Anonymous discovery still answers:

```bash
curl -s -X POST https://api.gemina.co/api/v1/mcp/public/ \
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | grep -o '"name":"[a-z_]*"' | wc -l
```

Expected: `13`.

## 1. Fill in the date and validate the manifests

```bash
sed -i 's/## \[2.0.0\] - 2026-08-xx/## [2.0.0] - '"$(date +%F)"'/' CHANGELOG.md
python3 -m json.tool server.json        > /dev/null
python3 -m json.tool server.legacy.json > /dev/null
python3 -m json.tool glama.json         > /dev/null
python3 - <<'PY'
import json, jsonschema, urllib.request
schema = json.load(urllib.request.urlopen("https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"))
for f in ("server.json", "server.legacy.json"):
    d = json.load(open(f))
    assert len(d["description"]) <= 100, f
    errs = [e.message for e in jsonschema.Draft7Validator(schema).iter_errors(d)]
    print(f, "OK" if not errs else errs)
PY
python3 -c "import json; [print(f, json.load(open(f))['remotes'][0]['url'].endswith('/api/v1/mcp/')) for f in ('server.json','server.legacy.json')]"   # both True
git add CHANGELOG.md && git commit -m "chore(release): 2.0.0 release date"
```

## 2. Log in to the registry (DNS proof of `gemina.co`)

```bash
mcp-publisher login dns --domain gemina.co \
  --private-key "$(openssl pkey -in key.pem -outform DER | tail -c 32 | xxd -p -c 64)"
```

Expected: `Successfully authenticated`. Token lands in
`~/.config/mcp-publisher/token.json`.

## 3. Publish the new name first

```bash
mcp-publisher publish            # reads ./server.json  -> co.gemina/gemina 2.0.0
```

Verify:

```bash
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers/co.gemina%2Fgemina/versions/2.0.0" \
  | jq '{name:.server.name, version:.server.version, title:.server.title, website:.server.websiteUrl, docs:.server.documentationUrl, hdr:.server.remotes[0].headers[0].isRequired, meta:._meta["io.modelcontextprotocol.registry/official"]}'
```

Expected: `name` `co.gemina/gemina`, `version` `2.0.0`, `hdr` `false`,
`meta.status` `active`, `meta.isLatest` `true`. `docs` will be `null` (the
registry strips `documentationUrl`; expected).

## 4. Publish the legacy pointer, then deprecate it

```bash
mcp-publisher publish server.legacy.json   # co.gemina/filetag 1.0.3
mcp-publisher status --status deprecated --all-versions --yes \
  --message "Renamed to co.gemina/gemina (same server, same endpoint). Install co.gemina/gemina." \
  co.gemina/filetag
```

Verify both names:

```bash
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=co.gemina" \
  | jq -r '.servers[] | [.server.name, .server.version, ._meta["io.modelcontextprotocol.registry/official"].status, (._meta["io.modelcontextprotocol.registry/official"].isLatest|tostring)] | @tsv'
```

Expected rows: `co.gemina/gemina 2.0.0 active true`, `co.gemina/filetag 1.0.3
deprecated true`, and the older `filetag` versions `deprecated false`.

If `mcp-publisher status` is missing in the installed CLI version, the raw
call is:

```bash
TOKEN=$(jq -r .token ~/.config/mcp-publisher/token.json)
curl -s -X PATCH "https://registry.modelcontextprotocol.io/v0.1/servers/co.gemina%2Ffiletag/status" \
  -H "Authorization: Bearer $TOKEN" -H 'content-type: application/json' \
  -d '{"status":"deprecated","statusMessage":"Renamed to co.gemina/gemina (same server, same endpoint). Install co.gemina/gemina."}'
```

## 5. Tag and GitHub Release

```bash
git tag -a v2.0.0 -m "gemina-mcp 2.0.0: co.gemina/gemina, OAuth-first, 13 tools"
git push origin main --tags
gh release create v2.0.0 --title "v2.0.0: Gemina (co.gemina/gemina), OAuth 2.1, 13 tools" \
  --notes-file <(awk '/^## \[2.0.0\]/{f=1;next} /^## \[/{f=0} f' CHANGELOG.md)
gh release view v2.0.0 --json tagName,url -q '"\(.tagName) \(.url)"'
```

## 6. Repository metadata

```bash
gh repo edit tommyil/gemina-mcp \
  --description "Gemina MCP server: invoice OCR, document extraction, document search, and free FileTag tagging for AI agents. OAuth 2.1 or API key. Works with Claude, Cursor, VS Code, Cline, Windsurf, Codex, OpenClaw, Hermes." \
  --homepage "https://www.gemina.co/product/agents" \
  --remove-topic vector-store-metadata --remove-topic rag-ingestion --remove-topic pdf-processing \
  --add-topic oauth --add-topic document-extraction --add-topic document-search
```

GitHub caps topics at 20. Dropped (near-duplicates of kept topics, least
searched): `vector-store-metadata` (dup of `metadata`), `rag-ingestion` (dup
of `rag`), `pdf-processing` (dup of `pdf`). Kept: `claude`, `cursor`,
`document-ai`, `email-automation`, `image-processing`, `invoice-processing`,
`langchain`, `llamaindex`, `mcp`, `mcp-server`, `metadata`,
`model-context-protocol`, `pdf`, `rag`, `remote-mcp`, `streamable-http`,
`vscode`, plus the three new ones.

Verify:

```bash
gh repo view tommyil/gemina-mcp --json description,homepageUrl,repositoryTopics \
  -q '{d:.description, h:.homepageUrl, n:(.repositoryTopics|length), t:[.repositoryTopics[].name]}'
```

Expected: `n` = 20, includes `oauth`, `document-extraction`, `document-search`.

## 7. Directory outreach (after the registry shows 2.0.0)

Send in this order; drafts are in `docs/outreach/`:

1. `glama-support-email.md`: slug rename + re-scan.
2. `cline-marketplace.md`: comment on cline/mcp-marketplace#1646, close #1617.
3. `mcp-so-listing.md`: submit at mcp.so.
4. `awesome-mcp-servers-pr.md`: open the PR; the Glama badge URL only
   resolves after step 1 completes.
5. `anthropic-connector-directory.md`: needs `/privacy` live and tool
   `title`/`readOnlyHint`/`destructiveHint` annotations shipped on the server
   first (see the draft's blockers list).
6. `smithery-submission.md`: needs prod OAuth 401 header (step 0) or the
   static server card.

## 8. Post-publish sanity

```bash
claude mcp add --transport http gemina https://api.gemina.co/api/v1/mcp/   # OAuth lane
claude mcp list
```

Expected: `gemina` connects after a browser sign-in with no headers.
