import streamlit as st
# Clear cache programmatically
st.cache_data.clear()  # Clear data cache
st.cache_resource.clear()  # Clear resource cache (if using st.cache_resource)
st.title("AES Encryption Page")

# AES Encryption page content
st.write("This is the AES Encryption page. Add your encryption logic here.")

# Back to Home button
if st.button("Back to Home 🏠"):
    st.session_state.page = "home"
    st.rerun()  # Rerun the app to navigate to home