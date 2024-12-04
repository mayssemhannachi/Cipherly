import streamlit as st
import sqlite3
from datetime import datetime
from utils import log_activity, navigate_to  # Ensure navigate_to is defined in your utils module

# Caesar cipher logic
def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

# Function to log encryption operations
def log_encryption_operation(user_id, encryption_type):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO encryption_logs (encryption_type, user_id, timestamp)
        VALUES (?, ?, ?)
    ''', (encryption_type, user_id, timestamp))
    conn.commit()
    conn.close()

def show_caesar_cipher():
    # Inline styles for the page
    st.markdown("""
    <style>
        /* Center text for titles */
        .centered-text {
            text-align: center;
            margin-bottom: 1rem;
        }
        
        /* Style for text input, number input, and buttons */
        textarea, input {
            width: 100%;
            padding: 0.8rem;
            margin: 0.5rem 0;
            border: 2px solid #ccc;
            border-radius: 12px;
            font-size: 1rem;
        }
        
        .button-container button {
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            border-radius: 25px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .button-container button:hover {
            background: linear-gradient(to right, #feb47b, #ff7e5f);
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .centered-text h1, .centered-text h2 {
                font-size: 1.5rem;
            }
            
            textarea, input {
                width: 100%;
                font-size: 0.9rem;
            }

            .button-container button {
                font-size: 0.9rem;
                padding: 0.4rem 0.8rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Display a personalized welcome message
    user_name = st.session_state.get('user_name', 'User')  # Default to 'User' if not found
    user_id = st.session_state.get('user_id', 0)  # Default to 0 if not found
    st.markdown(f'<div class="centered-text"><h1>Welcome, {user_name}!</h1></div>', unsafe_allow_html=True)

    # Title for Caesar Cipher
    st.markdown('<div class="centered-text"><h2>Caesar Cipher</h2></div>', unsafe_allow_html=True)
    st.write("Explore the ancient encryption technique used by Julius Caesar!")

    # Input Fields for Caesar Cipher
    with st.form(key="caesar_form"):
        text = st.text_area("Enter your text here:", "", help="Input the text you want to encrypt or decrypt.")
        shift = st.number_input("Enter the shift value (1-25):", min_value=1, max_value=25, value=3)
        operation = st.radio("Choose an operation:", ("Encrypt", "Decrypt"))

        # Form submission button
        submitted = st.form_submit_button("Run Caesar Cipher")

        if submitted:
            if not text.strip():
                st.error("Please enter some text to proceed.")
            else:
                is_decrypt = operation == "Decrypt"
                result = caesar_cipher(text, shift, decrypt=is_decrypt)
                st.success(f"Result: {result}")
                # Log the operation
                log_encryption_operation(user_id, "Caesar Cipher")
                log_activity(user_id, user_name, f"Performed Caesar Cipher {'decryption' if is_decrypt else 'encryption'}")

    # Navigation Buttons
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Try Another Encryption"):
        navigate_to("encryption")
    st.markdown('</div>', unsafe_allow_html=True)