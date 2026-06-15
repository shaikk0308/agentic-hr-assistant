import sqlite3
from pathlib import Path
from fastmcp import FastMCP

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "compensation.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

mcp = FastMCP("compensation-server")

@mcp.tool()
def get_current_compensation(employee_code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT employee_code, base_salary, bonus, currency, effective_from, effective_to, created_at
        FROM compensation
        WHERE employee_code = ?
        ORDER BY effective_from DESC
        LIMIT 1
        """,
        (employee_code,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {"success": False, "message": f"No compensation found for {employee_code}"}

    keys = [
        "employee_code",
        "base_salary",
        "bonus",
        "currency",
        "effective_from",
        "effective_to",
        "created_at",
    ]
    return {"success": True, "compensation": dict(zip(keys, row))}

if __name__ == "__main__":
    mcp.run()
