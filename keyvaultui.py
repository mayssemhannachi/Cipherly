import streamlit as st
from keyvault import add_secret, get_secrets

def show_key_vault():
    # Ensure the user is logged in
    if not st.session_state.get('logged_in', False):
        st.warning("You need to log in to access the Key Vault.")
        return

    # Get user email
    user_email = st.session_state.get('user_email', '')
    st.markdown(f"### Key Vault for {st.session_state.get('user_name', 'User')}")

    # Display user secrets
    st.markdown("#### Your Secrets:")
    secrets = get_secrets(user_email)
    if secrets:
        for secret_name, secret_value, created_at in secrets:
            st.write(f"- **{secret_name}**: {secret_value} (Added on {created_at})")
    else:
        st.write("No secrets found.")

    # Form to add a new secret
    st.markdown("#### Add a New Secret")
    with st.form(key="add_secret_form"):
        secret_name = st.text_input("Secret Name")
        secret_value = st.text_input("Secret Value")
        submit = st.form_submit_button("Add Secret")

        if submit:
            if not secret_name or not secret_value:
                st.error("Both fields are required.")
            else:
                add_secret(user_email, secret_name, secret_value)
                st.success(f"Secret '{secret_name}' added successfully!")
                st.rerun()