import streamlit as st
import sqlite3

# Verify authentication
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.get("user_catagory") != "Student":
        st.error("**Access Denied!** This page is only for Students.")
        st.stop()

    st.title("Exam")

    # .session_state Memory Initialize
    if "exam_started" not in st.session_state:
        st.session_state.exam_started = False
    if "current_q_index" not in st.session_state:
        st.session_state.current_q_index = 0
    if "student_answers" not in st.session_state:
        st.session_state.student_answers = {}
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "exam_info" not in st.session_state:
        st.session_state.exam_info = None

    # Auto-Start Logic
    if not st.session_state.exam_started:
        exam_code = st.session_state.get("exam_code", "").strip()

        if exam_code:
            conn = sqlite3.connect("ExamMate.db")
            cursor = conn.cursor()

            # Check if exam exists in DB
            cursor.execute("SELECT exam_name, timer_minutes FROM exams WHERE exam_code = ?", (exam_code,))
            exam_data = cursor.fetchone()  

            if exam_data:
                exam_name = exam_data[0]
                timer = exam_data[1]

                # Fetch all questions for this exam
                cursor.execute("SELECT id, question_text, option_a, option_b, option_c, option_d, correct_option FROM questions WHERE exam_code = ?", (exam_code,))
                questions = cursor.fetchall()  

                if questions:
                    # Exam and questions found -> AUTOMATICALLY START EXAM
                    st.session_state.questions = questions
                    st.session_state.exam_info = (exam_name, timer)
                    st.session_state.exam_started = True
                    st.session_state.current_q_index = 0
                    st.session_state.student_answers = {}
                    st.rerun() # Silent rerun to jump straight into the exam interface
                else:
                    st.error(f"Test found ({exam_name}), but no questions were attached to it in the database.")
                    if st.button("Return to Dashboard 🏠"):
                        st.switch_page("pages/03_student_dashboard.py")
            else:
                st.error(f"Invalid Code: No exam with the code '{exam_code}' was found in the database.")
                if st.button("Return to Dashboard 🏠"):
                    st.switch_page("pages/03_student_dashboard.py")

            conn.close()
        else:
            # Fallback if someone manually navigates to the URL without clicking an exam button
            st.warning("No exam selected.")
            if st.button("Return to Dashboard 🏠"):
                st.switch_page("pages/03_student_dashboard.py")

    # Live exam interface
    else:
        exam_name, timer_minutes = st.session_state.exam_info
        questions = st.session_state.questions
        total_questions = len(questions)
        current_index = st.session_state.current_q_index

        # Display Exam Name and Time
        st.subheader(f"Exam: {exam_name}")
        st.write(f"Time: {timer_minutes} min")

        # Progress bar
        progress_val = (current_index + 1) / total_questions
        st.progress(progress_val)
        st.write(f"**Question No.: {current_index + 1} / {total_questions}**")

        st.divider()

        # Separate current question data
        q_id, q_text, opt_a, opt_b, opt_c, opt_d, correct_opt = questions[current_index]

        # Display Question
        st.markdown(f"### Q: {q_text}")

        # Format 4 options
        option_list = [f"A. {opt_a}", f"B. {opt_b}", f"C. {opt_c}", f"D. {opt_d}"]
        option_map = {"A": 0, "B": 1, "C": 2, "D": 3}
        reverse_map = {0: "A", 1: "B", 2: "C", 3: "D"}

        # Maintain selected state
        previously_saved_ans = st.session_state.student_answers.get(current_index, None)
        default_selection = option_map[previously_saved_ans] if previously_saved_ans in option_map else 0

        # Radio button selection
        user_choice = st.radio("Choose the correct option:",
                               option_list,
                               index=default_selection,
                               key=f"q_radio_{current_index}"
                               )

        # Save student choice to memory
        selected_letter = reverse_map[option_list.index(user_choice)]
        st.session_state.student_answers[current_index] = selected_letter

        st.divider()

        # --- Navigation (Previous, Next, Submit) ---
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("⬅️ Previous", disabled=(current_index == 0), use_container_width=True):
                st.session_state.current_q_index -= 1
                st.rerun()

        with col2:
            if st.button("Next ➡️", disabled=(current_index == total_questions - 1), use_container_width=True):
                st.session_state.current_q_index += 1
                st.rerun()

        with col3:
            if st.button("Submit Exam 🚀", type="primary", use_container_width=True):
                st.session_state.exam_started = "completed" 
                st.rerun()


    # Post-Exam Score View
    if st.session_state.exam_started == "completed":
        st.balloons()
        st.title("Exam Completed!")

        questions = st.session_state.questions
        total_questions = len(questions)

        # Calculate Score
        score = 0
        for idx, q in enumerate(questions):
            real_correct_answer = q[6] # Correct answer index from DB
            student_given_answer = st.session_state.student_answers.get(idx, None)

            if student_given_answer == real_correct_answer:
                score += 1

        st.metric(label="Your Score", value=f"{score} / {total_questions}")
        st.success("Your answers have been submitted successfully. The teacher will be able to view them.")

        # --- Save Results to Database ---
        if "result_saved" not in st.session_state:
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
            exam_code = st.session_state.get('exam_code', '')

            cursor.execute('''
                INSERT INTO results (student_email, exam_code, exam_name, score, total_questions) 
                VALUES (?, ?, ?, ?, ?)
            ''', (student_email, exam_code, exam_name, score, total_questions))

            conn.commit()
            conn.close()
            st.session_state.result_saved = True


        # Return to Dashboard Button
        if st.button("Return to Dashboard 🏠"):
            st.session_state.exam_started = False
            st.session_state.current_q_index = 0
            st.session_state.student_answers = {}
            # Optional: reset dash view to categories when returning
            st.session_state.dash_flow_step = "categories"
            st.switch_page("pages/03_student_dashboard.py")

else:
    st.warning("Please, sign-in first.")
    if st.button("⬅️ Sign In page"):
        st.switch_page("pages/02_signin.py")