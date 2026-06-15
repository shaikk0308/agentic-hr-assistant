import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "db" / "policies.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT id, code, title, category, effective_from FROM policies")
rows = cur.fetchall()
conn.close()

for r in rows:
    print(r)
