from pathlib import Path
from importlib.resources import files
from datetime import datetime,UTC
import sqlite3,json,re
ACTIVE=("active","tentative","resolved")
INVERSE={"supports":"supported_by","contradicts":"contradicted_by","depends_on":"required_by","tested_by":"tests","implements":"implemented_by","supersedes":"superseded_by","derived_from":"source_of","refines":"refined_by"}
class Store:
 def __init__(self,path:Path):path.parent.mkdir(parents=True,exist_ok=True);self.path=path;self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row;self.db.execute("PRAGMA foreign_keys=ON");self.db.executescript(files("discursive_memory").joinpath("schema.sql").read_text());self.db.commit()
 def rebuild(self,records):
  with self.db:
   for t in ("records_fts","relations","facets","records"):self.db.execute(f"DELETE FROM {t}")
   for r in records:
    self.db.execute("INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?,?,?)",(r["id"],r["type"],r["status"],r["granularity"],r["title"],r["summary"],r["content"],r["confidence"],r["source_path"],r["content_hash"],r["updated_at"]))
    for kind in ("topics","entities","aliases"):self.db.executemany("INSERT INTO facets VALUES(?,?,?)",[(r["id"],kind,x) for x in r[kind]])
    self.db.executemany("INSERT INTO relations VALUES(?,?,?,?,?,?)",[(r["id"],e["type"],e["target"],float(e.get("confidence",1)),str(e.get("rationale","")),json.dumps(e.get("evidence",[]))) for e in r["relations"]])
    self.db.execute("INSERT INTO records_fts VALUES(?,?,?,?,?,?,?)",(r["id"],r["title"],r["summary"],r["content"]," ".join(r["topics"])," ".join(r["entities"])," ".join(r["aliases"])))
 def search(self,q,limit=6,types=None):
  toks=re.findall(r"[\w./:#-]+",q);match=" OR ".join('"'+x.replace('"','')+'"' for x in toks[:24])
  if not match:return []
  params=[match,*ACTIVE];extra=""
  if types:extra=" AND r.type IN ("+",".join("?"*len(types))+")";params+=types
  params.append(limit)
  return [dict(x) for x in self.db.execute(f"SELECT r.id,r.type,r.status,r.granularity,r.title,r.summary,r.confidence,bm25(records_fts) score FROM records_fts JOIN records r ON r.id=record_id WHERE records_fts MATCH ? AND r.status IN (?,?,?){extra} ORDER BY score LIMIT ?",params)]
 def get(self,ids):
  if not ids:return []
  rows=self.db.execute("SELECT * FROM records WHERE id IN ("+",".join("?"*len(ids))+")",ids);d={x["id"]:dict(x) for x in rows};return [d[x] for x in ids if x in d]
 def edges(self,ids,direction="both",types=None):
  if not ids:return []
  marks=",".join("?"*len(ids));out=[]
  if direction in ("out","both"):out += [dict(x)|{"display_type":x["type"]} for x in self.db.execute(f"SELECT * FROM relations WHERE source_id IN ({marks})",ids)]
  if direction in ("in","both"):out += [dict(x)|{"display_type":INVERSE.get(x["type"],"incoming_"+x["type"])} for x in self.db.execute(f"SELECT * FROM relations WHERE target_id IN ({marks})",ids)]
  return [x for x in out if not types or x["type"] in types or x["display_type"] in types]
 def journal(self,op,q,ids):self.db.execute("INSERT INTO journal(ts,operation,query,result_ids) VALUES(?,?,?,?)",(datetime.now(UTC).isoformat(),op,q,json.dumps(ids)));self.db.commit()
 def stats(self):return {"records":self.db.execute("SELECT count(*) FROM records").fetchone()[0],"relations":self.db.execute("SELECT count(*) FROM relations").fetchone()[0],"sqlite":str(self.path)}
