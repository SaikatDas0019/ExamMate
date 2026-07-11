import os
import json
import sqlite3
import streamlit as st

# SignUp e je JSON file ti toiry hoyachilo
user_data_file = "users.json"
db_file = "ExamMate.db"

# .session_state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# SQLite theke user er data load korar funtion.
def load_users_from_sql():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT email, name, password, category FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = {}
    for row in rows:
        users[row["email"]] = {
            "name": row["name"],
            "email": row["email"],
            "password": row["password"],
            "catagory": row["category"],
        }
    return users

# JSON file theke purono user er data porer funtion.
def load_users():
    sql_users = load_users_from_sql()
    if sql_users:
        return sql_users

    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as f:
            return json.load(f)
    return {}

# JSON file theke specific user er data delete korar funtion.
def delete_user(email):
    users = load_users()
    if email in users:
        del users[email]
        with open(user_data_file, "w") as f:
            json.dump(users, f, indent=4)

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        return True
    return False


# User Interface (UI) Configurations & CSS
st.set_page_config(page_title="ExamMate | Sign In", page_icon="📝", layout="centered")

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
        border: 1px solid #3b82f6 !important;
        box-shadow: 0 0 5px rgba(59, 130, 246, 0.4) !important;
    }
    .stTextInput>label>div, .stSelectbox>label>div { 
        color: #333333 !important; 
        font-size: 0.95rem !important; 
        font-weight: 600 !important; 
        margin-bottom: 4px;
    }
    
    /* Primary Buttons (Sign In - Solid Blue) */
    .stButton button[kind="primary"] { 
        width: 100%; 
        background: #3b82f6 !important; 
        color: #ffffff !important; 
        border-radius: 25px !important; 
        padding: 0.75rem 1rem !important; 
        font-size: 1.1rem !important; 
        font-weight: 700 !important; 
        border: none !important; 
        transition: all 0.3s ease; 
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2) !important;
    }
    .stButton button[kind="primary"]:hover { 
        background: #2563eb !important;
        transform: translateY(-2px); 
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.3) !important; 
    }
    .stButton button[kind="primary"] p { color: #ffffff !important; margin: 0; font-weight: 700 !important; }

    /* Secondary Buttons (Forget Password - Default Light Gray) */
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

    /* Create Account Button (Targeted via marker - Solid Green) */
    .btn-create-account + div button {
        background: #10b981 !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2) !important;
    }
    .btn-create-account + div button:hover {
        background: #059669 !important;
        transform: translateY(-2px);
    }
    .btn-create-account + div button p { color: #ffffff !important; font-weight: 700 !important; margin: 0; }

    /* Titles */
    .custom-title { text-align: center; font-size: 2rem; font-weight: 800; margin-bottom: 0px; color: #000000; }
    .custom-subtitle { text-align: center; color: #4b5563; font-size: 1rem; margin-bottom: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="custom-title">Sign In</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subtitle">Welcome back to ExamMate</div>', unsafe_allow_html=True)

email = st.text_input("📧 Username / Email")
password = st.text_input("🔒 Password", type="password")

st.write("") # Spacer

if st.button("Sign In", type="primary"):
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

col1, col2 = st.columns(2)
with col1:
    if st.button("Forget Password?", type="secondary", key="forget_password"):
        if email:
            deleted = delete_user(email)
            if deleted:
                st.success("Email-er data delete hoye geche. Ekhon abar signup korte parben.")
            else:
                st.warning("Ei email-er kono user data paoa jay ni.")

            st.switch_page("pages/01_signup.py")
        else:
            st.warning("Prothome apnar email likhun.")
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.user_name = ""
        st.session_state.user_catagory = ""
        st.stop()

with col2:
    # Marker injected to allow CSS to specifically style this button Green
    st.markdown('<div class="btn-create-account"></div>', unsafe_allow_html=True)
    if st.button("Create Account", type="secondary"):
        st.switch_page("pages/01_signup.py")