import sqlite3

def create_table():
    try:
        conn = sqlite3.connect("papers.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            authors TEXT,
            year INTEGER,
            abstract TEXT,
            pdf_url TEXT
        )
        """)

        conn.commit()
        conn.close()

        print("✅ Database table ready")

    except Exception as e:
        print("❌ Database error:", e)
