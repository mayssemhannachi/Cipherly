import sqlite3
from datetime import datetime
import streamlit as st
import requests
from streamlit_javascript import st_javascript


# Function to capture IP address and User Agent

def get_client_details():
    # Get user agent using JavaScript
    user_agent = st_javascript("navigator.userAgent") or "Unknown Agent"
    print (user_agent)

    # Get IP address using an external API
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        ip_address = response.json().get("ip", "Unknown IP")
    except:
        ip_address = "Unknown IP"
    print(ip_address)

    return ip_address, user_agent
# Function to handle guest actions
def handle_guest_action():
    # Get guest details
    ip_address, user_agent = get_client_details()

    # Add guest to the database
    add_guest_to_database(ip_address, user_agent)


# Function to add a guest to the database
def add_guest_to_database(ip_address, user_agent):
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Guest details
    guest_role = "Guest"
    is_active = True
    visit_time = datetime.now()

    # Insert guest into the database
    cursor.execute('''
        INSERT INTO users (role, is_active, ip_address, user_agent, visit_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (guest_role, is_active, ip_address, user_agent, visit_time))

    # Commit and close
    conn.commit()
    conn.close()
