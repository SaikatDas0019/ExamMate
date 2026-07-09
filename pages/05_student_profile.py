import sqlite3

import streamlit as st
import base64
import os
import streamlit as st

# first e chack kore neoya je user asole login kore aseche kina.
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.user_catagory != "Student":
        st.error("**Access Denaid!** This page in only for Students.")
        st.stop()

    # Page Title
    st.title("Profile")

    # 1. Photo gol kore dekhanor jonno html er akti function.
    def get_circular_image(image_data, is_path=False):
        if is_path:
            with open(image_data, "rb") as f:
                image_bytes = f.read()
        else:
            image_bytes = image_data

        encoded_img = base64.b64encode(image_bytes).decode()

        html_code = f'''
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{encoded_img}" 
                     style="width: 180px; height: 180px; border-radius: 50%; object-fit: cover; border: 3px solid #4CAF50;">
            </div>
        '''
        st.markdown(html_code, unsafe_allow_html=True)

    # 2. .session_state e photo save korer babosta
    if "profile_pic" not in st.session_state:
        st.session_state.profile_pic = None

    # 3. Photo uploade korar option
    if st.session_state.profile_pic is None:
        default_profile_pic = "images\default_profile_pic.jpg"
        if os.path.exists(default_profile_pic):
            get_circular_image(default_profile_pic, is_path=True)
        col, col1, col = st.columns([2, 1, 2])
        with col1:
            uploaded_file = st.file_uploader("Upload your Profile Picture (JPG/PNG)", type=["png", "jpg", "jpeg"])

        if uploaded_file is not None:
            # Upload kora photo session_state e save kora
            st.session_state.profile_pic = uploaded_file.getvalue()
            st.rerun()

    # 4. Photo dekhano
    else:
        get_circular_image(st.session_state.profile_pic, is_path=False)

        col, col2, col = st.columns([4, 2, 4])
        with col2:
            if st.button("Edit", use_container_width=True):
                st.session_state.profile_pic = None
                st.rerun()

    # User data
    st.write(f"**Name:** {st.session_state.get('user_name', 'Student')}")
    st.write(f"**Email:** {st.session_state.get('user_email', 'student@email.com')}")

    st.write("---")
    st.subheader("My Favourite Teachers")

    col01, col02, col03 = st.columns([1, 1, 1])
    with col01:
        teacher_1 = st.button("Tarapada Sir", use_container_width=True)
        teacher_2 = st.button("Amit Sir", use_container_width=True)
    with col02:
        teacher_3 = st.button("Prokash Sir", use_container_width=True)
        teacher_4 = st.button("Manash Sir", use_container_width=True)
    with col03:
        teacher_5 = st.button("Somnath Sir", use_container_width=True)
        teacher_6 = st.button("Mithun Sir", use_container_width=True)

    st.write("---")
    st.subheader("Exam History")
    
    conn = sqlite3.connect('ExamMate.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT NOT NULL,
            exam_code TEXT NOT NULL,
            exam_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    student_email = st.session_state.get('user_email', 'student@email.com')
    
    # Oi student er result gula ber kora
    cursor.execute("SELECT exam_name, score, total_questions, date_taken FROM results WHERE student_email = ? ORDER BY date_taken DESC", (student_email,))
    results_data = cursor.fetchall()
    
    if results_data:
        import pandas as pd
        
        # DataFrame toyri kora, column name gula Bangla te deya
        df = pd.DataFrame(results_data, columns=["Exam Name", "Score", "Total Questions", "Date Taken"])
        
        # Number ke persentage e dekhano
        df["Performance (%)"] = round((df["Score"] / df["Total Questions"]) * 100, 2)
        
        # streamlit e dataframe dekhano, index hide kora, container width use kora
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No exam history found. Please take some exams to see your results here.")
    
    conn.close()
else:
    st.warning("Please, sign-in first.")