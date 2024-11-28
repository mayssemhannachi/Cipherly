import streamlit as st


st.set_page_config(page_title="Cipherly", page_icon="🔐", layout="wide", initial_sidebar_state="collapsed", menu_items=None)

# Read the CSS file
with open("style.css") as f:
    css = f.read()

# Apply the custom style
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Sidebar for user role selection
st.sidebar.title("Who are you?")
user_role = st.sidebar.radio("Who are you?", ("Regular User", "Admin"), index=0)

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Function to navigate to a different page
def navigate_to(page):
    st.session_state.page = page
    print(f"Navigate to {page}")
    st.rerun()  # Force app to rerun and reflect the change immediately

# Render the current page
if st.session_state.page == "home":

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
    col1, col2,col3,col4 = st.columns([2, 1,1,2])

    # Add Python-based navigation for "Sign Up"
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

        if st.button('Caesar Cipher'):
            navigate_to('caesar_cipher')


    with col6:
        st.markdown('''
            <div class="button-container" style="position: relative; top: -80px; left: 50px;">
                <a href="?page=eas_encryption" style="text-decoration: none;">
                    <button id="rectangle">
                        <img src="https://raw.githubusercontent.com/mayssemhannachi/Cipherly/master/stickers/security.png" alt="EAS Encryption" style="width: 100px; height: 100px;">        
                        EAS Encryption 
                        <br>
                        Enter the world of modern encryption 
                        with EAS (Enhanced Algorithmic 
                        Security) Encryption. This technique 
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

# Handle navigation based on session state
if st.session_state.page == "caesar_cipher":
    # Import Caesar Cipher Page
    import caesar_cipher
elif st.session_state.page == "eas_encryption":
    # Import EAS Encryption Page
    import eas_encryption
elif st.session_state.page == "sign_up":
    # Import Sign Up Page
    import sign_up
    sign_up.show_sign_up_page()
elif st.session_state.page == "log_in":
    # Import Log In Page
    import log_in
    log_in.show_log_in_page()

