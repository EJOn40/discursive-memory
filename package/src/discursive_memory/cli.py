import argparse,json,sys,subprocess
from pathlib import Path
from .config import paths
from .records import load,embedding_text
from .store import Store
from .semantic import call
TEMPLATE="""---
id: example-memory-record
type: finding
status: tentative
granularity: atomic
title: Example memory record
summary: Replace this example with a repository-specific durable memory.
confidence: 0.5
topics: [memory]
entities: []
aliases: []
relations: []
updated_at: 2026-09-30
---

## Observation or evidence

The repository memory was initialized successfully.
"""
def emit(x):print(json.dumps(x,indent=2,ensure_ascii=False,default=str))
def init(repo):
 c=paths(repo)
 for d in ["decisions","problems","findings","experiments","hypotheses","assumptions","procedures","preferences","concepts","constraints"]:(c["records"]/d).mkdir(parents=True,exist_ok=True)
 (c["workspaces"]/"active").mkdir(parents=True,exist_ok=True);(c["workspaces"]/"archived").mkdir(parents=True,exist_ok=True);(c["repo"]/"memory/proposals").mkdir(parents=True,exist_ok=True);c["index"].mkdir(exist_ok=True);p=c["records"]/"findings/example-memory-record.md"
 if not p.exists():p.write_text(TEMPLATE)
 (c["repo"]/".vscode").mkdir(exist_ok=True);python=sys.executable;config={"servers":{"discursive-memory":{"type":"stdio","command":python,"args":["-m","discursive_memory.server"],"cwd":"${workspaceFolder}","env":{"MEMORY_REPO_ROOT":"${workspaceFolder}"}}}};(c["repo"]/".vscode/mcp.json").write_text(json.dumps(config,indent=2)+"\n")
 gi=c["repo"]/".gitignore";old=gi.read_text() if gi.exists() else "";
 if ".memory-index/" not in old:gi.write_text(old+("\n" if old and not old.endswith("\n") else "")+".memory-index/\n")
 return {"repo":str(c["repo"]),"python":python,"mcp_config":str(c["repo"]/".vscode/mcp.json")}
def selftest(repo):
 c=paths(repo);checks={"python":sys.executable,"mcp_import":False,"config_exists":(c["repo"]/".vscode/mcp.json").exists(),"fts5":False}
 try:subprocess.run([sys.executable,"-c","from discursive_memory.server import mcp"],check=True,timeout=10,capture_output=True);checks["mcp_import"]=True
 except Exception as e:checks["mcp_error"]=str(e)
 try:s=Store(c["sqlite"]);s.db.execute("SELECT count(*) FROM records_fts");checks["fts5"]=True
 except Exception as e:checks["fts5_error"]=str(e)
 checks["ok"]=checks["mcp_import"] and checks["config_exists"] and checks["fts5"];return checks
def main():
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest="cmd",required=True)
 for n in ("init","index","doctor","self-test"):
  x=sub.add_parser(n);x.add_argument("--repo",default=".");
  if n=="index":x.add_argument("--semantic",action="store_true")
 q=sub.add_parser("search");q.add_argument("query");q.add_argument("--repo",default=".");q.add_argument("--limit",type=int,default=6)
 a=p.parse_args();c=paths(a.repo)
 if a.cmd=="init":emit(init(a.repo));return
 s=Store(c["sqlite"])
 if a.cmd=="index":
  records=load(c["records"]);s.rebuild(records);result={"lexical_records":len(records)}
  if a.semantic:result["semantic"]=call("index",c["lance"],{"rows":[{"id":r["id"],"text":embedding_text(r)} for r in records]},600)
  emit(result)
 elif a.cmd=="doctor":emit(s.stats()|{"config_exists":(c["repo"]/".vscode/mcp.json").exists(),"python":sys.executable})
 elif a.cmd=="self-test":emit(selftest(a.repo))
 else:emit(s.search(a.query,a.limit))
if __name__=="__main__":main()
