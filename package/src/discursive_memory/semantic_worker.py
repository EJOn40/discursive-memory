"""Optional semantic backend. Imported only in a child process."""
from pathlib import Path
import json,sys
def main():
 op=sys.argv[1];request=json.load(sys.stdin)
 try:
  import lancedb
  from fastembed import TextEmbedding
 except Exception as e:
  json.dump({"ok":False,"error":f"semantic dependencies unavailable: {e}"},sys.stdout);return
 model=TextEmbedding(model_name=request.get("model","BAAI/bge-small-en-v1.5"));db=lancedb.connect(request["path"])
 if op=="index":
  rows=request["rows"];texts=[x["text"] for x in rows];vectors=[v.tolist() for v in model.embed(texts)] if texts else []
  if "records" in db.table_names():db.drop_table("records")
  if rows:db.create_table("records",data=[{"record_id":x["id"],"text":x["text"],"vector":v} for x,v in zip(rows,vectors,strict=True)])
  json.dump({"ok":True,"count":len(rows)},sys.stdout)
 elif op=="search":
  if "records" not in db.table_names():json.dump({"ok":False,"error":"semantic index missing"},sys.stdout);return
  vector=next(iter(model.query_embed(request["query"]))).tolist();rows=db.open_table("records").search(vector).limit(request["limit"]).to_list();json.dump({"ok":True,"ids":[x["record_id"] for x in rows]},sys.stdout)
if __name__=="__main__":main()
