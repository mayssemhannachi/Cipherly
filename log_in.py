import streamlit as st
import re
import sqlite3
from captcha.image import ImageCaptcha
import random, string
import time
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

def show_log_in_page():
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
            # Store the old CAPTCHA and input before regenerating
            st.session_state['old_captcha'] = st.session_state['Captcha']
            st.session_state['old_captcha_input'] = captcha_text

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
                # Generate a new CAPTCHA and rerun the app
                st.session_state['Captcha'] = generate_captcha()
                st.rerun()
            else: 
                if st.session_state['Captcha'] == captcha_text:
                    # Process successful login
                    
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
                            st.session_state.user_name = result[0]  # Store the user's name in the session state
                            st.session_state.logged_in = True  # Set the login status
                            del st.session_state['Captcha']
                            navigate_to("login_success")
                        else:
                            st.error("Your account is inactive. Please contact support.")
                    else:
                        st.error("Invalid credentials.")

    

    # Display error if the previous CAPTCHA attempt was incorrect
    if (
        st.session_state.get('old_captcha') 
        and st.session_state.get('old_captcha_input') != st.session_state['old_captcha']
        ):
        st.error(f"The entered CAPTCHA code was incorrect. Please try again.")

                
    
    st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h6>Do not have an account? </h6></div>', unsafe_allow_html=True)
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
    left:600px;
    top:-40px
    }</style>""", unsafe_allow_html=True)

    st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
    if st.button("Sign up", key="sign_up_button"):
            navigate_to("sign_up")