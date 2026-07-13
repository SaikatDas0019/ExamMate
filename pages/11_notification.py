import streamlit as st

if st.session_state.get("logged_in") or st.session_state.get("is_logged_in"):

    if st.session_state.get("user_catagory") == "Student":
        if st.button("⬅️ Back to Home"):
            st.switch_page("pages/03_student_dashboard.py")
    elif st.session_state.get("user_catagory") == "Teacher":
        if st.button("⬅️ Back to Home"):
            st.switch_page("pages/04_teacher_dashboard.py")

    st.title("Notification")

else:
    st.warning("Please, sign-in first.")
    if st.button("⬅️Sign In page"):
        st.switch_page("pages/02_signin.py")