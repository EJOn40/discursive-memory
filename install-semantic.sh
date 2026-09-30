#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="${DISCURSIVE_MEMORY_VENV:-$HOME/.local/share/discursive-memory/venv}"
env -u PIP_TARGET -u PYTHONPATH "$VENV/bin/pip" install "$ROOT/dist/discursive_memory_mcp-1.0.0-py3-none-any.whl[semantic]"
printf '
Semantic dependencies installed. Build them per repository with:
%s/discursive-memory index --repo . --semantic
' "$VENV/bin"
