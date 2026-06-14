import sqlite3
import os

DB_NAME = "drivetest_history.db"

def get_db_path():
    return os.path.join(os.getcwd(), DB_NAME)

def init_db():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            mode TEXT,
            total_rows INTEGER,
            excellent_count INTEGER,
            good_count INTEGER,
            fair_count INTEGER,
            poor_count INTEGER,
            raw_data TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_history(mode, total_rows, excellent, good, fair, poor, raw_data):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO calculation_history (mode, total_rows, excellent_count, good_count, fair_count, poor_count, raw_data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (mode, total_rows, excellent, good, fair, poor, raw_data))
    conn.commit()
    conn.close()

def get_all_history():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, mode, total_rows, excellent_count, good_count, fair_count, poor_count, raw_data 
        FROM calculation_history 
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_history_item(item_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calculation_history WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()