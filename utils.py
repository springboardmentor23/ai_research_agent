import sqlite3
import json
from database import DB_FILE
from json_store import JSON_FILE

def export_database_to_json(output_file="papers_export.json"):
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM papers')
        rows = cursor.fetchall()
        
        data = {
            "total_papers": len(rows),
            "papers": [dict(row) for row in rows]
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"Database exported to {output_file}")
        conn.close()
    except Exception as e:
        print(f"Export error: {e}")

def count_papers_in_database():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM papers')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Count error: {e}")
        return 0

def count_papers_by_topic():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT topic, COUNT(*) as count FROM papers GROUP BY topic')
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Count error: {e}")
        return []

def search_papers_in_database(keyword):
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = '%' + keyword + '%'
        cursor.execute('SELECT * FROM papers WHERE title LIKE ? OR authors LIKE ?', 
                      (query, query))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"Search error: {e}")
        return []

def display_statistics():
    print("\n" + "=" * 60)
    print("RESEARCH PAPER STATISTICS")
    print("=" * 60)
    
    total = count_papers_in_database()
    print(f"\nTotal Papers in Database: {total}")
    
    topics = count_papers_by_topic()
    if topics:
        print("\nPapers by Topic:")
        for topic, count in topics:
            print(f"  - {topic}: {count} paper(s)")
    
    print("\n" + "=" * 60 + "\n")

def print_database_info():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        print("\n" + "=" * 60)
        print("DATABASE INFORMATION")
        print("=" * 60)
        print(f"\nDatabase File: {DB_FILE}")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
            
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print(f"    Columns: {len(columns)}")
            for col in columns:
                print(f"      - {col[1]} ({col[2]})")
        
        print("\n" + "=" * 60 + "\n")
        conn.close()
    except Exception as e:
        print(f"Info error: {e}")

if __name__ == "__main__":
    print("Utility functions for AI Research Paper Retrieval System")
