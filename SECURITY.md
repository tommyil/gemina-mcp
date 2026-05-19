# Security policy

## Reporting a vulnerability

**Please do not file public GitHub issues for security vulnerabilities.**

Email **security@gemina.co** with:

- A description of the vulnerability and its potential impact.
- Steps to reproduce, including any required API key permissions, request payloads, or environmental conditions.
- Your contact information if you'd like a response (anonymous reports are also accepted).

We aim to respond within **two business days** with an acknowledgement and an initial assessment. We will keep you informed of progress until resolution.

## Scope

This policy covers:

- The Gemina FileTag MCP server at `https://api.gemina.co/api/v1/mcp/`.
- The Gemina FileTag REST API at `https://api.gemina.co/api/v1/filetag` and adjacent endpoints.
- The example code in this repository (Python, shell, configuration files).
- Authentication flows for API keys issued via `https://console.gemina.co`.

Out of scope (please don't report):

- Issues in third-party MCP clients (Claude Desktop, Cursor, etc.) — report those to their respective vendors.
- Rate-limiting denial of service from a single API key (we limit by design).
- Reports that require physical access to a victim's device.

## Coordinated disclosure

We follow standard coordinated disclosure. Please give us a reasonable window (typically 90 days from first contact, extendable by mutual agreement) before public disclosure, and we will work with you to credit your finding in the release notes if you'd like.

## Public PGP key

Available on request at security@gemina.co — we'll send the fingerprint and key from the same address for first-contact verification.

## Other security resources

- [Gemina Trust Center](https://www.gemina.co/trust-center) — security posture, encryption, residency.
- [Privacy Policy](https://www.gemina.co/privacy-policy)
- [Terms of Service](https://www.gemina.co/terms-of-service)
