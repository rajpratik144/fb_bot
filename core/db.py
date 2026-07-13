# core/db.py
import sqlite3
import os

DB_PATH = "app_memory.db"

def init_db():
    """Creates the database file and tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Table to store chat history and owner commands
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history 
                 (thread_id TEXT, role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    # Table to store a log of feed posts made from the CSV
    c.execute('''CREATE TABLE IF NOT EXISTS post_history 
                 (topic TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()
    if not os.path.exists(DB_PATH):
        print("📁 Database created: app_memory.db")

def save_chat_message(thread_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (thread_id, role, content) VALUES (?, ?, ?)", (thread_id, role, content))
    conn.commit()
    conn.close()

def get_thread_history(thread_id, limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_history WHERE thread_id = ? ORDER BY timestamp DESC LIMIT ?", (thread_id, limit))
    rows = c.fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

def get_last_bot_message(thread_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT content FROM chat_history WHERE thread_id = ? AND role = 'assistant' ORDER BY timestamp DESC LIMIT 1", (thread_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# core/db.py

def log_successful_post(topic):
    """Records a successful post in the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO post_history (topic) VALUES (?)", (topic,))
    conn.commit()
    conn.close()
    print(f"💾 Database Updated: Topic '{topic}' recorded.")

def get_today_post_count():
    """Returns how many posts were made in the last 24 hours."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM post_history WHERE timestamp > datetime('now', '-1 day')")
    count = c.fetchone()[0]
    conn.close()
    return count