import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

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

# Function to add a new user
def add_user(name, surname, email, password, role):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, surname, email, password, role, is_active, login_attempts)
        VALUES (?, ?, ?, ?, ?, 1, 0)
    ''', (name, surname, email, password, role))
    conn.commit()
    conn.close()

# Function to delete a user
def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

# Function to update user role
def update_user_role(user_id, new_role):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET role = ?
        WHERE id = ?
    ''', (new_role, user_id))
    conn.commit()
    conn.close()

# Function to deactivate a user
def deactivate_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET is_active = 0
        WHERE id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

# Function to fetch activation requests
def fetch_activation_requests():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ar.id, u.name, u.surname, ar.email, ar.request_time, ar.status
        FROM activation_requests ar
        JOIN users u ON ar.user_id = u.id
        WHERE ar.status = 'Pending'
    ''')
    requests = cursor.fetchall()
    conn.close()
    return requests

# Function to activate a user
def activate_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET is_active = 1
        WHERE id = ?
    ''', (user_id,))
    cursor.execute('''
        UPDATE activation_requests
        SET status = 'Approved'
        WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

# Function to delete processed activation requests and reset the id sequence
def delete_processed_requests_and_reset_id():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM activation_requests WHERE status = "Approved"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "activation_requests"')
    conn.commit()
    conn.close()

# Admin Panel Page
def show_admin_panel_page():
    st.success("Welcome Mayssem!")
    st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h1>Admin Panel</h1></div>', unsafe_allow_html=True)

    # Sidebar Navigation
    st.sidebar.title("Admin Dashboard")
    section = st.sidebar.selectbox("Choose Section", ["Overview", "Users",  "Guests", "Encryption Algorithms", "Key Vault", "Logs"])

    # Example Queries (Replace with actual queries based on your schema)
    user_count_query = "SELECT COUNT(*) FROM users WHERE role = ?"
    guest_count_query = "SELECT COUNT(*) FROM users WHERE role = 'Guest'"
    encryption_usage_query = "SELECT encryption_type, COUNT(*) FROM encryption_logs GROUP BY encryption_type"
    recent_encryption_query = "SELECT encryption_type, user_id, timestamp FROM encryption_logs ORDER BY timestamp DESC LIMIT 5"
    user_growth_query = "SELECT DATE(created_at), COUNT(*) FROM users GROUP BY DATE(created_at)"
    logs_query = "SELECT user_id, user_name, action, timestamp FROM logs ORDER BY timestamp DESC"

    # Fetch data
    user_counts = {
        "Guests": fetch_data(user_count_query, ("Guest",))[0][0],
        "Regular Users": fetch_data(user_count_query, ("Regular User",))[0][0],
        "Admins": fetch_data(user_count_query, ("Admin",))[0][0],
    }
    guest_counts = fetch_data(guest_count_query)[0][0]
    encryption_usage = dict(fetch_data(encryption_usage_query))
    recent_encryption = fetch_data(recent_encryption_query)
    user_growth = fetch_data(user_growth_query)
    logs = fetch_data(logs_query)

    # Display Section
    if section == "Overview":
        st.title("Admin Dashboard Overview")
        st.metric("Total Users", sum(user_counts.values()))
        st.metric("Total Guests", guest_counts)
        st.metric("Total Encryptions", sum(encryption_usage.values()))
    
    elif section == "Guests":
        st.title("Guest Statistics")
        guest_data_query = "SELECT ip_address, user_agent, created_at FROM users WHERE role = 'Guest'"
        guest_data = fetch_data(guest_data_query)
        guest_df = pd.DataFrame(guest_data, columns=["IP Address", "User Agent", "Created At"])
        st.dataframe(guest_df)

        # Guest Visits Over Time
        st.subheader("Guest Visits Over Time")
        guest_df['Created At'] = pd.to_datetime(guest_df['Created At'])
        guest_visits_over_time = guest_df.groupby(guest_df['Created At'].dt.date).size().reset_index(name='Count')
        st.line_chart(guest_visits_over_time.set_index('Created At'))

        # User Agent Distribution
        st.subheader("User Agent Distribution")
        user_agent_distribution = guest_df['User Agent'].value_counts().reset_index()
        user_agent_distribution.columns = ['User Agent', 'Count']
        fig = px.pie(user_agent_distribution, names='User Agent', values='Count', title='User Agent Distribution')
        st.plotly_chart(fig)

        # IP Address Distribution
        st.subheader("IP Address Distribution")
        ip_address_distribution = guest_df['IP Address'].value_counts().reset_index()
        ip_address_distribution.columns = ['IP Address', 'Count']
        st.bar_chart(ip_address_distribution.set_index('IP Address'))

    
    elif section == "Encryption Algorithms":
        st.title("Encryption Usage")
        # Recent Encryption Activities
        st.subheader("Recent Encryption Activities")
        recent_encryption_df = pd.DataFrame(recent_encryption, columns=["Encryption Type", "User ID", "Timestamp"])
        st.table(recent_encryption_df)
        
        st.bar_chart(pd.DataFrame.from_dict(encryption_usage, orient="index", columns=["Count"]))

        # Encryption Types Distribution
        st.subheader("Encryption Types Distribution")
        encryption_usage_df = pd.DataFrame(list(encryption_usage.items()), columns=["Encryption Type", "Count"])
        fig = px.pie(encryption_usage_df, names="Encryption Type", values="Count", title="Encryption Types Distribution")
        st.plotly_chart(fig)
    elif section == "Key Vault":
        st.title("Key Vault Statistics")
    elif section == "Users":
        st.title("User Statistics")

        # Display All Users
        st.subheader("All Users")
        all_users_query = "SELECT id, name, surname, email, role, is_active,login_attempts FROM users"
        all_users = fetch_data(all_users_query)
        all_users_df = pd.DataFrame(all_users, columns=["ID", "Name", "Surname", "Email", "Role", "Active","login_attempts"])
        st.dataframe(all_users_df)

        # Total Users by Role
        st.subheader("Total Users by Role")
        st.bar_chart(pd.DataFrame.from_dict(user_counts, orient="index", columns=["Count"]))

        # User Growth Over Time
        st.subheader("User Growth Over Time")
        user_growth_df = pd.DataFrame(user_growth, columns=["Date", "Count"])
        st.line_chart(user_growth_df.set_index("Date"))

         # Add and Delete User Form
        st.subheader("Add or Delete User")
        
        with st.form(key="manage_user_form"):
            name = st.text_input("Name")
            surname = st.text_input("Surname")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["Regular User", "Admin"])
            add_user_button = st.form_submit_button(label="Add User")

            user_id_to_delete = st.number_input("Enter User ID to Delete", min_value=1)
            delete_user_button = st.form_submit_button(label="Delete User")

            if add_user_button:
                add_user(name, surname, email, password, role)
                st.success("User added successfully.")

            if delete_user_button:
                delete_user(user_id_to_delete)
                st.success("User deleted successfully.")

        

        # Change User Role
        st.subheader("Change User Role")
        user_id_to_change = st.number_input("Enter User ID to Change Role", min_value=1)
        new_role = st.selectbox("New Role", ["Regular User", "Admin"])
        change_role_button = st.button("Change Role")

        if change_role_button:
            update_user_role(user_id_to_change, new_role)
            st.success("User role updated successfully.")

        # Deactivate User
        st.subheader("Deactivate User")
        user_id_to_deactivate = st.number_input("Enter User ID to Deactivate", min_value=1)
        deactivate_user_button = st.button("Deactivate User")

        if deactivate_user_button:
            deactivate_user(user_id_to_deactivate)
            st.success("User deactivated successfully.")
    
        st.title("Activation Requests")
        # Fetch and display activation requests
        activation_requests = fetch_activation_requests()
        activation_requests_df = pd.DataFrame(activation_requests, columns=["Request ID", "Name", "Surname", "Email", "Request Time", "Status"])
        st.dataframe(activation_requests_df)

        # Approve Activation Request
        st.subheader("Approve Activation Request")
        request_id_to_approve = st.number_input("Enter Request ID to Approve", min_value=1)
        approve_request_button = st.button("Approve Request")

        if approve_request_button:
            # Fetch the user_id from the activation request
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute('SELECT user_id FROM activation_requests WHERE id = ?', (request_id_to_approve,))
            user_id = cursor.fetchone()[0]
            conn.close()

            # Activate the user
            activate_user(user_id)
            st.success("User account activated successfully.")

            # Delete processed requests and reset the id sequence
            delete_processed_requests_and_reset_id()

    elif section == "Logs":
        st.title("Application Logs")
        logs_df = pd.DataFrame(logs, columns=["User ID", "User Name", "Action", "Timestamp"])
        st.dataframe(logs_df)

# Call the function to render the admin page
if __name__ == "__main__":
    show_admin_panel_page()