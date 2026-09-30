from discursive_memory.cli import init,selftest
from discursive_memory.config import paths
from discursive_memory.records import load
from discursive_memory.store import Store
def test_end_to_end(tmp_path):
 init(tmp_path);c=paths(tmp_path);r=load(c["records"]);s=Store(c["sqlite"]);s.rebuild(r);assert s.search("initialized",5);assert selftest(tmp_path)["ok"]
