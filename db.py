import os
import sqlite3

# Always use the full path to ensure it's the same everywhere
DB_PATH = os.path.join(os.path.dirname(__file__), "bot.db")

def get_connection():
    return sqlite3.connect(DB_PATH)
