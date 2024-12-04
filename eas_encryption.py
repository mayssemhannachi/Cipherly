import streamlit as st
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import sqlite3
from datetime import datetime
from utils import navigate_to

# AES Encryption Function
def aes_encrypt(text, key):
    key = key.ljust(32)[:32].encode()  # Ensure key is 32 bytes
    iv = os.urandom(16)  # Generate a random Initialization Vector (IV)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Add padding
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()

    # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext  # Combine IV and ciphertext

# AES Decryption Function
def aes_decrypt(encrypted_data, key):
    key = key.ljust(32)[:32].encode()  # Ensure key is 32 bytes
    iv = encrypted_data[:16]  # Extract IV (first 16 bytes)
    ciphertext = encrypted_data[16:]  # Extract ciphertext (rest of the bytes)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    return plaintext.decode()

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

# Function to get user_id by user_name
def get_user_id_by_name(user_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM users WHERE name = ?
    ''', (user_name,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

# Streamlit UI
def show_aes_page():
    # Page styling
    st.markdown("""
    <style>
        .centered-text { text-align: center; margin-bottom: 1rem; }
        textarea, input { width: 100%; padding: 0.8rem; margin: 0.5rem 0; border: 2px solid #ccc; border-radius: 12px; font-size: 1rem; }
        .button-container button { background: linear-gradient(to right, #6a11cb, #2575fc); color: white; border: none; padding: 0.5rem 1rem; font-size: 1rem; border-radius: 25px; cursor: pointer; transition: background 0.3s ease; }
        .button-container button:hover { background: linear-gradient(to right, #2575fc, #6a11cb); }
        @media (max-width: 768px) { textarea, input { font-size: 0.9rem; } .button-container button { font-size: 0.9rem; padding: 0.4rem 0.8rem; } }
    </style>
    """, unsafe_allow_html=True)

    # Welcome header
    user_name = st.session_state.get('user_name', 'User')
    user_id = get_user_id_by_name(user_name)  # Get user_id by user_name
    st.markdown(f'<div class="centered-text"><h1>Welcome, {user_name}!</h1></div>', unsafe_allow_html=True)

    # Page title
    st.markdown('<div class="centered-text"><h2>AES Encryption</h2></div>', unsafe_allow_html=True)
    st.write("Explore the Advanced Encryption Standard (AES) for secure encryption!")

    # AES Input form
    with st.form(key="aes_form"):
        text = st.text_area("Enter your text here:", "", help="Input the text you want to encrypt or decrypt.")
        key = st.text_input("Enter a secret key (max 32 characters):", help="This key will be used for encryption and decryption.")
        operation = st.radio("Choose an operation:", ("Encrypt", "Decrypt"))

        # Submit button
        submitted = st.form_submit_button("Run AES")

        # Process the operation
        if submitted:
            if not text.strip() or not key.strip():
                st.error("Both text and key are required.")
            else:
                try:
                    if operation == "Encrypt":
                        encrypted_data = aes_encrypt(text, key)
                        st.success(f"Encrypted Data (Hex): {encrypted_data.hex()}")  # Show encrypted data in hex
                        # Log the operation
                        log_encryption_operation(user_id, "AES")
                    else:  # Decrypt
                        encrypted_bytes = bytes.fromhex(text)  # Convert hex input to bytes
                        decrypted_text = aes_decrypt(encrypted_bytes, key)
                        st.success(f"Decrypted Text: {decrypted_text}")
                        # Log the operation
                        log_encryption_operation(user_id, "AES")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Navigation Button
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Try Another Encryption"):
        navigate_to("encryption")
    st.markdown('</div>', unsafe_allow_html=True)