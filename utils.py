import streamlit as st

# Function to navigate to a different page
def navigate_to(page):
    st.session_state.page = page
    print(f"Navigate to {page}")
    st.rerun()  # Force app to rerun and reflect the change immediately

# Function to clear cache and reset session state
def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    for key in st.session_state.keys():
        del st.session_state[key]
    navigate_to('home')