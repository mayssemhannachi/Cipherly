import streamlit as st

# Function to navigate to a different page
def navigate_to(page):
    st.session_state.page = page
    print(f"Navigate to {page}")
    st.rerun()  # Force app to rerun and reflect the change immediately

# Clear cache programmatically
st.cache_data.clear()  # Clear data cache
st.cache_resource.clear()  # Clear resource cache (if using st.cache_resource)

st.title("Caesar Cipher Page")

# Caesar Cipher page content
st.write("This is the Caesar Cipher page. Add your encryption logic here.")

# Back to Home button
if st.button("Back to Home 🏠"):
    navigate_to('main')  # Navigate to the home page
