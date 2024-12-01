import streamlit as st
import os
from dotenv import load_dotenv
from utils import navigate_to, clear_cache  # Import navigation functions from utils

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Cipherly", page_icon="🔐", layout="wide", initial_sidebar_state="collapsed", menu_items=None)

# Read the CSS file
with open("style.css") as f:
    css = f.read()

# Apply the custom style
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"  # Set the default page to "main"

# Admin login function
def admin_login():
    st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h1>Admin Log In</h1></div>', unsafe_allow_html=True)
    st.markdown("""
    <style>
    /* Custom styling for the form submit button */
    .element-container:has(#form-id-after) + div button {
        background: transparent;
        padding: 0.5rem 0.5rem;
        font-size: 2rem;
        border-top-left-radius: 255px 15px;
        border-top-right-radius: 15px 225px;
        border-bottom-right-radius: 225px 15px;
        border-bottom-left-radius: 15px 255px;
        pointer-events: auto;
        width: 8rem;
    }

    /* Optional: Styling for the form container */
    .element-container:has(#form-id-after) + div {
        position: relative;
        background: transparent;
        padding: 1.5rem 1.5rem;
        font-size: 2rem;
        border-color: black;
        border-top-left-radius: 255px 15px;
        border-top-right-radius: 15px 225px;
        border-bottom-right-radius: 225px 15px;
        border-bottom-left-radius: 15px 255px;
        width: 40rem;
        top: 0px;
        left: 320px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Marker for the form
    st.markdown('<span id="form-id-after"></span>', unsafe_allow_html=True)

    with st.form(key="admin_login_form"):
        username = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_password = os.getenv("ADMIN_PASSWORD")
            if username == admin_email and password == admin_password:
                st.session_state.page = "admin_panel"
                st.rerun()
            else:
                st.error("Invalid credentials")

# Function to show the main page
def show_main_page():
    # Sidebar for user role selection
    st.sidebar.title("Who are you?")
    user_role = st.sidebar.radio("Who are you?", ("Regular User", "Admin"), index=0)

    # Render the current page based on user role
    if user_role == "Admin":
        admin_login()
    elif st.session_state.page == "home" and user_role == "Regular User":
        st.markdown(
            '<div style="position: relative; top: 10px; left: 50px;">'
            '<img src="https://raw.githubusercontent.com/mayssemhannachi/Cipherly/master/stickers/arrow.png" alt="Expand Sidebar" style="width: 200px; height: 200px;transform: scaleX(-1);">'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="centered-text" style="position: relative; top: -180px; left: 50px;"><h1>Cipherly 🔐✨</h1></div>', unsafe_allow_html=True)
        st.markdown('<div class="centered-text" style="position: relative; top: -140px; left: 50px;"><h3>The encryption app that you need</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="centered-text" style="position: relative; top: -100px; left: 50px;"><p>Are you ready to unlock the secrets of encryption? Cipherly is your interactive playground where you can explore two exciting encryption techniques—Caesar Cipher and EAS Encryption. Whether you’re just curious about how data is protected or looking to experiment with encryption and decryption yourself, CipherPlay has you covered.\n With a simple and intuitive interface, you’ll be transforming ordinary text into cryptic codes in no time!</p></div>', unsafe_allow_html=True)

        st.markdown("""
        <style>.element-container:has(#button-after) + div button {
        position: relative;
        background: transparent;
        padding: 0.5rem 0.5rem;
        font-size: 1rem;
        border-top-left-radius: 255px 15px;
        border-top-right-radius: 15px 225px;
        border-bottom-right-radius: 225px 15px;
        border-bottom-left-radius: 15px 255px;
        pointer-events: auto; /* Make the button unclickable */
        width:8rem;
        top:-80px;
        left:60px;
        }</style>""", unsafe_allow_html=True)

        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)

        # Use columns for side-by-side buttons
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

        # Add Python-based navigation for "Log In"
        with col2:
            if st.button("Log In", key="log_in_button"):
                navigate_to("log_in")

        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)

        # Add Python-based navigation for "Sign Up"
        with col3:
            if st.button("Sign Up", key="sign_up_button"):

                navigate_to("sign_up")

        # Spacer to visually separate rows (optional)
        st.markdown('<div style="margin-bottom: 40px;"></div>', unsafe_allow_html=True)

        # Navigation buttons
        col5, col6 = st.columns([1, 1])

        with col5:
            st.markdown('''
                <div class="button-container" style="position: relative; top: -80px; left: 50px;">
                        <a href="?page=caesar_cipher" style="text-decoration: none;">
                            <button type="submit" id="rectangle">
                                <img src="https://raw.githubusercontent.com/mayssemhannachi/Cipherly/master/stickers/caesar.png" alt="Caesar Cipher" style="width: 100px; height: 100px;">
                                Caesar Cipher 
                                <br>
                                Step into the ancient world of Julius 
                                Caesar, who invented one of the 
                                earliest forms of encryption to keep 
                                his military strategies under wraps. 
                                The Caesar Cipher is a substitution 
                                cipher that shifts each letter 
                                in the alphabet by a certain number
                                of positions. Want to send a secret 
                                message like a Roman general?
                                Just pick your shift value, 
                                and Cipherly will do the rest—
                                turning your plain text into a string 
                                of cryptic letters! 
                                Can you crack the code?
                            </button>
                        </a>
                </div>
                        
                ''', unsafe_allow_html=True)

            


        with col6:
            st.markdown('''
                <div class="button-container" style="position: relative; top: -80px; left: 50px;">
                    <a href="?page=eas_encryption" style="text-decoration: none;">
                        <button id="rectangle">
                            <img src="https://raw.githubusercontent.com/mayssemhannachi/Cipherly/master/stickers/security.png" alt="EAS Encryption" style="width: 100px; height: 100px;">        
                            AES Encryption 
                            <br>
                            Enter the world of modern encryption 
                            with AES (Advanced Encryption Standard)
                            Encryption. This technique 
                            uses advanced cryptographic methods 
                            to secure your data, ensuring that 
                            your secrets remain just that—secret.
                            If you want to experience how 
                            today’s encryption algorithms work, 
                            Cipherly lets you encrypt
                            and decrypt messages using this highly 
                            secure approach. 
                            Protect your data like a cybersecurity 
                            pro, and see firsthand how encryption 
                            keeps today’s digital world safe.
                        </button>
                    </a>
                </div>
            ''', unsafe_allow_html=True)

            

        # Spacer to visually separate rows (optional)
        st.markdown('<div style="margin-bottom: 40px;"></div>', unsafe_allow_html=True)

        st.markdown("""
        <style>.element-container:has(#button-after) + div button {
        position: relative;
        background: transparent;
        padding: 0.5rem 0.5rem;
        font-size: 1rem;
        border-top-left-radius: 255px 15px;
        border-top-right-radius: 15px 225px;
        border-bottom-right-radius: 225px 15px;
        border-bottom-left-radius: 15px 255px;
        pointer-events: auto; /* Make the button unclickable */
        width:12rem;
        top:-80px;
        left:60px;
        }</style>""", unsafe_allow_html=True)

        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)

        # Use columns for side-by-side buttons
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

        # Add Python-based navigation for "Log In"
        with col2:
            if st.button('Caesar Cipher'):
                if "user_role" not in st.session_state or st.session_state.user_role is None:
                    navigate_to('log_in_error')

        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)

        # Add Python-based navigation for "Sign Up"
        with col3:
            if st.button('AES Encryption'):
                if "user_role" not in st.session_state or st.session_state.user_role is None:
                    navigate_to('log_in_error_aes')


        

        

# Handle navigation based on session state
if st.session_state.page == "caesar_cipher":
    import caesar_cipher
    caesar_cipher.show_caesar_cipher()
elif st.session_state.page == "eas_encryption":
    # Import EAS Encryption Page
    import eas_encryption
    eas_encryption.show_aes_page()
elif st.session_state.page == "sign_up":
    # Import Sign Up Page
    import sign_up
    sign_up.show_sign_up_page()
elif st.session_state.page == "log_in":
    # Import Log In Page
    import log_in
    log_in.show_log_in_page()
elif st.session_state.page == "admin_panel":
    # Import Admin Panel Page
    import admin_panel
    admin_panel.show_admin_panel_page()
elif st.session_state.page == "encryption":
    # Import Encryption Page
    import encryption
    encryption.encryption_show()
elif st.session_state.page == "home":
    show_main_page()
elif st.session_state.page == "log_in_error":
    import log_in_error
    log_in_error.show_log_in_error_page()
elif st.session_state.page == "key_vault":
    import keyvaultui
    keyvaultui.show_key_vault()
elif st.session_state.page == "log_in_error_aes":
    import log_in_error_aes
    log_in_error_aes.show_log_in_error_aes_page()
elif st.session_state.page == "sign_up_success":
    import sign_up_success
    sign_up_success.encryption_show()
elif st.session_state.page == "login_success":
    import login_success
    login_success.encryption_show()


else:
    show_main_page()