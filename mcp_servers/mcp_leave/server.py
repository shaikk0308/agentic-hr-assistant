import sqlite3
from pathlib import Path
from datetime import datetime
from fastmcp import FastMCP

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "leave.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

mcp = FastMCP("leave-server")

def calculate_days_logic(start_date: str, end_date: str) -> int:
    d1 = datetime.strptime(start_date, "%Y-%m-%d")
    d2 = datetime.strptime(end_date, "%Y-%m-%d")
    return (d2 - d1).days + 1

@mcp.tool()
def get_leave_balance(employee_code: str):
    """Get the total remaining leave balance for an employee."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance_days FROM leave_balances WHERE employee_code = ? AND leave_type_code = 'TOTAL'", (employee_code,))
    row = cur.fetchone()
    conn.close()
    if row is None: return {"success": False, "message": "No balance record."}
    return {"success": True, "employee_code": employee_code, "balance_days": row[0]}

@mcp.tool()
def book_leave(employee_code: str, leave_type: str, start_date: str, end_date: str, reason: str = ""):
    """Book a leave and deduct from total balance. start_date/end_date: YYYY-MM-DD"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        days_to_deduct = calculate_days_logic(start_date, end_date)
        cur.execute("SELECT balance_days FROM leave_balances WHERE employee_code = ? AND leave_type_code = 'TOTAL'", (employee_code,))
        row = cur.fetchone()
        if not row or row[0] < days_to_deduct:
            return {"success": False, "message": "Insufficient balance."}

        # Update balance
        cur.execute("UPDATE leave_balances SET balance_days = balance_days - ?, updated_at = datetime('now') WHERE employee_code = ?", (days_to_deduct, employee_code))
        
        # Save request with total_days
        cur.execute("""
            INSERT INTO leave_requests (employee_code, leave_type_code, start_date, end_date, total_days, reason, status, requested_at)
            VALUES (?, ?, ?, ?, ?, ?, 'BOOKED', datetime('now'))
        """, (employee_code, leave_type, start_date, end_date, days_to_deduct, reason))
        
        conn.commit()
        return {"success": True, "message": f"Booked {days_to_deduct} days. New balance: {row[0] - days_to_deduct}"}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()

@mcp.tool()
def cancel_leave(request_id: int):
    """Cancel a request and refund the 'total_days' back to balance."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT employee_code, total_days FROM leave_requests WHERE id = ?", (request_id,))
        row = cur.fetchone()
        if not row: return {"success": False, "message": "Not found."}
        
        emp_code, days_to_refund = row
        cur.execute("UPDATE leave_balances SET balance_days = balance_days + ? WHERE employee_code = ?", (days_to_refund, emp_code))
        cur.execute("DELETE FROM leave_requests WHERE id = ?", (request_id,))
        conn.commit()
        return {"success": True, "message": f"Cancelled. {days_to_refund} days refunded."}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()

@mcp.tool()
def list_my_leaves(employee_code: str):
    """List all leave requests with their total days count."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, leave_type_code, start_date, end_date, total_days, reason FROM leave_requests WHERE employee_code = ?", (employee_code,))
    rows = cur.fetchall()
    conn.close()
    leaves = [{"id": r[0], "type": r[1], "from": r[2], "to": r[3], "days": r[4], "reason": r[5]} for r in rows]
    return {"success": True, "leaves": leaves}

if __name__ == "__main__":
    mcp.run()
