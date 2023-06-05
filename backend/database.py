import sqlite3

conn = sqlite3.connect('Users.db')
cursor = conn.cursor()

# create table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
''')

conn.commit()
conn.close()