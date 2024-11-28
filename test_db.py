import sqlite3

def print_users():
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Query the users table
    cursor.execute('SELECT * FROM users')

    # Fetch all rows from the query
    rows = cursor.fetchall()

    # Print the column names
    column_names = [description[0] for description in cursor.description]
    print(column_names)

    # Print each row
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    print_users()