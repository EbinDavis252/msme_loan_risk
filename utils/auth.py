import hashlib
import sqlite3

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_table():
    conn = sqlite3.connect("data/user_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, role='user'):
    conn = sqlite3.connect("data/user_data.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)",
              (username, hash_password(password), role))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("data/user_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result
