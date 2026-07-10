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


# User Interface (UI)
if not st.session_state.logged_in:
    st.title("Email Login System")
    st.subheader("Login to your account.")

    email = st.text_input("Enter your Email Address:")
    password = st.text_input("Enter your Password:", type="password")

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

    if st.button("forget password", type="tertiary", key="forget_password"):
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