import streamlit as st
from utils import add_secret, get_secret, get_all_secrets, delete_secret, log_activity, get_user_id_by_username
import pandas as pd

# Function to navigate to a different page
def navigate_to(page):
    st.session_state.page = page
    print(f"Navigate to {page}")
    st.rerun()  # Force app to rerun and reflect the change immediately

def show_key_vault():
    st.title("Key Vault")
    st.write("Welcome to the Key Vault! Here, you can store and manage your secrets securely.")

    # Retrieve user name from session state
    user_name = st.session_state.get('user_name', 'guest')
    # Retrieve user ID from the database using the username
    user_id = get_user_id_by_username(user_name)

    # Add a new secret
    st.subheader("Add a New Secret")
    with st.form(key="add_secret_form"):
        secret_name = st.text_input("Secret Name")
        secret_value = st.text_input("Secret Value")
        add_secret_button = st.form_submit_button("Add Secret")

        if add_secret_button:
            if secret_name and secret_value:
                add_secret(secret_name, secret_value, user_id)
                st.success("Secret added successfully.")
                # Log the addition of a new secret
                log_activity(user_id, user_name, f"Added secret: {secret_name}")
                # Clear the input fields by rerunning the script
                st.rerun()
            else:
                st.error("Please enter both secret name and value.")

    # View all secrets
    st.subheader("View All Secrets")
    secrets = get_all_secrets(user_id)
    secret_names = [secret[0] for secret in secrets]  # Extract only the names of the secrets
    secret_names_df = pd.DataFrame(secret_names, columns=["Name"])
    st.dataframe(secret_names_df)

    # View a specific secret
    st.subheader("View a Specific Secret")
    with st.form(key="view_secret_form"):
        secret_name_to_view = st.text_input("Enter the Secret Name to View")
        view_secret_button = st.form_submit_button("View Secret")

        if view_secret_button:
            if secret_name_to_view:
                secret_value = get_secret(secret_name_to_view, user_id)
                if secret_value:
                    st.success(f"Secret Value: {secret_value}")
                    # Log the viewing of a secret
                    log_activity(user_id, user_name, f"Viewed secret: {secret_name_to_view}")
                else:
                    st.error("Secret not found.")
            else:
                st.error("Please enter the secret name.")

    # Delete a secret
    st.subheader("Delete a Secret")
    with st.form(key="delete_secret_form"):
        secret_name_to_delete = st.text_input("Enter the Secret Name to Delete")
        delete_secret_button = st.form_submit_button("Delete Secret")

        if delete_secret_button:
            if secret_name_to_delete:
                delete_secret(secret_name_to_delete, user_id)
                st.success("Secret deleted successfully.")
                # Log the deletion of a secret
                log_activity(user_id, user_name, f"Deleted secret: {secret_name_to_delete}")
                # Clear the input fields by rerunning the script
                st.rerun()
            else:
                st.error("Please enter the secret name.")

    # return to home
    if st.button("Back Home"):
        navigate_to("encryption")

# Call the function to render the key vault page
if __name__ == "__main__":
    show_key_vault()