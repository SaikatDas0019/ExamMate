import streamlit as st
import smtplib
import random
import json
import os
from email.mime.text import MIMEText


# Data save korer jonno JSON file er name.
user_data_file = "users.json"

# Gmail pathanor configaretion (Akhane apner data bosaben)
sender_email = "dasbabu938207@gmail.com"
# Google er deoya 16 digite er App Password
sender_password = "vgyi zfoh prka lpkd"

# .session_state
if "otp" not in st.session_state:
    st.session_state.otp = None
if "temp_user" not in st.session_state:
    st.session_state.temp_user = {}

# JSON file theke purono user er data porer funtion.
def load_users():
    if os.path.exists(user_data_file):
        with open(user_data_file, "r")as f:
            return json.load(f)
    return {}

# JSON file e natun user er data save korer funtion.
def save_user(users_data):
    with open(user_data_file, "w") as f:
        json.dump(users_data, f, indent=4)

# Email e OTP pathanor Funtion
def send_otp_email(receiver_email, otp_code):
    msg = MIMEText(f"Your Streamlit app verification OTP code is: {otp_code}")
    msg["Subject"] = "Streamlit App OTP Verification"
    msg['From'] = sender_email
    msg["To"] = receiver_email

    try:
        # Gmail er Secure server er sathe connect kora.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"There was a problem sending the email: {e}")
        return False

# User Interface (UI)
st.title("Gmail OTP Sign-Up System")

# jodi OTP akhono pathano na hoya thake (First Step: Email and Password input)
if st.session_state.otp is None:
    st.subheader("Create a new account.")
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your Email Address:")
    password = st.text_input("Enter a new password:", type='password')
    catagory = st.radio("Are you a", ["Student", "Teacher"])

    if catagory == "Teacher":
        st.session_state.teachers = True
    else:
        st.session_state.students = True

    st.session_state.user_name = name
    st.session_state.user_catagory = catagory

    if st.button("Send OTP", type='primary'):
        users = load_users()
        if email in users:
            st.error("An account has already been created with this email!")
        elif email and password:
            # 4 digite er OTP toyri.
            generated_otp = str(random.randint(1000, 9999))

            # email e pathano
            with st.spinner("Sending OTP..."):
                if send_otp_email(email, generated_otp):
                    # .session_state e OTP & user data samoyik vabe save kora.
                    st.session_state.otp = generated_otp
                    st.session_state.temp_user = {
                        "name": name,
                        "email": email,
                        "password": password,
                        "catagory": catagory,
                    }
                    st.success("OTP has been sent to your email! Enter the OTP in the box below.")
                    st.rerun()
        else:
            st.warning("Please fill in both email and password.")

# jodi OTP already chole jai(Second Step: OTP Verification.)
else:
    st.subheader("Email Verification")
    st.write(f"The OTP has been sent here: {st.session_state.temp_user['email']}")

    user_otp = st.text_input("Enter your 4 digite OTP:")

    if st.button("Sign Up", type='primary'):
        if user_otp == st.session_state.otp:
            users = load_users()
            users[st.session_state.temp_user["email"]] = st.session_state.temp_user
            save_user(users)
            st.balloons()
            st.session_state.logged_in = True
            st.session_state.is_logged_in = True
            st.session_state.students = True
            st.session_state.teachers = True
            # .session_state reset kora.
            st.session_state.otp = None
            st.session_state.temp_user = {}
        else:
            st.error("Incorrect OTP! Please try again.")

if st.button("Resume / Cancel"):
    st.session_state.otp = None
    st.session_state.temp_user = {}
    st.rerun()