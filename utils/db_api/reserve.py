import sqlite3

from db import get_connection


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    # Drop the table if it already exists
    cursor.execute("DROP TABLE IF EXISTS reservations;")

    # Create the table with the correct schema (including group_number)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        fullname TEXT NOT NULL,
        group_number TEXT NOT NULL,  
        day DATE NOT NULL,
        time TIME NOT NULL,
        instrument TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        responsibility_confirmation BOOLEAN NOT NULL
    )
    """)

    conn.commit()
    conn.close()



def get_user_info(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT fullname, student_id, group_number, phone_number
        FROM reservations
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))

    result = cursor.fetchone()
    conn.close()
    return result



