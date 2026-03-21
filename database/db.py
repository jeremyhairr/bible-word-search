import sqlite3

DB_PATH = "database/bible.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 👈 allows dict-like access
    return conn
