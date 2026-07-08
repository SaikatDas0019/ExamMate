import streamlit as st
# first e chack kore neoya je user asole login kore aseche kina.
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("teachers"):
    if st.session_state.user_catagory != "Teacher":
        st.error("**Access Denaid!** This page in only for Teachers.")
        st.stop()
    
    # user name and catagory
    user_name = st.session_state.get("user_name", "Teacher")
    user_catagory = st.session_state.get("user_catagory", "Teacher")

    # Dashboard

    col1, col2 = st.columns([5, 1])
    with col1:
        st.header(f"Hi, {user_name}")
    with col2:
        if st.button("👤"):
            st.switch_page("pages/06_teacher_profile.py")
    
    st.write("---")
    st.subheader("Exams")

    col3, col4 = st.columns([7, 1])
    with col3:
        search_exam = st.text_input("", placeholder="Search Exam")
    with col4:
        st.write("")
        st.write("")
        search_button = st.button("🔍")


    coustomize_exam = st.button("+ Coustomize Exam", use_container_width=True, type="primary")

    col5, col6, col7 =st.columns([1, 1, 1])
    with col5:
        jee_main = st.button("JEE Main", use_container_width=True)
        neet = st.button("NEET", use_container_width=True)
    with col6:
        wbjee = st.button("WBJEE", use_container_width=True)
        clas_11 = st.button("Class-11 Sem-1", use_container_width=True)
    with col7:
        jee_adv = st.button("JEE ADVANCE", use_container_width=True)
        clas_12 = st.button("Class-12 Sem-3", use_container_width=True)

    
else:
    st.warning("Please, sign-in first.")