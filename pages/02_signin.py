import streamlit as st
import json
import os

# SignUp e je JSON file ti toiry hoyachilo
user_data_file = "users.json"

# .session_state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # surute user login abasta thakbe na.
if "user_email" not in st.session_state:
    st.session_state.user_email = ""    # login kora user er email store korar jonno.

# JSON file theke purono user er data porer funtion.
def load_users():
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as f:
            return json.load(f)
    return {}

# User Interface (UI)
if not st.session_state.logged_in:
    st.title("Gmail Login System")
    st.subheader("Login to your account.")

    # email and password input field
    email = st.text_input("Enter your Email Address:")
    password = st.text_input("Enter your Password:", type="password")
    forget_password = st.button("forget password", type="tertiary")

    # login button click korle
    if st.button("Login", type="primary"):
        users = load_users()
        if email in users and users[email].get("password") == password:
            st.session_state.logged_in = True
            st.session_state.is_logged_in = True
            st.session_state.user_email = email
            st.session_state.user_data = users[email]
            st.session_state.user_name = users[email]["name"]
            st.session_state.user_catagory = users[email]["catagory"]
            
            if st.session_state.user_catagory == "Student":
                st.switch_page("pages/03_student_dashboard.py")
            else:
                st.switch_page("pages/04_teacher_dashboard.py")

        else:
            st.error("Invalid email or password. Please try again.")