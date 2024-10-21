import streamlit as st

# Read the CSS file
with open("style.css") as f:
    css = f.read()

# Apply the custom style
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)




st.markdown('<div class="centered-text"><h1>Cipherly 🔐✨</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="centered-text"><h3>The encryption app that you need</h3></div>', unsafe_allow_html=True)
st.markdown('<div class="centered-text"><p>Are you ready to unlock the secrets of encryption? CipherPlay is your interactive playground where you can explore two exciting encryption techniques—Caesar Cipher and EAS Encryption. Whether you’re just curious about how data is protected or looking to experiment with encryption and decryption yourself, CipherPlay has you covered.\n With a simple and intuitive interface, you’ll be transforming ordinary text into cryptic codes in no time!</p></div>', unsafe_allow_html=True)
st.markdown('''
<div class="button-container">
    <button id="rectangle">
        <img src="/Users/macbookair/Documents/ISAMM/sem5/Sec BD/final-project/stickers/caesar.png" alt="Caesar Cipher">
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
        <img src=".stickers/security.png" alt="EAS Encryption">
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