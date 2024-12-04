import sqlite3

def delete_rows_with_user_id_zero():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM encryption_logs WHERE user_id = 0')
    conn.commit()
    conn.close()
    print("Rows with user_id 0 deleted successfully.")

# Run the function to delete rows with user_id 0
delete_rows_with_user_id_zero()