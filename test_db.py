import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Query to fetch all rows from the users table
cursor.execute("SELECT * FROM users")

# Fetch all rows
rows = cursor.fetchall()

# Display each row
for row in rows:
    print(row)

# Close the connection
conn.close()