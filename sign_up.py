import streamlit as st
import re
import sqlite3
from captcha.image import ImageCaptcha
import random, string

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

def insert_user(name, surname, email, password, role="Regular User"):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, surname, email, password, role, is_active, login_attempts)
        VALUES (?, ?, ?, ?, ?, 1, 0)
    ''', (name, surname, email, password, role))
    conn.commit()
    conn.close()

def show_sign_up_page():
    st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h1>Sign up</h1></div>', unsafe_allow_html=True)

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
        name = st.text_input("Name:")
        surname = st.text_input("Surname:")
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm Password:", type="password")

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

        # Password complexity validation
        if password:
            complexity = "Simple"
            suggestions = []
            if len(password) < 8 or len(password) > 64:
                suggestions.append("Password length should be between 8 and 64 characters.")
            else:
                complexity_count = sum([
                    bool(re.search(r'[a-z]', password)),
                    bool(re.search(r'[A-Z]', password)),
                    bool(re.search(r'\d', password)),
                    bool(re.search(r'\W', password))
                ])
                if complexity_count >= 3:
                    complexity = "Strong"
                elif complexity_count >= 2:
                    complexity = "Custom"
                    suggestions.append("Add more character types (uppercase, lowercase, numbers, symbols) to make it stronger.")
                else:
                    suggestions.append("Add more character types (uppercase, lowercase, numbers, symbols) to make it stronger.")

        if submitted:
            # Store the old CAPTCHA and input before regenerating
            st.session_state['old_captcha'] = st.session_state['Captcha']
            st.session_state['old_captcha_input'] = captcha_text

            # Input validation
            if not name:
                st.error("Name is required.")
            elif not surname:
                st.error("Surname is required.")
            elif not email:
                st.error("Email is required.")
            elif "@" not in email or "." not in email:
                st.error("Invalid email address.")
            elif not password:
                st.error("Password is required.")
            elif len(password) < 8 or len(password) > 64:
                st.error("Password must be between 8 and 64 characters long.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif complexity != "Strong":
                if suggestions:
                    for suggestion in suggestions:
                        st.error(f"Password is not strong enough. Please: {suggestion}")
            elif not captcha_text:
                st.error("Please enter the captcha code.")
            elif st.session_state['Captcha'] != captcha_text:
                # Generate a new CAPTCHA and rerun the app
                st.session_state['Captcha'] = generate_captcha()
                st.rerun()
            else:
                if st.session_state['Captcha'] == captcha_text:
                    # Process successful login
                    st.success("Captcha verified. Proceeding with login...")
                    # Insert user into the database
                    insert_user(name, surname, email, password)
                    st.session_state.user_name = name  # Store the user's name in the session state
                    st.session_state.logged_in = True  # Set the login status
                    st.success(f"Welcome, {name}! Your account has been created.")
                    navigate_to("sign_up_success")
                    del st.session_state['Captcha']
                
    # Display error if the previous CAPTCHA attempt was incorrect
    if (
        st.session_state.get('old_captcha') 
        and st.session_state.get('old_captcha_input') != st.session_state['old_captcha']
        ):
        st.error(f"The entered CAPTCHA code was incorrect. Please try again.")            
    
    st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h6>Already have an account? </h6></div>', unsafe_allow_html=True)
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
    if st.button("Log In", key="log_in_button"):
            navigate_to("log_in")