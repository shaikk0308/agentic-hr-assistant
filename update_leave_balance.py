import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "employees.db"

def update_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        print("Adding password column to employees table...")
        # 1. Add the password column
        cur.execute("ALTER TABLE employees ADD COLUMN password TEXT")
        
        # 2. Set a default password for everyone (e.g., 'password123')
        # In production, these would be hashed, but we'll keep it simple for now.
        cur.execute("UPDATE employees SET password = 'password123'")
        
        conn.commit()
        print("Success! All employees can now log in with 'password123'.")
    except sqlite3.OperationalError:
        print("Column 'password' already exists. Skipping.")
    finally:
        conn.close()

if __name__ == "__main__":
    update_schema()
