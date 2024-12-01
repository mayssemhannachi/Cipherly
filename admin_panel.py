import streamlit as st
import sqlite3
import pandas as pd

# Database connection
def get_connection():
    return sqlite3.connect("users.db")

# Fetching data from database
def fetch_data(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# Admin Panel Page
def show_admin_panel_page():
    st.success("Welcome Mayssem!")
    st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h1>Admin Panel</h1></div>', unsafe_allow_html=True)

    

    # Sidebar Navigation
    st.sidebar.title("Admin Dashboard")
    section = st.sidebar.selectbox("Choose Section", ["Overview", "User Stats", "Guest Stats", "Encryption Stats", "Key Vault Stats"])

    # Example Queries (Replace with actual queries based on your schema)
    user_count_query = "SELECT COUNT(*) FROM users WHERE role = ?"
    guest_count_query = "SELECT COUNT(*) FROM users WHERE role = 'Guest'"
    encryption_usage_query = "SELECT encryption_type, COUNT(*) FROM encryption_logs GROUP BY encryption_type"

    # Fetch data
    user_counts = {
        "Guests": fetch_data(user_count_query, ("Guest",))[0][0],
        "Regular Users": fetch_data(user_count_query, ("Regular User",))[0][0],
        "Admins": fetch_data(user_count_query, ("Admin",))[0][0],
    }
    guest_counts = fetch_data(guest_count_query)[0][0]
    encryption_usage = dict(fetch_data(encryption_usage_query))


    # Display Section
    if section == "Overview":
        st.title("Admin Dashboard Overview")
        st.metric("Total Users", sum(user_counts.values()))
        st.metric("Total Guests", guest_counts)
        st.metric("Total Encryptions", sum(encryption_usage.values()))

    elif section == "User Stats":
        st.title("User Statistics")
        st.bar_chart(pd.DataFrame.from_dict(user_counts, orient="index", columns=["Count"]))
    elif section == "Guest Stats":
        st.title("Guest Statistics")
        guest_data_query = "SELECT ip_address, user_agent, created_at FROM users WHERE role = 'Guest'"
        guest_data = fetch_data(guest_data_query)
        guest_df = pd.DataFrame(guest_data, columns=["IP Address", "User Agent", "Created At"])
        st.dataframe(guest_df)
    elif section == "Encryption Stats":
        st.title("Encryption Usage")
        st.bar_chart(pd.DataFrame.from_dict(encryption_usage, orient="index", columns=["Count"]))
    elif section == "Key Vault Stats":
        st.title("Key Vault Statistics")

# Call the function to render the admin page
if __name__ == "__main__":
    show_admin_panel_page()