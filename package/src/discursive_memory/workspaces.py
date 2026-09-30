from pathlib import Path
from datetime import datetime,UTC
import frontmatter,yaml
class Workspaces:
 def __init__(self,root):self.root=Path(root);(self.root/"active").mkdir(parents=True,exist_ok=True)
 def list(self):return [p.stem for p in sorted((self.root/"active").glob("*.md"))]
 def get(self,i):
  p=self.root/"active"/f"{i}.md"
  if not p.exists():return None
  x=frontmatter.load(p);return {"id":i,"metadata":x.metadata,"content":x.content,"path":str(p)}
 def checkpoint(self,i,objective,understanding,evidence,questions,rejected,actions):
  meta={"id":i,"status":"active","objective":objective,"updated_at":datetime.now(UTC).isoformat()};body=f"## Current understanding\n\n{understanding}\n\n## Evidence\n"+"".join(f"- {x}\n" for x in evidence)+"\n## Open questions\n"+"".join(f"- {x}\n" for x in questions)+"\n## Rejected explanations\n"+"".join(f"- {x}\n" for x in rejected)+"\n## Next actions\n"+"".join(f"- {x}\n" for x in actions);p=self.root/"active"/f"{i}.md";p.write_text("---\n"+yaml.safe_dump(meta,sort_keys=False)+"---\n\n"+body);return self.get(i)
