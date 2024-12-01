import sqlite3

# Connect to the database
def get_db_connection():
    return sqlite3.connect('users.db')

# Create the key_vault table
def setup_key_vault():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS key_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            secret_name TEXT NOT NULL,
            secret_value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Add a secret
def add_secret(user_email, secret_name, secret_value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO key_vault (user_email, secret_name, secret_value)
        VALUES (?, ?, ?)
    ''', (user_email, secret_name, secret_value))
    conn.commit()
    conn.close()

# Retrieve secrets for a user
def get_secrets(user_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT secret_name, secret_value, created_at FROM key_vault
        WHERE user_email = ?
    ''', (user_email,))
    secrets = cursor.fetchall()
    conn.close()
    return secrets