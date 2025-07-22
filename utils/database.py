import sqlite3
from datetime import datetime

def create_upload_table():
    conn = sqlite3.connect("data/user_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS upload_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            filename TEXT,
            upload_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_upload(username, filename):
    conn = sqlite3.connect("data/user_data.db")
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO upload_history (username, filename, upload_time) VALUES (?, ?, ?)",
              (username, filename, now))
    conn.commit()
    conn.close()

def fetch_uploads():
    conn = sqlite3.connect("data/user_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM upload_history ORDER BY upload_time DESC")
    rows = c.fetchall()
    conn.close()
    return rows
