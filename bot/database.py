import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../database/users.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        likes INTEGER DEFAULT 0,
        views INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def increment_likes(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET likes = likes + 1 WHERE id = ?", (user_id,))
    conn.commit()
    cursor.execute("SELECT likes FROM users WHERE id = ?", (user_id,))
    likes = cursor.fetchone()["likes"]
    conn.close()
    return likes

def increment_views(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET views = views + 1 WHERE id = ?", (user_id,))
    conn.commit()
    cursor.execute("SELECT views FROM users WHERE id = ?", (user_id,))
    views = cursor.fetchone()["views"]
    conn.close()
    return views

def get_user_stats(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT likes, views FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"likes": row["likes"], "views": row["views"]}
    return {"likes": 0, "views": 0}