#!/bin/sh
# Optional: index the project for Serena (can be heavy)
# Requires uv/uvx or python environment; see Serena docs.
# Usage: scripts/serena-index.sh

set -e
echo "Starting Serena MCP server / indexing is environment-specific."
echo "Suggested (uvx) command:"
echo "  uvx --from git+https://github.com/oraios/serena.git serena project index"
echo ""
echo "If you already have Serena installed as a CLI, run:"
echo "  serena project index"
