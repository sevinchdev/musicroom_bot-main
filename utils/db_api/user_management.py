import sqlite3



def add_user(user_id, username, fullname, language ='ru'):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT is_active FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result is not None: 
            cursor.execute('''
                UPDATE users
                SET is_active = 1,
                    language = ?
                WHERE user_id = ?
            ''', (language, user_id))
    else:
        cursor.execute('''
            INSERT INTO users (user_id, username, fullname, is_active, language) 
            VALUES (?, ?, ?, 1, ?)
        ''', (user_id, username, fullname, language))

    conn.commit()
    conn.close()



def is_user_blocked(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT is_blocked FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else False


def set_inactive(user_id):
    if not isinstance(user_id, int):
        raise ValueError("user_id must be an integer")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        UPDATE users
        SET is_active = 0
        WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def active_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT COUNT(*) FROM users WHERE is_active = 1;
    ''')  
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def inactive_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT COUNT(*) FROM users WHERE is_active = 0;
    ''')  
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def blocked_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT COUNT(*) FROM users WHERE is_blocked=1;
    ''')  
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None
    
def toggle_is_blocked(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT is_blocked FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result is None:
        conn.close()
        raise ValueError("User not found in the database.")
    
    current_status = result[0]
    new_status = not current_status
    
    cursor.execute('UPDATE users SET is_blocked = ? WHERE user_id = ?', (new_status, user_id))
    conn.commit()
    conn.close()
    
    return new_status

def get_user_language(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else False

def get_user_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else False

def get_all_userid():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_id FROM users;
    ''')  
    result = cursor.fetchall()
    conn.close()

    return result

def update_user_contact(user_id: int, phone_number: str):
    conn = sqlite3.connect("database.db")  
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users 
        SET phone = ? 
        WHERE user_id = ?
    """, (phone_number, user_id))

    conn.commit()
    conn.close()