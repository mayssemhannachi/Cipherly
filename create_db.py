import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Step 1: Rename the existing table
cursor.execute("ALTER TABLE users RENAME TO users_backup")

# Step 2: Create the new table with the desired schema
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,
    is_active BOOLEAN,
    login_attempts INTEGER,
    session_id TEXT,
    ip_address TEXT,
    user_agent TEXT,
    visit_time TIMESTAMP
)
''')

# Step 3: Migrate data from the backup table to the new table
cursor.execute('''
INSERT INTO users (id, name, surname, email, password, role, is_active, login_attempts)
SELECT id, name, surname, email, password, role, is_active, login_attempts
FROM users_backup
''')

# Step 4: Drop the backup table
cursor.execute("DROP TABLE users_backup")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Schema updated successfully.")