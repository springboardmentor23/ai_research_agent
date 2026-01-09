import sqlite3

DB_NAME = "papers.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            title TEXT,
            authors TEXT,
            year INTEGER,
            url TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_paper(topic, title, authors, year, url):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO papers (topic, title, authors, year, url)
        VALUES (?, ?, ?, ?, ?)
    """, (topic, title, authors, year, url))

    conn.commit()
    conn.close()


def fetch_papers_by_topic(topic):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, authors, year, url
        FROM papers
        WHERE topic = ?
    """, (topic,))

    results = cursor.fetchall()
    conn.close()
    return results