import sqlite3

def create_acls_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS acls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            resource TEXT,
            permission TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# Run the function to create the table
create_acls_table()
print("ACLs table created successfully.")