#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="${DISCURSIVE_MEMORY_VENV:-$HOME/.local/share/discursive-memory/venv}"
python3 -m venv "$VENV"
env -u PIP_TARGET -u PYTHONPATH "$VENV/bin/python" -m pip install --upgrade pip
env -u PIP_TARGET -u PYTHONPATH "$VENV/bin/pip" install --no-cache-dir --force-reinstall "$ROOT/dist/discursive_memory_mcp-1.0.0-py3-none-any.whl"
printf '
Installed. Next, from your repository run:
%s/discursive-memory init --repo .
%s/discursive-memory index --repo .
%s/discursive-memory self-test --repo .
' "$VENV/bin" "$VENV/bin" "$VENV/bin"
