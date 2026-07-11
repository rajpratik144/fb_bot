import sqlite3
from datetime import datetime

class AgentDB:
    def __init__(self, db_path="agent_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Stores chat history per thread
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                sender TEXT,
                content TEXT,
                timestamp DATETIME
            )
        ''')
        # Stores metadata for the Feed (last post time, etc.)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registry (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.conn.commit()

    def log_message(self, thread_id, sender, content):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO messages (thread_id, sender, content, timestamp) VALUES (?, ?, ?, ?)",
            (thread_id, sender, content, datetime.now())
        )
        self.conn.commit()

    def get_last_bot_message(self, thread_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT content FROM messages WHERE thread_id = ? AND sender = 'bot' ORDER BY id DESC LIMIT 1",
            (thread_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else None