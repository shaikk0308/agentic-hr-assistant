import sqlite3
from pathlib import Path
from datetime import datetime
import random

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(exist_ok=True)


def setup_realistic_data():
    """Initializes 3 SQLite databases with 15 employees and full history."""

    # Connect to the databases
    emp_conn = sqlite3.connect(DB_DIR / "employees.db")
    leave_conn = sqlite3.connect(DB_DIR / "leave.db")
    comp_conn = sqlite3.connect(DB_DIR / "compensation.db")

    emp_cur = emp_conn.cursor()
    leave_cur = leave_conn.cursor()
    comp_cur = comp_conn.cursor()

    print("Cleaning up old data...")
    emp_cur.execute("DROP TABLE IF EXISTS employees")
    leave_cur.execute("DROP TABLE IF EXISTS leave_types")
    leave_cur.execute("DROP TABLE IF EXISTS leave_balances")
    leave_cur.execute("DROP TABLE IF EXISTS leave_requests")
    comp_cur.execute("DROP TABLE IF EXISTS compensation")

    # --- 1. EMPLOYEES TABLE ---
    print("Creating employees...")
    emp_cur.execute("""
        CREATE TABLE employees (
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
            updated_at TEXT NOT NULL,
            password TEXT
        )
    """)

    employees_data = [
        ("E1001", "Rahul", "Sharma", "Engineering", "Lead Engineer", "E1015", "9876543201"),
        ("E1002", "Priya", "Iyer", "HR", "HR Manager", "E1015", "9876543202"),
        ("E1003", "Vikram", "Singh", "Engineering", "DevOps", "E1001", "9876543203"),
        ("E1004", "Sanya", "Malhotra", "Marketing", "Lead", "E1015", "9876543204"),
        ("E1005", "Arjun", "Reddy", "Engineering", "SDE-2", "E1001", "9876543205"),
        ("E1006", "Deepa", "Nair", "Finance", "Analyst", "E1015", "9876543206"),
        ("E1007", "Rohan", "Gupta", "Engineering", "SDE-1", "E1005", "9876543207"),
        ("E1008", "Anjali", "Desai", "HR", "Recruiter", "E1002", "9876543208"),
        ("E1009", "Karan", "Mehta", "Sales", "Manager", "E1015", "9876543209"),
        ("E1010", "Neha", "Kapoor", "Sales", "Associate", "E1009", "9876543210"),
        ("E1011", "Amit", "Patel", "Engineering", "Intern", "E1007", "9876543211"),
        ("E1012", "Sneha", "Joshi", "Finance", "Controller", "E1006", "9876543212"),
        ("E1013", "Zaid", "Khan", "Engineering", "Architect", "E1001", "9876543213"),
        ("E1014", "Meera", "Sen", "Marketing", "Designer", "E1004", "9876543214"),
        ("E1015", "Anita", "Rao", "Management", "Director", None, "9876543215"),
    ]

    for emp in employees_data:
        employee_code = emp[0]
        first_name = emp[1]
        last_name = emp[2]
        department = emp[3]
        designation = emp[4]
        manager_employee_code = emp[5]
        phone = emp[6]
        email = f"{first_name.lower()}@acme.com"
        password = f"{employee_code.lower()}@123"

        emp_cur.execute("""
            INSERT INTO employees (
                employee_code,
                first_name,
                last_name,
                email,
                phone,
                date_of_joining,
                department,
                designation,
                manager_employee_code,
                is_active,
                created_at,
                updated_at,
                password
            )
            VALUES (?, ?, ?, ?, ?, '2023-01-01', ?, ?, ?, 1, datetime('now'), datetime('now'), ?)
        """, (
            employee_code,
            first_name,
            last_name,
            email,
            phone,
            department,
            designation,
            manager_employee_code,
            password,
        ))

    # --- 2. LEAVE TABLES ---
    print("Creating leave records...")

    leave_cur.execute("""
        CREATE TABLE leave_types (
            id INTEGER PRIMARY KEY,
            code TEXT UNIQUE,
            name TEXT,
            annual_allocation INTEGER
        )
    """)

    leave_cur.executemany("""
        INSERT INTO leave_types (code, name, annual_allocation)
        VALUES (?, ?, ?)
    """, [
        ("CL", "Casual Leave", 12),
        ("PL", "Privilege Leave", 18),
    ])

    leave_cur.execute("""
        CREATE TABLE leave_balances (
            id INTEGER PRIMARY KEY,
            employee_code TEXT,
            leave_type_code TEXT,
            balance_days REAL,
            updated_at TEXT
        )
    """)

    leave_cur.execute("""
        CREATE TABLE leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_code TEXT NOT NULL,
            leave_type_code TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            total_days INTEGER NOT NULL,
            reason TEXT,
            status TEXT NOT NULL,
            requested_at TEXT NOT NULL
        )
    """)

    def get_days(start_date, end_date):
        return (
            datetime.strptime(end_date, "%Y-%m-%d")
            - datetime.strptime(start_date, "%Y-%m-%d")
        ).days + 1

    reasons = ["Family Function", "Medical", "Personal Work", "Vacation", "Rest"]

    for emp in employees_data:
        code = emp[0]
        used = 0

        # Every employee gets 2 booked leaves automatically, total 5 days used
        for date_range in [("2026-01-05", "2026-01-06"), ("2026-02-10", "2026-02-12")]:
            days = get_days(date_range[0], date_range[1])

            leave_cur.execute("""
                INSERT INTO leave_requests (
                    employee_code,
                    leave_type_code,
                    start_date,
                    end_date,
                    total_days,
                    reason,
                    status,
                    requested_at
                )
                VALUES (?, 'CL', ?, ?, ?, ?, 'BOOKED', datetime('now'))
            """, (
                code,
                date_range[0],
                date_range[1],
                days,
                random.choice(reasons),
            ))

            used += days

        # Unified Balance: Initial 24.0 - 5.0 used = 19.0
        leave_cur.execute("""
            INSERT INTO leave_balances (
                employee_code,
                leave_type_code,
                balance_days,
                updated_at
            )
            VALUES (?, 'TOTAL', ?, datetime('now'))
        """, (code, 24.0 - used))

    # --- 3. COMPENSATION TABLE ---
    print("Creating compensation records...")

    comp_cur.execute("""
        CREATE TABLE compensation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_code TEXT NOT NULL,
            base_salary REAL,
            bonus REAL,
            currency TEXT,
            effective_from TEXT,
            effective_to TEXT,
            created_at TEXT
        )
    """)

    for emp in employees_data:
        comp_cur.execute("""
            INSERT INTO compensation (
                employee_code,
                base_salary,
                bonus,
                currency,
                effective_from,
                created_at
            )
            VALUES (?, ?, ?, 'INR', '2025-01-01', datetime('now'))
        """, (
            emp[0],
            random.randint(800000, 2200000),
            random.randint(10000, 60000),
        ))

    # Finalize
    emp_conn.commit()
    leave_conn.commit()
    comp_conn.commit()

    emp_conn.close()
    leave_conn.close()
    comp_conn.close()

    print("\nSUCCESS: All databases are initialized with 15 Employees.")
    print("Default Leave Balance for everyone: 19.0 days (24.0 total - 5.0 already booked).")


if __name__ == "__main__":
    setup_realistic_data()
