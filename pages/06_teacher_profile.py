import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import base64
import os

# first e chack kore neoya je user asole login kore aseche kina.
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.user_catagory != "Teacher":
        st.error("**Access Denaid!** This page in only for Teachers.")
        st.stop()
    import streamlit as st

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


    st.divider()
    st.subheader("Your Exams & Results Analysis")
    
    # Database connection
    conn = sqlite3.connect('ExamMate.db')
    cursor = conn.cursor()
    
    # session_state theke teacher er email ber kora
    teacher_email = st.session_state.get('user_email', 'teacher@email.com')
    
    # SQL query to fetch exams created by the logged-in teacher
    cursor.execute("SELECT exam_code, exam_name FROM exams WHERE teacher_email = ?", (teacher_email,))
    exams_created = cursor.fetchall()
    
    if exams_created:
        # Exams er naam o code ke dictionary te convert kora jate dropdown e dekhano jay
        exam_options = {f"{exam[1]} ({exam[0]})": exam[0] for exam in exams_created}
        
        # Teacher ke dropdown deya jate kon exam er analysis dekhte chai ta select korte pare
        selected_exam_name = st.selectbox("Which exam's detailed analysis would you like to see?", list(exam_options.keys()))
        selected_exam_code = exam_options[selected_exam_name]
        
        if selected_exam_code:
            st.write(f"### 📈 {selected_exam_name} - detailed report")
            
            # SQL query to fetch results for the selected exam
            query = """
                SELECT users.name, results.score, results.total_questions 
                FROM results 
                JOIN users ON results.student_email = users.email 
                WHERE results.exam_code = ?
            """
            # Pandas er read_sql_query diye query run kora
            df_results = pd.read_sql_query(query, conn, params=(selected_exam_code,))
            
            if not df_results.empty:
                # Pandas DataFrame theke total students, average score, and total questions ber kora
                total_students = len(df_results)
                avg_score = df_results['score'].mean()
                total_qs = df_results['total_questions'].iloc[0] # total_questions column er first value neya, karon sob row te same thakbe
                
                # Screen e metrics dekhano
                st.write("### 📊 Exam Summary Metrics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Students", f"{total_students} জন")
                with col2:
                    st.metric("Average Score", f"{avg_score:.2f} / {total_qs}")
                with col3:
                    st.metric("Total Questions in Exam", f"{total_qs} টি")
                    
                st.divider()
                
                # performance percentage ber kora
                df_results['Performance (%)'] = round((df_results['score'] / df_results['total_questions']) * 100, 2)
                
                # Top 10 & Bottom 10
                col_top, col_bottom = st.columns(2)
                
                with col_top:
                    st.success("🏆 **Top 10 Students**")
                    # nlargest diye sobcheye beshi score paoya ১০ jon ke ber kora
                    top_10 = df_results.nlargest(10, 'score')[['name', 'score', 'Performance (%)']]
                    top_10.columns = ["Student Name", "Score", "Performance (%)"]
                    st.dataframe(top_10, use_container_width=True, hide_index=True)
                    
                with col_bottom:
                    st.error("📉 **Bottom 10 Students**")
                    # nsmallest diye sobcheye kom score paoya ১০ jon ke ber kora
                    bottom_10 = df_results.nsmallest(10, 'score')[['name', 'score', 'Performance (%)']]
                    bottom_10.columns = ["Student Name", "Score", "Performance (%)"]
                    st.dataframe(bottom_10, use_container_width=True, hide_index=True)
                    
                st.divider()
                
                # Matplotlib diye histogram (Score Distribution Graph) toyri kora
                st.write("### 📊 Score Distribution Graph")
                st.write("📊 **Number Distribution (Score Distribution Graph)**")
                st.write("*(This graph shows the distribution of scores among students)*")
                
                fig, ax = plt.subplots(figsize=(7, 3.5))
                # Histogram plot kora, bins er range 0 theke total_questions+1, color, edgecolor, alignment and width set kora
                ax.hist(df_results['score'], bins=range(0, int(total_qs)+2), color='#4CAF50', edgecolor='black', align='left', rwidth=0.8)
                ax.set_xlabel('Received Scores')
                ax.set_ylabel('Number of Students')
                ax.set_title('Exam Score Distribution Graph')
                ax.set_xticks(range(0, int(total_qs)+1))
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                
                st.pyplot(fig) # streamlit e matplotlib graph dekhano
                
                st.divider()
                
                # samanno student der list dekhano
                st.write("📋 **List off all the students who have taken this exam:**")
                full_list = df_results[['name', 'score', 'total_questions', 'Performance (%)']].sort_values(by="score", ascending=False)
                full_list.columns = ["Student Name", "Score", "Total Questions", "Performance (%)"]
                st.dataframe(full_list, use_container_width=True, hide_index=True)
                
            else:
                st.info("ℹ️ No students have taken this exam yet. Once students take the exam, their results will appear here.")
    else:
        st.info("ℹ️ You haven't created any exams yet. Once you create exams, you will be able to see the results and analysis here.")
    
    conn.close()
    
else:
    st.warning("Please, sign-in first.")