from pathlib import Path
from datetime import date
import hashlib
import frontmatter
TYPES={"decision","problem","finding","experiment","hypothesis","assumption","procedure","preference","concept","constraint"}
STATUSES={"active","tentative","resolved","superseded","rejected","obsolete","archived"}
def load(directory:Path):
 out=[]
 for p in sorted(directory.rglob("*.md")):
  raw=p.read_bytes()
  if not raw.startswith(b"---"):continue
  post=frontmatter.loads(raw.decode("utf-8"));m=post.metadata
  for k in ("id","type","status","title","summary"):
   if not m.get(k):raise ValueError(f"{p}: missing {k}")
  if m["type"] not in TYPES:raise ValueError(f"{p}: invalid type {m['type']}")
  if m["status"] not in STATUSES:raise ValueError(f"{p}: invalid status {m['status']}")
  out.append({"id":str(m["id"]),"type":m["type"],"status":m["status"],"granularity":m.get("granularity","atomic"),"title":str(m["title"]),"summary":str(m["summary"]),"content":post.content.strip(),"confidence":float(m.get("confidence",1)),"topics":m.get("topics",[]) or [],"entities":m.get("entities",[]) or [],"aliases":m.get("aliases",[]) or [],"relations":m.get("relations",[]) or [],"source_path":str(p.resolve()),"content_hash":hashlib.sha256(raw).hexdigest(),"updated_at":str(m.get("updated_at",date.today()))})
 ids=[x["id"] for x in out]
 if len(ids)!=len(set(ids)):raise ValueError("duplicate record ID")
 missing={e["target"] for r in out for e in r["relations"] if e["target"] not in set(ids)}
 if missing:raise ValueError(f"unknown relation targets: {sorted(missing)}")
 return out
def embedding_text(r):return "\n".join([r["type"],r["title"],r["summary"]," ".join(r["topics"])," ".join(r["entities"])," ".join(r["aliases"]),r["content"]])
