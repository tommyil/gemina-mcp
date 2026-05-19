# Examples

Runnable recipes for the Gemina FileTag MCP server. Each subdirectory is independent — clone the repo, `cd` into one, follow its README.

| Directory | What it shows | Stack |
|---|---|---|
| [`curl-quickstart`](./curl-quickstart) | First successful tag in three minutes | Shell + curl |
| [`claude-desktop`](./claude-desktop) | Step-by-step setup in Claude Desktop | None (config-only walkthrough) |
| [`bulk-tag-folder`](./bulk-tag-folder) | Walk a directory and tag every file | Python + `requests` |
| [`gmail-attachment-triage`](./gmail-attachment-triage) | Pull Gmail attachments, tag them, route to folders | Python + Google API |
| [`llamaindex-reader`](./llamaindex-reader) | Custom LlamaIndex reader that enriches each node with FileTag metadata | Python + LlamaIndex |
| [`langchain-loader`](./langchain-loader) | Equivalent LangChain document loader | Python + LangChain |

## Getting an API key

All examples need an API key. Get one free (1,500 tags/month, no credit card) at https://console.gemina.co/registration/create-account.

Set it as `GEMINA_API_KEY` in your shell:

```bash
export GEMINA_API_KEY="paste-your-key-here"
```

The Python examples read this env var by default; the curl examples expect it in the same shell session.

## Conventions

- Examples target Python 3.10+ and assume a virtualenv (`python -m venv .venv && source .venv/bin/activate`).
- No SDK — all examples talk to the public REST/MCP endpoints directly with `requests` or `curl`. Keeps the code copy-pasteable and dependency-light.
- All output is written under `output/` inside each example dir (gitignored). Re-runs are idempotent.

## Contributing a new example

See [CONTRIBUTING.md](../CONTRIBUTING.md). One folder per example, with its own README and a working script you've actually run end-to-end against production.
