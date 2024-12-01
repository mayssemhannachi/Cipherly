import sqlite3

def update_user_role(email, new_role):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET role = ?
        WHERE email = ?
    ''', (new_role, email))
    conn.commit()
    conn.close()

# Update the role of the user 'maysem hannachi' to 'Admin'
update_user_role('h.mayssem2003@gmail.com', 'Admin')
print("User role updated successfully.")