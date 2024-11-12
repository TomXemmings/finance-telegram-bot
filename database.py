import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    c.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY
            )
        ''')
    c.execute('SELECT COUNT(*) FROM admins')
    if c.fetchone()[0] == 0:
        # Change to your Telegram user ID
        first_admin_id = 1111
        c.execute('INSERT INTO admins (user_id) VALUES (?)', (first_admin_id,))
        print(f"Первый администратор с user_id {first_admin_id} добавлен.")
    conn.commit()
    conn.close()

def add_item(table, name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    try:
        c.execute(f'INSERT INTO {table} (name) VALUES (?)', (name,))
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False
    conn.close()
    return result

def remove_item(table, name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f'DELETE FROM {table} WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def get_items(table):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f'SELECT name FROM {table}')
    items = [row[0] for row in c.fetchall()]
    conn.close()
    return items

def add_admin(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO admins (user_id) VALUES (?)', (user_id,))
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False
    conn.close()
    return result

def remove_admin(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def is_admin(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM admins WHERE user_id = ?', (user_id,))
    result = c.fetchone() is not None
    conn.close()
    return result

def get_admins():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM admins')
    admins = [row[0] for row in c.fetchall()]
    conn.close()
    return admins
