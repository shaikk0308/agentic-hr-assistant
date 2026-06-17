import sqlite3
from pathlib import Path
from fastmcp import FastMCP

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "employees.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

mcp = FastMCP("employees-server")


@mcp.tool()
def get_employee_by_code(employee_code: str):
    """
    Get full employee details by employee_code.
    Also resolves the manager's name from the same table.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            e.employee_code,
            e.first_name,
            e.last_name,
            e.email,
            e.phone,
            e.date_of_joining,
            e.department,
            e.designation,
            e.manager_employee_code,
            (m.first_name || ' ' || m.last_name) AS manager_name,
            e.is_active
        FROM employees e
        LEFT JOIN employees m ON e.manager_employee_code = m.employee_code
        WHERE e.employee_code = ?
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
        "manager_name",
        "is_active",
    ]
    return {"success": True, "employee": dict(zip(keys, row))}

@mcp.tool()
def search_employees_by_name(name: str):
    """
    Search employees by full name or partial name.

    Special case:
    - If name is "__ALL__", returns all employees in the organization.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Special case: return all employees
    if name.strip().upper() == "__ALL__":
        cur.execute(
            """
            SELECT
                e.id,
                e.employee_code,
                e.first_name,
                e.last_name,
                e.email,
                e.phone,
                e.department,
                e.designation,
                e.manager_employee_code,
                (m.first_name || ' ' || m.last_name) AS manager_name,
                e.is_active
            FROM employees e
            LEFT JOIN employees m ON e.manager_employee_code = m.employee_code
            ORDER BY e.department, e.first_name
            """
        )

        rows = cur.fetchall()
        conn.close()

        employees = []

        for row in rows:
            employees.append({
                "id": row[0],
                "employee_code": row[1],
                "name": f"{row[2]} {row[3]}",
                "email": row[4] or "",
                "phone": row[5] or "",
                "department": row[6] or "",
                "designation": row[7] or "",
                "manager_employee_code": row[8] or "",
                "manager_name": row[9] or "No Manager",
                "is_active": "Active" if row[10] else "Inactive",
            })

        return {
            "success": True,
            "count": len(employees),
            "employees": employees,
        }

    # Normal name search
    pattern = f"%{name}%"

    cur.execute(
        """
        SELECT
            e.employee_code,
            e.first_name,
            e.last_name,
            e.email,
            e.phone,
            e.date_of_joining,
            e.department,
            e.designation,
            e.manager_employee_code,
            (m.first_name || ' ' || m.last_name) AS manager_name,
            e.is_active
        FROM employees e
        LEFT JOIN employees m ON e.manager_employee_code = m.employee_code
        WHERE
            e.first_name LIKE ?
            OR e.last_name LIKE ?
            OR (e.first_name || ' ' || e.last_name) LIKE ?
        LIMIT 20
        """,
        (pattern, pattern, pattern),
    )

    rows = cur.fetchall()
    conn.close()

    if not rows:
        return {
            "success": False,
            "message": f"No employees found matching '{name}'",
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
        "manager_name",
        "is_active",
    ]

    employees = [dict(zip(keys, row)) for row in rows]

    return {
        "success": True,
        "count": len(employees),
        "employees": employees,
    }

if __name__ == "__main__":
    mcp.run()
