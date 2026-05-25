# Dockerfile -- Glama directory introspection container.
#
# NOT for end users. End users should follow the "Quick install" section
# of README.md and point their MCP client at
# https://api.gemina.co/api/v1/mcp/ with their personal X-API-Key.
#
# This file is consumed by Glama (https://glama.ai/mcp/servers/) so their
# health checker can run a stdio MCP client that bridges to Gemina's
# anonymous discovery endpoint at /api/v1/mcp/public/. The endpoint
# allows ``initialize`` / ``tools/list`` / ``prompts/list`` without
# credentials but refuses ``tools/call`` -- exactly what Glama's
# introspection check needs (and nothing more).

FROM node:20-alpine

RUN npm install -g mcp-remote@0.1.38

ENTRYPOINT ["mcp-remote", "https://api.gemina.co/api/v1/mcp/public/"]
