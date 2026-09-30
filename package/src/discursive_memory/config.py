from pathlib import Path
import os
def paths(repo=None):
 r=Path(repo or os.getenv("MEMORY_REPO_ROOT",".")).expanduser().resolve()
 return {"repo":r,"records":r/"memory/records","workspaces":r/"memory/workspaces","index":r/".memory-index","sqlite":r/".memory-index/memory.sqlite3","lance":r/".memory-index/lancedb"}
