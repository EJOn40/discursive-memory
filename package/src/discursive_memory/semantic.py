from pathlib import Path
import json,subprocess,sys
def call(op,path,payload,timeout):
 request={"path":str(path),**payload}
 try:
  p=subprocess.run([sys.executable,"-m","discursive_memory.semantic_worker",op],input=json.dumps(request),text=True,capture_output=True,timeout=timeout)
  if p.returncode:return {"ok":False,"error":p.stderr[-1000:]}
  return json.loads(p.stdout)
 except subprocess.TimeoutExpired:return {"ok":False,"error":f"semantic {op} timed out after {timeout}s"}
 except Exception as e:return {"ok":False,"error":str(e)}
