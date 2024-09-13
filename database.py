import sqlite3

# Connect to the database
conn = sqlite3.connect('retrieval.db')
cursor = conn.cursor()

# Create a table for storing document embeddings
cursor.execute('''
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    document_text TEXT,
    embedding BLOB
)
''')

# Create a table for storing user info and API call counts
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    api_calls INTEGER
)
''')
conn.commit()
