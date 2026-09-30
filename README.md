# Robust Discursive Memory MCP

This version starts from scratch with failure isolation:

- SQLite + FTS5 is the always-available core.
- LanceDB/FastEmbed is optional and loaded only in a child process.
- The MCP imports quickly even if LanceDB is slow or broken.
- Semantic timeout/failure falls back to lexical retrieval.
- VS Code launches the package with an absolute Python path plus `-m`, avoiding PATH and console-script issues.
- A self-test checks MCP import, configuration, and FTS5.

## 1. Install the robust core

```bash
unzip discursive-memory-robust.zip
cd discursive-memory-robust
./install.sh
```

## 2. Initialize a repository

```bash
cd ~/Documents/GitHub/agent-memory
/path/to/discursive-memory-robust/setup-repo.sh "$PWD"
```

Or directly:

```bash
~/.local/share/discursive-memory/venv/bin/discursive-memory init --repo .
~/.local/share/discursive-memory/venv/bin/discursive-memory index --repo .
~/.local/share/discursive-memory/venv/bin/discursive-memory self-test --repo .
```

Expected self-test result includes `"ok": true`.

## 3. VS Code

Open the repository root, not this installer directory:

```bash
code ~/Documents/GitHub/agent-memory
```

Reload the window. The generated `.vscode/mcp.json` uses the official workspace `servers` format and runs:

```text
<absolute-venv-python> -m discursive_memory.server
```

## 4. Optional semantic layer

After the core works:

```bash
/path/to/discursive-memory-robust/install-semantic.sh
cd ~/Documents/GitHub/agent-memory
~/.local/share/discursive-memory/venv/bin/discursive-memory index --repo . --semantic
```

A slow LanceDB import can never block MCP startup because it occurs only in a bounded child process.

## Diagnostics

```bash
~/.local/share/discursive-memory/venv/bin/discursive-memory self-test --repo .
cat .vscode/mcp.json
MEMORY_REPO_ROOT="$PWD" timeout 10 ~/.local/share/discursive-memory/venv/bin/python -m discursive_memory.server
```

The timeout test should run for 10 seconds and exit with status 124, showing that the stdio server stayed alive.
