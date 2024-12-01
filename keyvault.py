import sqlite3
from datetime import datetime

# Store Key in Key Vault
def store_key_in_vault(secret_name, key, owner_id):
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO key_vault (secret_name, secret_value, owner_id, created_at)
        VALUES (?, ?, ?, ?)
    """, (secret_name, key.hex(), owner_id, datetime.now()))
    conn.commit()
    conn.close()

# Retrieve Key from Vault
def retrieve_key_from_vault(secret_id):
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT secret_value FROM key_vault WHERE id = ?
    """, (secret_id,))
    result = cursor.fetchone()
    conn.close()
    return bytes.fromhex(result[0]) if result else None