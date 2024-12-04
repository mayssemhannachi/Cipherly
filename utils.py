import streamlit as st
import sqlite3
from datetime import datetime


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

