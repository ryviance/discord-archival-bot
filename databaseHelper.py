import sqlite3

# Initialize the database (create tables if they don't exist)
def init_db():
    conn = sqlite3.connect('archives.db')
    cursor = conn.cursor()

    # Create a table for archives (name, content)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS archives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        content TEXT NOT NULL
    )
    ''')

    # Create a table for attachments (archive_id, attachment_url)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        archive_id INTEGER NOT NULL,
        attachment_url TEXT NOT NULL,
        FOREIGN KEY(archive_id) REFERENCES archives(id)
    )
    ''')

    conn.commit()
    conn.close()

# Function to save archive and attachments in the database
def save_archive(name, messages, attachments):
    conn = sqlite3.connect('archives.db')
    cursor = conn.cursor()

    # Save the archived message (name and content)
    cursor.execute('INSERT INTO archives (name, content) VALUES (?, ?)', (name, "\n".join(messages)))
    archive_id = cursor.lastrowid  # Get the ID of the last inserted row

    # Save the attachments, linked to the archive by archive_id
    for attachment in attachments:
        cursor.execute('INSERT INTO attachments (archive_id, attachment_url) VALUES (?, ?)', (archive_id, attachment))

    conn.commit()
    conn.close()

# Function to retrieve archived messages and attachments
def retrieve_archive(name):
    conn = sqlite3.connect('archives.db')
    cursor = conn.cursor()

    # Fetch the archive with the given name
    cursor.execute('SELECT content FROM archives WHERE name = ?', (name,))
    content = cursor.fetchone()

    # If no content is found
    if not content:
        return None, None

    # Fetch attachments linked to this archive
    cursor.execute('SELECT attachment_url FROM attachments WHERE archive_id = (SELECT id FROM archives WHERE name = ?)', (name,))
    attachments = cursor.fetchall()

    conn.close()

    # Convert attachments into a simple list
    attachment_urls = [attachment[0] for attachment in attachments]

    return content[0], attachment_urls