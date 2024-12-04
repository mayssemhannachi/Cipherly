import sqlite3

def alter_secrets_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        ALTER TABLE secrets ADD COLUMN user_id INTEGER
    ''')
    conn.commit()
    conn.close()

# Run the function to alter the table
alter_secrets_table()
print("Secrets table altered successfully.")