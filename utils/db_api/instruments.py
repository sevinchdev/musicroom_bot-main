import sqlite3


def get_instruments():
    conn = sqlite3.connect("database.db")  
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM instruments;
    """)

    result = cursor.fetchall()

    conn.close()

    return result