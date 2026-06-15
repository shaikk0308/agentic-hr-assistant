import json
import sqlite3
from pathlib import Path

from fastmcp import FastMCP


BASE_DIR = Path(__file__).resolve().parents[2]  # employee-assistant/
DB_PATH = BASE_DIR / "db" / "employees.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# Create an MCP server instance
mcp = FastMCP("employees-server")


@mcp.tool()
def get_employee_by_code(employee_code: str):
    """
    Get employee details by employee_code.
    Returns a dict with employee data or an error message.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT employee_code, first_name, last_name, email, phone,
               date_of_joining, department, designation,
               manager_employee_code, is_active
        FROM employees
        WHERE employee_code = ?
        """,
        (employee_code,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {
            "success": False,
            "message": f"No employee found for code {employee_code}",
        }

    keys = [
        "employee_code",
        "first_name",
        "last_name",
        "email",
        "phone",
        "date_of_joining",
        "department",
        "designation",
        "manager_employee_code",
        "is_active",
    ]
    employee = dict(zip(keys, row))
    return {"success": True, "employee": employee}


@mcp.tool()
def search_employees_by_name(name: str):
    """
    Search employees by partial first or last name (case-insensitive).
    Returns a list of basic employee info.
    """
    pattern = f"%{name}%"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT employee_code, first_name, last_name, email,
               department, designation
        FROM employees
        WHERE first_name LIKE ? OR last_name LIKE ?
        LIMIT 20
        """,
        (pattern, pattern),
    )
    rows = cur.fetchall()
    conn.close()

    keys = [
        "employee_code",
        "first_name",
        "last_name",
        "email",
        "department",
        "designation",
    ]
    employees = [dict(zip(keys, row)) for row in rows]
    return {"success": True, "employees": employees}


if __name__ == "__main__":
    mcp.run()
