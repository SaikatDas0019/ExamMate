import streamlit as st

st.set_page_config(page_title='ExamMate', page_icon="📝", layout="centered")

st.image("images/App_Logo_3.jpeg")
st.subheader("ExamMate | Best app for MCQ practice of any exam.")

st.write("---")

st.header("✅ Sign-Up or Sign-In")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Sing Up", use_container_width=True):
        st.switch_page("pages/01_signup.py")
with col2:
    if st.button("Sign In", use_container_width=True):
        st.switch_page("pages/02_signin.py")

st.write("---")
st.header("🟢 Feature:")

col3, col4 = st.columns([1, 1])

with col3:
    st.success("**Time Management:** Testing with timers like the real thing.")
    st.success("**Coustomize Exam:** Teachers have the freedom th set questions like their own.")
with col4:
    st.success("**Perfect Prep:** Unlimited MCQ Prectice.")
    st.success("**Instant Result:** Opportunity to khow the correct answer and score as soon as the test is over.")
