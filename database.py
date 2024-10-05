import sqlite3

def init_db():
    conn = sqlite3.connect('archives.db')
    cursor = conn.cursor

    # Create table for archives(name, content)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS archives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        content TEXT NOT NULL
    )
    ''')

    # Create table for attachments(archive_id, attachment_url)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        archive_id INTEGER NOT NULL,
        attachment_url TEXT NOT NULL,
        FOREIGN KEY(archive_id) REFERENCES archive(id)
    )
    ''')

    conn.commit()
    conn.close()