import sqlite3

# Connect to the database
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE key_vault (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    secret_name TEXT NOT NULL,
    secret_value TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users (id)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()