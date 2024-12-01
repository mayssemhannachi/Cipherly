import streamlit as st
import re
import sqlite3
from captcha.image import ImageCaptcha
import random, string
from add_guest_to_db import handle_guest_action


def navigate_to(page):
    st.session_state.page = page
    print(f"Navigate to {page}")
    st.rerun()  # Force app to rerun and reflect the change immediately

# define the constants
length_captcha = 4
width = 200
height = 150

def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length_captcha))

def increment_login_attempts(email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET login_attempts = login_attempts + 1
        WHERE email = ?
    ''', (email,))
    conn.commit()
    conn.close()

def show_log_in_error_page():
    handle_guest_action()
    st.warning("You need to log in to access the Caesar Cipher. Please log in first.")
    st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h1>Log In</h1></div>', unsafe_allow_html=True)

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

    # Form definition
    with st.form(key="example_form"):
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")

        # CAPTCHA widget
        if 'Captcha' not in st.session_state:
            st.session_state['Captcha'] = generate_captcha()
        image = ImageCaptcha(width=width, height=height)
        data = image.generate(st.session_state['Captcha'])
        st.image(data)
        
        # Initialize captcha_text in session state if not already present
        if 'captcha_text' not in st.session_state:
            st.session_state.captcha_text = ''
        
        captcha_text = st.text_input('Enter captcha text', value=st.session_state.captcha_text)

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Input validation
            if not email:
                st.error("Please enter your email.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address.")
            elif not password:
                st.error("Please enter your password.")
            elif not captcha_text:
                st.error("Please enter the captcha code.")
            elif st.session_state['Captcha'] != captcha_text:
                print(st.session_state['Captcha'])
                print(captcha_text)
                st.error("The captcha code is incorrect, please try again.")
                del st.session_state['Captcha']

            else:
                # Check credentials from the database
                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, password, is_active FROM users
                    WHERE email = ?
                ''', (email,))
                result = cursor.fetchone()
                conn.close()

                if result and result[1] == password:
                    if result[2] == 1:  # Check if the user is active
                        increment_login_attempts(email)
                        st.session_state.user_name = result[0]  # Store user's name
                        st.session_state.user_email = result[1]  # Store user's email
                        st.session_state.logged_in = True  # Set the login status
                        st.success(f"Welcome, {result[0]}!")
                        del st.session_state['Captcha']
                        navigate_to("caesar_cipher")
                    else:
                        st.error("Your account is inactive. Please contact support.")
                else:
                    st.error("Invalid credentials.")
    
    # Use columns for side-by-side buttons
    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
    
    with col2:
        st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h6>Do not have an account? </h6></div>', unsafe_allow_html=True)
        
    

    with col3:
        st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h6>Read more? </h6></div>', unsafe_allow_html=True)
        
    
    # Spacer to visually separate rows (optional)
    st.markdown('<div style="margin-bottom: -40px;"></div>', unsafe_allow_html=True)

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
    left:60px;
    top:-60px
    }</style>""", unsafe_allow_html=True)

    st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)

    # Use columns for side-by-side buttons
    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

    with col2:
        if st.button("Sign up", key="sign_up_button"):
            navigate_to("sign_up")
    
    with col3:    
        if st.button("Home", key="home_button"):
            navigate_to("home")


