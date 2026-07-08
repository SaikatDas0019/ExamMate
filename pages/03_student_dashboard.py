import streamlit as st

# first e chack kore neoya je user asole login kore aseche kina.
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.user_catagory != "Student":
        st.error("**Access Denaid!** This page in only for Students.")
        st.stop()
    # user name and catagory
    user_name = st.session_state.get("user_name", "Student")
    user_catagory = st.session_state.get("user_catagory", "Student")

    # Dashboard

    col1, col2 = st.columns([5, 1])
    with col1:
        st.header(f"Hi, {user_name}")
        col01, col02= st.columns([1, 1])
        with col01:
            st.write(f"**Score:** 01")
            st.write(f"**Total Exam:** 00")
        with col02:
            st.write(f"**Highest Marks:** 00")
            st.write(f"**Lowest Marks**: 00")
    with col2:
        if st.button("👤"):
            st.switch_page("pages/05_student_profile.py")

    st.divider()
    st.header("Exams")

    col_1, col_2 = st.columns([4, 1])
    with col_1:
        customize = st.text_input(f"**Teacher's Exam Code:**", placeholder="e.g: PHY-101")
    with col_2:
        st.write("")
        st.write("")
        search_exam = st.button("🔍")

    col3, col4, col5 = st.columns(3)

    with col3:
        jee_main = st.button("JEE Main", type="primary", use_container_width=True)
        neet = st.button("NEET", type="primary", use_container_width=True)
    with col4:
        wbjee = st.button("WBJEE", type="primary", use_container_width=True)
        clas_11 = st.button("Class-11 Sem-1", type="primary", use_container_width=True)
    with col5:
        jee_adv = st.button("JEE ADVANCE", type="primary", use_container_width=True)
        clas_12 = st.button("Class-12 Sem-3", type="primary", use_container_width=True)
    
else:
    st.warning("Please, sign-in first.")