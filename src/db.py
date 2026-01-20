import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple

DEFAULT_DB_PATH = "data/app.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  content TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

def connect(db_path: str) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: str) -> None:
    conn = connect(db_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()

def seed(db_path: str, created_at: str) -> None:
    conn = connect(db_path)
    try:
        conn.execute(
            "INSERT OR IGNORE INTO users(username, role, created_at) VALUES(?,?,?)",
            ("admin", "admin", created_at),
        )
        conn.execute(
            "INSERT OR IGNORE INTO users(username, role, created_at) VALUES(?,?,?)",
            ("student", "user", created_at),
        )

        cur = conn.execute("SELECT id FROM users WHERE username = ?", ("student",))
        row = cur.fetchone()
        if row:
            student_id = row[0]
            conn.execute(
                "INSERT INTO notes(user_id, content, created_at) VALUES(?,?,?)",
                (student_id, "Hello from SQLite Manager Tool!", created_at),
            )
        conn.commit()
    finally:
        conn.close()

def list_tables(db_path: str) -> List[str]:
    conn = connect(db_path)
    try:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        return [r[0] for r in cur.fetchall()]
    finally:
        conn.close()

def table_row_counts(db_path: str) -> Dict[str, int]:
    conn = connect(db_path)
    try:
        tables = list_tables(db_path)
        counts: Dict[str, int] = {}
        for t in tables:
            cur = conn.execute(f"SELECT COUNT(*) FROM {t};")
            counts[t] = int(cur.fetchone()[0])
        return counts
    finally:
        conn.close()

def healthcheck(db_path: str) -> Tuple[bool, str]:
    try:
        conn = connect(db_path)
        conn.execute("SELECT 1;")
        conn.close()
        return True, "ok"
    except Exception as e:
        return False, str(e)
