import sqlite3

def create_secrets_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Run the function to create the table
create_secrets_table()
print("Secrets table created successfully.")