import sqlite3
from pathlib import Path
from fastmcp import FastMCP

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "policies.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

mcp = FastMCP("policies-server")

@mcp.tool()
def get_policy_by_code(code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT code, title, body, category, effective_from, effective_to
        FROM policies
        WHERE code = ?
        """,
        (code,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {"success": False, "message": f"No policy found for code {code}"}

    keys = ["code", "title", "body", "category", "effective_from", "effective_to"]
    return {"success": True, "policy": dict(zip(keys, row))}

@mcp.tool()
def search_policies(keyword: str):
    pattern = f"%{keyword}%"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT code, title, category, effective_from
        FROM policies
        WHERE title LIKE ? OR body LIKE ?
        LIMIT 20
        """,
        (pattern, pattern),
    )
    rows = cur.fetchall()
    conn.close()

    keys = ["code", "title", "category", "effective_from"]
    return {"success": True, "policies": [dict(zip(keys, r)) for r in rows]}

if __name__ == "__main__":
    mcp.run()
