import streamlit as st
import pandas as pd
import os
from utils import navigate_to, add_acl, check_permission, get_user_id_by_username, log_activity

# Function to show the encryption page
def encryption_show():
    st.markdown('<div class="centered-text" style="position: relative; top: -10px; left: 50px;"><h1>Cipherly 🔐✨</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="centered-text" style="position: relative; top: -5px; left: 30px;"><h3>The encryption app that you need</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="centered-text" style="position: relative; top: 50px; left: 50px;"><p>Are you ready to unlock the secrets of encryption? Cipherly is your interactive playground where you can explore two exciting encryption techniques—Caesar Cipher and EAS Encryption. Whether you’re just curious about how data is protected or looking to experiment with encryption and decryption yourself, CipherPlay has you covered.\n With a simple and intuitive interface, you’ll be transforming ordinary text into cryptic codes in no time!</p></div>', unsafe_allow_html=True)

    # Spacer to visually separate rows (optional)
    st.markdown('<div style="margin-bottom: 170px;"></div>', unsafe_allow_html=True)

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
                
                    navigate_to('caesar_cipher')

    st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)

    # Add Python-based navigation for "Sign Up"
    with col3:
            if st.button('AES Encryption'):
                
                    navigate_to('eas_encryption')

    # Spacer to visually separate rows (optional)
    st.markdown('<div style="margin-bottom: 0px;"></div>', unsafe_allow_html=True)
    col1,col2,col3=st.columns([2,1,2])
    
    with col2:
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
        left:60px;
        }</style>""", unsafe_allow_html=True)
        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
        if st.button("Go to Key Vault"):
            navigate_to("key_vault")

    

    # Informational message
    st.subheader("Learn More About Caesar and AES Encryption")
    st.write("Choose a document to download and learn more about the encryption algorithms.")

    # List available documents
    documents = os.listdir("documents")
    document_name = st.selectbox("Select a document to download", documents)

    # Download document
    download_button = st.button("Download Document")

    if download_button:
        if document_name:
            user_name = st.session_state.get('user_name', 'guest')
            user_id = get_user_id_by_username(user_name)
            if check_permission(user_id, document_name, "download"):
                with open(f"documents/{document_name}", "rb") as f:
                    st.download_button(label="Download", data=f, file_name=document_name)
                log_activity(user_id, user_name, f"Downloaded document: {document_name}")
            else:
                st.error("You do not have permission to download this document.")
        else:
            st.error("Please select a document.")

# Call the function to render the encryption page
if __name__ == "__main__":
    encryption_show()