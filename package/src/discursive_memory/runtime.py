from functools import lru_cache
from .config import paths
from .store import Store
from .workspaces import Workspaces
@lru_cache
def cfg():return paths()
@lru_cache
def store():return Store(cfg()["sqlite"])
@lru_cache
def workspaces():return Workspaces(cfg()["workspaces"])
