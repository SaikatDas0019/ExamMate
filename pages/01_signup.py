import os
import random
import json
import sqlite3
import smtplib
import streamlit as st
from email.mime.text import MIMEText


# Data save korer jonno JSON file er name.
user_data_file = "users.json"
db_file = "ExamMate.db"


# .session_state
if "otp" not in st.session_state:
    st.session_state.otp = None
if "temp_user" not in st.session_state:
    st.session_state.temp_user = {}


def get_secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return os.getenv(name, default)


# JSON file theke purono user er data porer funtion.
def load_users():
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as f:
            return json.load(f)
    return {}


# JSON file e natun user er data save korer funtion.
def save_user(users_data):
    with open(user_data_file, "w") as f:
        json.dump(users_data, f, indent=4)


def save_user_to_sql(user_data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            category TEXT NOT NULL,
            gender TEXT
        )
    """)

    cursor.execute(
        "INSERT OR REPLACE INTO users (email, name, password, category) VALUES (?, ?, ?, ?)",
        (user_data["email"], user_data["name"], user_data["password"], user_data["catagory"])
    )
    conn.commit()
    conn.close()


def send_otp_email(receiver_email, otp_code):
    sender_email = get_secret("SMTP_EMAIL", "dasbabu938207@gmail.com")
    sender_password = get_secret("SMTP_PASSWORD", "vgyi zfoh prka lpkd")

    if not sender_email or not sender_password:
        st.info(f"SMTP credentials are not configured. For testing, use OTP: {otp_code}")
        return True

    msg = MIMEText(f"Your ExamMate verification code is: {otp_code}")
    msg["Subject"] = "ExamMate OTP Verification"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.warning(f"Email could not be sent automatically. For testing, use OTP: {otp_code}")
        return False


# User Interface (UI)
st.title("Email OTP Sign-Up System")

if st.session_state.otp is None:
    st.subheader("Create a new account.")
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your Email Address:")
    password = st.text_input("Enter a new password:", type="password")
    catagory = st.radio("Are you a", ["Student", "Teacher"])

    if catagory == "Teacher":
        st.session_state.teachers = True
    else:
        st.session_state.students = True

    st.session_state.user_name = name
    st.session_state.user_catagory = catagory

    if st.button("Send OTP", type="primary"):
        users = load_users()
        if email in users:
            st.error("An account has already been created with this email!")
        elif email and password:
            generated_otp = str(random.randint(1000, 9999))

            with st.spinner("Sending OTP..."):
                send_otp_email(email, generated_otp)

            st.session_state.otp = generated_otp
            st.session_state.temp_user = {
                "name": name,
                "email": email,
                "password": password,
                "catagory": catagory,
            }
            st.success("OTP has been sent to your email! Enter the OTP below.")
            st.rerun()
        else:
            st.warning("Please fill in both email and password.")
else:
    st.subheader("Email Verification")
    st.write(f"The OTP has been sent to: {st.session_state.temp_user.get('email', '')}")

    user_otp = st.text_input("Enter your 4 digit OTP:")

    if st.button("Sign Up", type="primary"):
        if user_otp == st.session_state.otp:
            users = load_users()
            users[st.session_state.temp_user["email"]] = st.session_state.temp_user
            save_user(users)
            save_user_to_sql(st.session_state.temp_user)
            st.balloons()
            st.session_state.logged_in = True
            st.session_state.is_logged_in = True
            st.session_state.students = True
            st.session_state.teachers = True
            st.session_state.user_email = st.session_state.temp_user["email"]
            st.session_state.user_name = st.session_state.temp_user["name"]
            st.session_state.user_catagory = st.session_state.temp_user["catagory"]
            st.session_state.otp = None
            st.session_state.temp_user = {}
            if st.session_state.user_catagory == "Student":
                st.switch_page("pages/03_student_dashboard.py")
            else:
                st.switch_page("pages/04_teacher_dashboard.py")
        else:
            st.error("Incorrect OTP! Please try again.")

if st.button("Resume / Cancel"):
    st.session_state.otp = None
    st.session_state.temp_user = {}
    st.rerun()