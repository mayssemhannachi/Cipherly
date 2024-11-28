import streamlit as st
import re
from captcha.image import ImageCaptcha

# Clear cache programmatically
st.cache_data.clear()  # Clear data cache
st.cache_resource.clear()  # Clear resource cache (if using st.cache_resource)

# Form definition

def show_log_in_page():
    st.markdown('<div class="centered-text" style="position: relative; top: 0px; left: 50px;"><h1>Log in</h1></div>', unsafe_allow_html=True)
