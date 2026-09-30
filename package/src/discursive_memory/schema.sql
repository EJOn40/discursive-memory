PRAGMA foreign_keys=ON;
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS records(id TEXT PRIMARY KEY,type TEXT NOT NULL,status TEXT NOT NULL,granularity TEXT NOT NULL,title TEXT NOT NULL,summary TEXT NOT NULL,content TEXT NOT NULL,confidence REAL NOT NULL,source_path TEXT NOT NULL,content_hash TEXT NOT NULL,updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS facets(record_id TEXT REFERENCES records(id) ON DELETE CASCADE,kind TEXT NOT NULL,value TEXT NOT NULL,PRIMARY KEY(record_id,kind,value));
CREATE TABLE IF NOT EXISTS relations(source_id TEXT REFERENCES records(id) ON DELETE CASCADE,type TEXT NOT NULL,target_id TEXT NOT NULL,confidence REAL NOT NULL,rationale TEXT NOT NULL,evidence TEXT NOT NULL,PRIMARY KEY(source_id,type,target_id));
CREATE TABLE IF NOT EXISTS journal(id INTEGER PRIMARY KEY,ts TEXT,operation TEXT,query TEXT,result_ids TEXT);
CREATE VIRTUAL TABLE IF NOT EXISTS records_fts USING fts5(record_id UNINDEXED,title,summary,content,topics,entities,aliases,tokenize='unicode61 remove_diacritics 2');
