#!/usr/bin/env bash
set -euo pipefail
VENV="${DISCURSIVE_MEMORY_VENV:-$HOME/.local/share/discursive-memory/venv}"
REPO="${1:-$PWD}"
env -u PYTHONPATH "$VENV/bin/discursive-memory" init --repo "$REPO"
env -u PYTHONPATH "$VENV/bin/discursive-memory" index --repo "$REPO"
env -u PYTHONPATH "$VENV/bin/discursive-memory" self-test --repo "$REPO"
printf '
Now open this exact folder in VS Code and reload the window:
%s
' "$REPO"
