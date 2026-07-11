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


# User Interface (UI) Configurations & CSS
st.set_page_config(page_title="ExamMate | Sign Up", page_icon="📝", layout="centered")

# ==========================================
# UI/UX CSS INJECTION (LIGHT THEME)
# ==========================================
st.markdown(
    """
    <style>
    /* Global Theme (Pure White) */
    :root { color-scheme: light; }
    body, .stApp, .main .block-container { 
        background-color: #ffffff !important; 
        color: #333333 !important; 
    }
    .main .block-container { max-width: 450px; padding: 2rem 1rem; margin: 0 auto; }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select { 
        background-color: #ffffff !important; 
        border: 1px solid #d1d5db !important; 
        color: #000000 !important; 
        border-radius: 12px !important; 
        padding: 14px 16px !important; 
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border: 1px solid #10b981 !important;
        box-shadow: 0 0 5px rgba(16, 185, 129, 0.4) !important;
    }
    .stTextInput>label>div, .stSelectbox>label>div { 
        color: #333333 !important; 
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin-bottom: 4px;
    }
    
    /* Primary Buttons (Sign Up / Create Account - Solid Green) */
    .stButton button[kind="primary"] { 
        width: 100%; 
        background: #10b981 !important; 
        color: #ffffff !important; 
        border-radius: 25px !important; 
        padding: 0.75rem 1rem !important; 
        font-size: 1.1rem !important; 
        font-weight: 700 !important; 
        border: none !important; 
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2) !important;
    }
    .stButton button[kind="primary"]:hover { 
        background: #059669 !important;
        transform: translateY(-2px); 
        box-shadow: 0 6px 12px rgba(16, 185, 129, 0.3) !important; 
    }
    .stButton button[kind="primary"] p { color: #ffffff !important; margin: 0; font-weight: 700 !important; }

    /* Secondary Buttons (Default Light Gray/Outline for Cancel etc.) */
    .stButton button[kind="secondary"] { 
        width: 100%;
        background: #f8fafc !important; 
        color: #4b5563 !important; 
        border: 1px solid #cbd5e1 !important; 
        border-radius: 25px !important; 
        transition: all 0.3s ease;
    }
    .stButton button[kind="secondary"]:hover { 
        background: #f1f5f9 !important; 
        color: #1e293b !important;
        border: 1px solid #94a3b8 !important;
    }

    /* Routing Button (Sign In - Targetted Solid Blue) */
    .btn-sign-in + div button {
        background: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2) !important;
    }
    .btn-sign-in + div button:hover {
        background: #2563eb !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.3) !important;
    }
    .btn-sign-in + div button p { color: #ffffff !important; font-weight: 700 !important; margin: 0; }

    /* Titles */
    .custom-title { text-align: center; font-size: 2rem; font-weight: 800; margin-bottom: 0px; color: #000000; }
    .custom-subtitle { text-align: center; color: #4b5563; font-size: 1rem; margin-bottom: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# BACKEND LOGIC & RENDER
# ==========================================

# Render UI Content
if st.session_state.otp is None:
    st.markdown('<div class="custom-title">Sign Up</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">Create a new ExamMate account</div>', unsafe_allow_html=True)
    
    name = st.text_input("👤 Full Name")
    email = st.text_input("📧 Email Address")
    password = st.text_input("🔒 Password", type="password")
    
    catagory = st.selectbox("🎓 Role", ["Student", "Teacher"])

    if catagory == "Teacher":
        st.session_state.teachers = True
    else:
        st.session_state.students = True

    st.session_state.user_name = name
    st.session_state.user_catagory = catagory

    st.write("") # Spacer
    
    if st.button("Create Account", type="primary"):
        users = load_users()
        if email in users:
            st.error("An account has already been created with this email!")
        elif email and password and name:
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
            st.warning("Please fill in all required fields.")
            
    st.write("---")
    
    # CSS Marker injected to specifically style this button Blue
    st.markdown('<div class="btn-sign-in"></div>', unsafe_allow_html=True)
    if st.button("Already have an account? Sign In", type="secondary"):
        st.switch_page("pages/02_signin.py")

else:
    st.markdown('<div class="custom-title">Verification</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="custom-subtitle">OTP sent to {st.session_state.temp_user.get("email", "")}</div>', unsafe_allow_html=True)

    user_otp = st.text_input("🔢 Enter your 4-digit OTP:")

    if st.button("Verify & Register", type="primary"):
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

    if st.button("Cancel & Go Back", type="secondary"):
        st.session_state.otp = None
        st.session_state.temp_user = {}
        st.rerun()