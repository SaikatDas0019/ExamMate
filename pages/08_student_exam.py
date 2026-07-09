import streamlit as st
import sqlite3


# first e chack kore neoya je user asole login kore aseche kina.
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.user_catagory != "Student":
        st.error("**Access Denaid!** This page in only for Students.")
        st.stop()

    st.title("Exam")

    # .session_state Memori inisialise kora.
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


    if not st.session_state.exam_started:
        exam_code = st.session_state.get("exam_code", "").strip()

        if exam_code:
            conn = sqlite3.connect("ExamMate.db")
            cursor = conn.cursor()

            # exams table e check kora je oi code er kono exam ache ki na.
            cursor.execute("SELECT exam_name, timer_minutes FROM exams WHERE exam_code = ?", (exam_code,))
            exam_date = cursor.fetchone()  # .fetchone() mane akta result tule ana.

            if exam_date:
                # Exam pauya gele tar name ar time variable e rakha 
                exam_name = exam_date[0]
                timer = exam_date[1]

                st.success(f"The test found: {exam_name}")
                st.info(f"Time: {timer} min")

                # eber 'questions' table theke all question tule ana.
                cursor.execute("SELECT id, question_text, option_a, option_b, option_c, option_d, correct_option FROM questions WHERE exam_code = ?", (exam_code,))
                questions = cursor.fetchall()  # .fetchall() mane sob question aksonge tile ana.

                st.write(f"Total questions: {len(questions)}")

                if questions:
                    st.session_state.questions = questions
                    st.session_state.exam_info = (exam_name, timer)
                    st.session_state.exam_started = True
                    st.session_state.current_q_index = 0
                    st.session_state.student_answers = {}
                    st.rerun()
                else:
                    st.error("No questions were found in this test.")

            else:
                st.error("Wrong code! No tests of this code were found in the database.")

            conn.close()
        else:
            st.warning("Please enter a code first.")

    # Live exam interface
    else:
        exam_name, timer_minutes = st.session_state.exam_info
        questions = st.session_state.questions
        total_questions = len(questions)
        current_index = st.session_state.current_q_index

        # Exam er name and time dekhano.
        st.subheader(f"Exam: {exam_name}")
        st.write(f"Time: {timer_minutes} min")

        # Progress ber
        progress_val = (current_index + 1) / total_questions
        st.progress(progress_val)
        st.write(f"**Question No.: {current_index + 1} / {total_questions}**")

        st.divider()

        # bartaman question er data alada kora
        q_id, q_text, opt_a, opt_b, opt_c, opt_d, correct_opt = questions[current_index]

        # Screen e question dekhano
        st.markdown(f"###Q: {q_text}")

        # 4 ti option sajano
        option_list = [f"A. {opt_a}", f"B. {opt_b}", f"C. {opt_c}", f"D. {opt_d}"]
        option_map = {"A": 0, "B": 1, "C": 2, "D": 3}
        reverse_map = {0: "A", 1: "B", 2: "C", 3: "D"}

        # Jodi student age ai question er answer diya thake , tobe seti selected thakbe (edit korer jonno)
        previously_saved_ans = st.session_state.student_answers.get(current_index, None)
        default_selection = option_map[previously_saved_ans] if previously_saved_ans in option_map else 0

        # radio button
        user_choice = st.radio("Choose the correct option:",
                               option_list,
                               index=default_selection,
                               key=f"q_radio_{current_index}"
                               )

        # Student ja select korbe ta memorite save kora.
        selected_letter = reverse_map[option_list.index(user_choice)]
        st.session_state.student_answers[current_index] = selected_letter

        st.divider()

        # --- Navigation (Previous, Next, Submit) ---
        col1, col2, col3 = st.columns(3)

        with col1:
            # 1st question e thakle 'Previous' batan ta disable thakbe
            if st.button("⬅️ Previous", disabled=(current_index == 0), use_container_width=True):
                st.session_state.current_q_index -= 1
                st.rerun()

        with col2:
            # question er last e thakle 'Next' batan ta disable thakbe
            if st.button("Next ➡️", disabled=(current_index == total_questions - 1), use_container_width=True):
                st.session_state.current_q_index += 1
                st.rerun()

        with col3:
            # final question e thakle 'Submit' batan ta dekhabe
            if st.button("Submit Exam 🚀", type="primary", use_container_width=True):
                st.session_state.exam_started = "completed" # Exa er status complete kora
                st.rerun()


    # Exam complete hole student ke score dekhano
    if st.session_state.exam_started == "completed":
        st.balloons()
        st.title("Exam Completed!")

        questions = st.session_state.questions
        total_questions = len(questions)

        # Score calculate kora
        score = 0
        for idx, q in enumerate(questions):
            real_correct_answer = q[6] # Database e correct answer (A/B/C/D)
            student_given_answer = st.session_state.student_answers.get(idx, None)

            if student_given_answer == real_correct_answer:
                score += 1

        st.metric(label="Your Score", value=f"{score} / {total_questions}")
        st.success("Your answers have been submitted successfully. The teacher will be able to view them.")

        # ---Save Results database e save---
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

            student_email = st.session_state.get('user_email', 'student@email.com') # login user er email
            exam_code = st.session_state.get('exam_code', '')

            cursor.execute('''
                INSERT INTO results (student_email, exam_code, exam_name, score, total_questions) 
                VALUES (?, ?, ?, ?, ?)
            ''', (student_email, exam_code, exam_name, score, total_questions))

            conn.commit()
            conn.close()
            st.session_state.result_saved = True # jate result save hoyeche seta mark kora


        # Exam ses kore dashboard e fire jawar jonno button
        if st.button("Return to Dashboard 🏠"):
            st.session_state.exam_started = False
            st.session_state.current_q_index = 0
            st.session_state.student_answers = {}
            st.rerun()

else:
    st.warning("Please, sign-in first.")