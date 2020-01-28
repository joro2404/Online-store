import sqlite3

DB_NAME = 'store.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        number TEXT NOT NULL,
        address TEXT NOT NULL
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS advertisements
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seller_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        release_date TEXT NOT NULL,
        is_available INTEGER,
        FOREIGN KEY (seller_id) REFERENCES users(id)
    )
''')

conn.commit()

class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
