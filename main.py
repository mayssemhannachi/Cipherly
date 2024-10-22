import streamlit as st

st.set_page_config(page_title="Cipherly" , page_icon="🔐", layout="wide", initial_sidebar_state="collapsed", menu_items=None)


# Read the CSS file
with open("style.css") as f:
    css = f.read()

# Apply the custom style
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.markdown(
    '<div style="position: relative; top: 10px; left: 50px;">'
    '<img src="https://raw.githubusercontent.com/mayssemhannachi/Cipherly/master/stickers/arrow.png" alt="Expand Sidebar" style="width: 200px; height: 200px;transform: scaleX(-1);">'
    '</div>',
    unsafe_allow_html=True
)

# Sidebar for user role selection
st.sidebar.title("Who are you?")
user_role = st.sidebar.radio("Who are you?", ("Regular User", "Admin"), index=0)


st.markdown('<div class="centered-text" style="position: relative; top: -180px; left: 50px;"><h1>Cipherly 🔐✨</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="centered-text" style="position: relative; top: -140px; left: 50px;"><h3>The encryption app that you need</h3></div>', unsafe_allow_html=True)
st.markdown('<div class="centered-text" style="position: relative; top: -100px; left: 50px;"><p>Are you ready to unlock the secrets of encryption? Cipherly is your interactive playground where you can explore two exciting encryption techniques—Caesar Cipher and EAS Encryption. Whether you’re just curious about how data is protected or looking to experiment with encryption and decryption yourself, CipherPlay has you covered.\n With a simple and intuitive interface, you’ll be transforming ordinary text into cryptic codes in no time!</p></div>', unsafe_allow_html=True)
st.markdown('''
<div class="button-container"style="position: relative; top: -50px; left: 50px;">
    <button id="rectangle">
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
</div>
''', unsafe_allow_html=True)