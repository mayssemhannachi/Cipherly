import streamlit as st
import sqlite3
from datetime import datetime
import os


# Function to navigate to a different page
def navigate_to(page):
    st.session_state.page = page
    print(f"Navigate to {page}")
    st.rerun()  # Force app to rerun and reflect the change immediately

# Function to clear cache and reset session state
def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    for key in st.session_state.keys():
        del st.session_state[key]
    navigate_to('home')


# Function to Log Activities
def log_activity(user_id, user_name, action):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO logs (user_id, user_name, action, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (user_id, user_name, action, timestamp))
    conn.commit()
    conn.close()

# manage keyvault secretsimport sqlite3

def add_secret(name, value, user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO secrets (name, value, user_id)
        VALUES (?, ?, ?)
    ''', (name, value, user_id))
    conn.commit()
    conn.close()

def get_secret(name, user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT value FROM secrets WHERE name = ? AND user_id = ?
    ''', (name, user_id))
    secret = cursor.fetchone()
    conn.close()
    return secret[0] if secret else None

def get_all_secrets(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT name, value FROM secrets WHERE user_id = ?', (user_id,))
    secrets = cursor.fetchall()
    conn.close()
    return secrets

def delete_secret(name, user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM secrets WHERE name = ? AND user_id = ?', (name, user_id))
    conn.commit()
    conn.close()

# function to retrieve user id using user name
def get_user_id_by_username(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM users WHERE name = ?
    ''', (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

# function to retrieve user name using user email

def get_user_name_by_email(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name FROM users WHERE email = ?
    ''', (email,))
    user_name = cursor.fetchone()
    conn.close()
    return user_name[0] if user_name else None

# handle encryption keys

def generate_encryption_key(key_type):
    if key_type == "AES":
        return os.urandom(32).hex()  # Generate a 256-bit AES key
    # Add other key types if needed
    return None

def add_encryption_key(user_id, key_type, key_value):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO encryption_keys (user_id, key_type, key_value)
        VALUES (?, ?, ?)
    ''', (user_id, key_type, key_value))
    conn.commit()
    conn.close()

def get_encryption_key(user_id, key_type):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT key_value FROM encryption_keys WHERE user_id = ? AND key_type = ?
    ''', (user_id, key_type))
    key = cursor.fetchone()
    conn.close()
    return key[0] if key else None


def add_acl(user_id, resource, permission):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO acls (user_id, resource, permission)
        VALUES (?, ?, ?)
    ''', (user_id, resource, permission))
    conn.commit()
    conn.close()

def get_acl(user_id, resource):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT permission FROM acls WHERE user_id = ? AND resource = ?
    ''', (user_id, resource))
    acl = cursor.fetchone()
    conn.close()
    return acl[0] if acl else None

def check_permission(user_id, resource, required_permission):
    permission = get_acl(user_id, resource)
    return permission == required_permission