import streamlit as st
import sqlite3
import google.generativeai as genai
import json
from PIL import Image

# 1. API Key set kora (Ekhane tomar nijer Google Gemini API key dibe)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

st.title("👨‍🏫 Teacher Panel - Create Custom Exam")

# ==========================================
# Part 1: Basic Exam Information
# ==========================================
# Porikkhar basic information (eti ekbari input hobe)
exam_name = st.text_input("Exam Name (e.g., Class 11 Physics Semester 1)")
exam_code = st.text_input("Unique Exam Code (e.g., WB-PHY-11)").strip().upper()
timer = st.number_input("Exam Duration (minutes)", min_value=1, max_value=180, value=30)

st.divider()

# Session state e proshno gulo samoyik bhabe joma rakhar jonno ekte list toiri kora
if "temp_questions" not in st.session_state:
    st.session_state.temp_questions = []

# ==========================================
# Part 2: AI Question Generator (Gemini)
# ==========================================
st.subheader("🤖 Create Magic Questions with Gemini AI")
st.write("Tired of typing questions? Upload a picture of a book or notebook, and AI will generate the questions for you!")

# Chhobi upload korar option
uploaded_image = st.file_uploader("Upload Question Image (JPG/PNG)", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # Chhobi screen e chhoto kore dekhano
    image = Image.open(uploaded_image)
    st.image(image, caption="Your Uploaded Image", width=350)
    
    if st.button("Scan Questions with AI 🪄", type="primary"):
        with st.spinner("Gemini is reading the image and creating questions... Please wait..."):
            try:
                # Gemini model call kora (gemini-1.5-flash chhobi process korte khub fast)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Prompt (AI ke bojhanor jonno English e kora nirdesh)
                prompt = """
                This image is a test question paper. Extract the MCQ questions from it and provide the exact response in the following JSON format:
                [
                  {
                    "question_text": "Question goes here",
                    "option_a": "Option A text",
                    "option_b": "Option B text",
                    "option_c": "Option C text",
                    "option_d": "Option D text",
                    "correct_option": "A" (or B/C/D whichever is correct)
                  }
                ]
                Very important: Only provide the JSON code, do not write anything else.
                """
                
                # Chhobi ebong nirdesh pathano
                response = model.generate_content([prompt, image])
                
                # JSON text ke python er list e porinoto kora
                # (Majhe majhe AI ```json likhe dey, seta muche porishkar kora hocche)
                json_text = response.text.replace("```json", "").replace("```", "").strip()
                ai_questions = json.loads(json_text)
                
                # AI er banano proshno gulo session state er list e jog kora
                for q in ai_questions:
                    st.session_state.temp_questions.append(q)
                    
                st.success(f"Magic successful! {len(ai_questions)} questions have been directly added to your list. Check the preview below.")
                
            except Exception as e:
                st.error("Sorry, there was a problem understanding the image. Please try uploading a clearer picture.")

st.divider()

# ==========================================
# Part 3: Manual Question Entry Form
# ==========================================
st.subheader(f"📝 Add Questions Manually (Currently added: {len(st.session_state.temp_questions)})")

# Proshno input newar form
with st.form(key="question_form", clear_on_submit=True):
    q_text = st.text_area("Type your question here:")
    col1, col2 = st.columns(2)
    with col1:
        opt_a = st.text_input("Option A:")
        opt_b = st.text_input("Option B:")
    with col2:
        opt_c = st.text_input("Option C:")
        opt_d = st.text_input("Option D:")
        
    correct_opt = st.selectbox("Which is the correct option?", ["A", "B", "C", "D"])
    
    # Form er submit button
    add_q_btn = st.form_submit_button(label="Add This Question ➕")
    
    if add_q_btn:
        if q_text and opt_a and opt_b and opt_c and opt_d:
            # Ekti dictionary baniye session state er list e push kora holo
            st.session_state.temp_questions.append({
                "question_text": q_text,
                "option_a": opt_a,
                "option_b": opt_b,
                "option_c": opt_c,
                "option_d": opt_d,
                "correct_option": correct_opt
            })
            st.success("Question added to the list! You can add more questions.")
            st.rerun()
        else:
            st.error("Please fill in all the fields for the question.")

# ==========================================
# Part 4: Preview & Publish Exam
# ==========================================
# Added proshno gulor ekti chhoto preview niche dekhano
if st.session_state.temp_questions:
    st.write("### Current Question Paper Preview:")
    for i, q in enumerate(st.session_state.temp_questions):
        st.write(f"**Q{i+1}:** {q['question_text']} *(Correct: {q['correct_option']})*")

st.divider()

# Final button: sob proshno eksathe database e (SQL) save korar jonno
if st.button("Publish & Post Entire Exam 🚀", type="primary"):
    if not exam_name or not exam_code:
        st.error("Please provide the exam name and unique code.")
    elif len(st.session_state.temp_questions) == 0:
        st.error("Please add at least 1 question before publishing the exam!")
    else:
        # --- Backend SQL er kaaj shuru ---
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()
        
        try:
            # a) Prothome 'exams' table e porikkhar tothyo save kora
            t_email = st.session_state.get('user_email', 'teacher@email.com')
            cursor.execute(
                "INSERT INTO exams (exam_code, exam_name, teacher_email, timer_minutes) VALUES (?, ?, ?, ?)",
                (exam_code, exam_name, t_email, timer)
            )
            
            # b) Loop chaliye list er sobkoti proshno 'questions' table e save kora
            for q in st.session_state.temp_questions:
                cursor.execute('''
                    INSERT INTO questions 
                    (exam_code, question_text, option_a, option_b, option_c, option_d, correct_option) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    exam_code, 
                    q["question_text"], 
                    q["option_a"], 
                    q["option_b"], 
                    q["option_c"], 
                    q["option_d"], 
                    q["correct_option"]
                ))
            
            # Database e sob permanently save holo
            conn.commit() 
            st.balloons() # Screen e ekta anonder animation hobe
            st.success(f"🎉 Awesome! Your exam has been successfully created. Share this code with your students: {exam_code}")
            
            # Porikkha save hoye jaoar por samoyik list ti khali kore dewa
            st.session_state.temp_questions = []
            
        except sqlite3.IntegrityError:
            st.error("⚠️ This exam code is already used by another teacher! Please provide a different unique code.")
        finally:
            conn.close()