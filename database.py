import sqlite3

DB_FILE = "papers.db"

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            title TEXT NOT NULL,
            authors TEXT,
            year INTEGER,
            url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database table created/verified in {DB_FILE}")

def insert_paper(topic, title, authors, year, url):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO papers (topic, title, authors, year, url)
            VALUES (?, ?, ?, ?, ?)
        ''', (topic, title, authors, year, url))
        
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Duplicate entry skipped: {title}")
    finally:
        conn.close()

def get_papers_by_topic(topic):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM papers WHERE topic = ?', (topic,))
    papers = cursor.fetchall()
    conn.close()
    
    return papers

def delete_papers_by_topic(topic):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM papers WHERE topic = ?', (topic,))
    conn.commit()
    conn.close()
    print(f"Deleted all papers for topic: {topic}")
