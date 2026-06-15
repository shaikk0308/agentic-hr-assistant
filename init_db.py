import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(exist_ok=True)


def create_employees_db():
    db_path = DB_DIR / "employees.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_code TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            date_of_joining TEXT NOT NULL,
            department TEXT,
            designation TEXT,
            manager_employee_code TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )

    now = datetime.utcnow().isoformat()
    # only insert sample data if table is empty
    cur.execute("SELECT COUNT(*) FROM employees;")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            """
            INSERT INTO employees (
                employee_code, first_name, last_name, email, phone,
                date_of_joining, department, designation,
                manager_employee_code, is_active, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "E1000",
                    "Anita",
                    "Rao",
                    "anita.rao@acmecorp.com",
                    "9876500000",
                    "2018-01-10",
                    "Engineering",
                    "Engineering Manager",
                    None,
                    1,
                    now,
                    now,
                ),
                (
                    "E1001",
                    "Rahul",
                    "Sharma",
                    "rahul.sharma@acmecorp.com",
                    "9876543210",
                    "2021-04-15",
                    "Engineering",
                    "Senior Software Engineer",
                    "E1000",
                    1,
                    now,
                    now,
                ),
                (
                    "E1002",
                    "Priya",
                    "Iyer",
                    "priya.iyer@acmecorp.com",
                    "9876543211",
                    "2020-06-20",
                    "HR",
                    "HR Business Partner",
                    "E1003",
                    1,
                    now,
                    now,
                ),
            ],
        )

    conn.commit()
    conn.close()
    print(f"Initialized {db_path}")


def create_leave_db():
    db_path = DB_DIR / "leave.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS leave_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            annual_allocation INTEGER NOT NULL
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS leave_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_code TEXT NOT NULL,
            leave_type_code TEXT NOT NULL,
            balance_days REAL NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_code TEXT NOT NULL,
            leave_type_code TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            reason TEXT,
            status TEXT NOT NULL,
            requested_at TEXT NOT NULL,
            decided_at TEXT
        );
        """
    )

    now = datetime.utcnow().isoformat()
    # seed if empty
    cur.execute("SELECT COUNT(*) FROM leave_types;")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            """
            INSERT INTO leave_types (code, name, annual_allocation)
            VALUES (?, ?, ?)
            """,
            [
                ("CL", "Casual Leave", 12),
                ("PL", "Privilege Leave", 18),
            ],
        )

    cur.execute("SELECT COUNT(*) FROM leave_balances;")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            """
            INSERT INTO leave_balances (
                employee_code, leave_type_code, balance_days, updated_at
            ) VALUES (?, ?, ?, ?)
            """,
            [
                ("E1001", "CL", 5.0, now),
                ("E1001", "PL", 10.0, now),
            ],
        )

    conn.commit()
    conn.close()
    print(f"Initialized {db_path}")


def create_compensation_db():
    db_path = DB_DIR / "compensation.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS compensation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_code TEXT NOT NULL,
            base_salary REAL NOT NULL,
            bonus REAL,
            currency TEXT NOT NULL,
            effective_from TEXT NOT NULL,
            effective_to TEXT,
            created_at TEXT NOT NULL
        );
        """
    )

    now = datetime.utcnow().isoformat()
    cur.execute("SELECT COUNT(*) FROM compensation;")
    if cur.fetchone()[0] == 0:
        cur.execute(
            """
            INSERT INTO compensation (
                employee_code, base_salary, bonus, currency,
                effective_from, effective_to, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "E1001",
                1200000.0,
                100000.0,
                "INR",
                "2024-04-01",
                None,
                now,
            ),
        )

    conn.commit()
    conn.close()
    print(f"Initialized {db_path}")


def create_policies_db():
    db_path = DB_DIR / "policies.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            category TEXT,
            effective_from TEXT,
            effective_to TEXT
        );
        """
    )

    cur.execute("SELECT COUNT(*) FROM policies;")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            """
            INSERT INTO policies (
                code, title, body, category, effective_from, effective_to
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "LEAVE_POLICY",
                    "ACME Leave Policy",
                    "Employees are entitled to casual and privilege leave as per allocation. Approval is required from reporting manager.",
                    "HR",
                    "2024-01-01",
                    None,
                ),
                (
                    "WFH_POLICY",
                    "Work From Home Policy",
                    "Employees may work from home up to 3 days per week with manager approval.",
                    "HR",
                    "2024-01-01",
                    None,
                ),
            ],
        )

    conn.commit()
    conn.close()
    print(f"Initialized {db_path}")


if __name__ == "__main__":
    create_employees_db()
    create_leave_db()
    create_compensation_db()
    create_policies_db()
    print("All databases initialized.")
