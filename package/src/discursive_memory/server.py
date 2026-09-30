from typing import Any,Literal
from mcp.server import MCPServer
from .runtime import cfg,store,workspaces
from .semantic import call
mcp=MCPServer("discursive-memory")
@mcp.tool()
def memory_search(query:str,limit:int=6,record_types:list[str]|None=None,mode:Literal["lexical","hybrid","semantic"]="hybrid")->dict[str,Any]:
 """Search compact memory candidates. Semantic failures automatically fall back to lexical retrieval."""
 limit=max(1,min(limit,10));lex=[] if mode=="semantic" else store().search(query,limit*3,record_types);warning=None
 if mode in ("hybrid","semantic"):
  sem=call("search",cfg()["lance"],{"query":query,"limit":limit*3},20)
  if sem.get("ok"):
   ordered=[]
   for rid in [x["id"] for x in lex]+sem["ids"]:
    if rid not in ordered:ordered.append(rid)
   records={r["id"]:r for r in store().get(ordered)};results=[]
   for rid in ordered:
    if rid in records:results.append({k:records[rid][k] for k in ("id","type","status","granularity","title","summary","confidence")}|{"matched_by":"hybrid"})
   results=results[:limit]
  else:warning=sem.get("error");results=lex[:limit]
 else:results=lex[:limit]
 store().journal("search",query,[x["id"] for x in results]);return {"query":query,"count":len(results),"results":results,"semantic_warning":warning}
@mcp.tool()
def memory_get(ids:list[str],detail:Literal["outline","evidence","full"]="evidence",max_characters:int=3500)->dict[str,Any]:
 """Fetch one to five selected records and their direct explicit relations."""
 out=[]
 for r in store().get(ids[:5]):
  r["content"]="" if detail=="outline" else r["content"] if detail=="full" else r["content"][:max(300,min(max_characters,12000))];r["relations"]=store().edges([r["id"]])[:10];out.append(r)
 return {"count":len(out),"records":out}
@mcp.tool()
def memory_trace(seed_ids:list[str],relation_types:list[str]|None=None,direction:Literal["out","in","both"]="both",limit:int=8)->dict[str,Any]:
 """Follow explicit bidirectional evidence, dependency, contradiction, and history relations."""
 x=store().edges(seed_ids[:5],direction,relation_types)[:max(1,min(limit,15))];return {"count":len(x),"relations":x}
@mcp.tool()
def workspace_list()->dict[str,Any]:return {"active":workspaces().list()}
@mcp.tool()
def workspace_get(workspace_id:str)->dict[str,Any]:return {"workspace":workspaces().get(workspace_id)}
@mcp.tool()
def workspace_checkpoint(workspace_id:str,objective:str,current_understanding:str,evidence:list[str],open_questions:list[str],rejected_explanations:list[str],next_actions:list[str])->dict[str,Any]:
 """Persist provisional discursive state before compaction or interruption."""
 return {"workspace":workspaces().checkpoint(workspace_id,objective,current_understanding,evidence,open_questions,rejected_explanations,next_actions)}
@mcp.tool()
def memory_stats()->dict[str,Any]:return store().stats()|{"active_workspaces":len(workspaces().list())}
def main():mcp.run()
if __name__=="__main__":main()
