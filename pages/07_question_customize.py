import os
import streamlit as st
import sqlite3
import google.generativeai as genai
import json
from PIL import Image, ImageOps

# ==========================================
# 1. AUTHENTICATION & SETUP
# ==========================================
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.get("user_catagory") != "Teacher":
        st.error("**Access Denied!** This page is only for Teachers.")
        st.stop()

    def get_gemini_api_key():
        """Reads Gemini API key from env/secrets/session state."""
        key = st.session_state.get("gemini_api_key")
        if key: return str(key).strip()

        key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if key: return str(key).strip()

        try:
            key = st.secrets["GEMINI_API_KEY"]
            if key: return str(key).strip()
        except Exception:
            pass
        return None

    def prepare_image_for_ai(uploaded_file):
        """Converts image to a compatible format for Gemini."""
        uploaded_file.seek(0)
        image = Image.open(uploaded_file).convert("RGB")
        image.load()

        max_size = 1536
        width, height = image.size
        if max(width, height) > max_size:
            scale = max_size / max(width, height)
            image = image.resize((int(width * scale), int(height * scale)), Image.Resampling.LANCZOS)

        image = ImageOps.autocontrast(image)
        return image

    # ==========================================
    # 2. UI/UX CSS INJECTION (LIGHT THEME)
    # ==========================================
    st.set_page_config(page_title="Create Custom Exam", page_icon="📝", layout="centered")

    st.markdown("""
    <style>
        /* Global Theme (Pure White) */
        :root { color-scheme: light; }
        body, .stApp, .main .block-container { 
            background-color: #ffffff !important; 
            color: #1a1a1a !important; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main .block-container { max-width: 500px; padding: 1.5rem 1rem 5rem 1rem !important; margin: 0 auto; }
        
        /* Input & Form Styling */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select { 
            background-color: #ffffff !important; 
            color: #1a1a1a !important; 
            border: 1px solid #cbd5e1 !important; 
            border-radius: 8px !important; 
            padding: 10px !important;
        }
        .stTextInput>label, .stNumberInput>label, .stTextArea>label, .stSelectbox>label {
            color: #333333 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
        }

        /* Card Layout Targetting (Light Gray) */
        div[data-testid="stVerticalBlock"]:has(> div.element-container .card-marker-basic) {
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        div[data-testid="stVerticalBlock"]:has(> div.element-container .card-marker-ai) {
            background-color: #f1f5f9;
            border: 2px dashed #8b5cf6;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }

        /* Top Back Button */
        .back-btn-wrapper + div button { background: transparent !important; color: #10b981 !important; border: none !important; box-shadow: none !important; padding: 0 !important; font-weight: bold !important; font-size: 14px !important; justify-content: flex-start; }
        .back-btn-wrapper + div button:hover { color: #059669 !important; text-decoration: underline; background: transparent !important;}

        /* AI Button */
        .ai-btn-wrapper + div button { background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; padding: 12px !important; width: 100% !important; font-weight: bold !important; box-shadow: 0 4px 6px rgba(139, 92, 246, 0.3); }
        .ai-btn-wrapper + div button p { color: #ffffff !important; font-weight: bold !important; margin: 0; }
        
        /* Add Question Button (Inside Form) */
        .stForm button { background-color: #3b82f6 !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; padding: 12px !important; width: 100% !important; font-weight: bold !important; margin-top: 10px; box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3); }
        .stForm button p { color: #ffffff !important; font-weight: bold !important; margin: 0; }
        
        /* Publish Button */
        .publish-btn-wrapper + div button { background: linear-gradient(135deg, #10b981, #059669) !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; padding: 15px !important; width: 100% !important; font-size: 1.1rem !important; font-weight: bold !important; box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3); }
        .publish-btn-wrapper + div button p { color: #ffffff !important; font-weight: bold !important; margin: 0; }
        
    </style>
    """, unsafe_allow_html=True)


    # ==========================================
    # 3. SIDEBAR SETUP
    # ==========================================
    with st.sidebar:
        st.header("🔑 Gemini Setup")
        st.caption("Paste your Gemini API key if you want AI image scanning.")
        api_key_input = st.text_input("Paste your Gemini API key", type="password", value=st.session_state.get("gemini_api_key", ""), key="gemini_api_key_input")
        if st.button("Save API Key", use_container_width=True) and api_key_input:
            st.session_state.gemini_api_key = api_key_input.strip()
            genai.configure(api_key=st.session_state.gemini_api_key)
            st.success("Gemini API key saved.")

    api_key_ready = bool(st.session_state.get("gemini_api_key")) and str(st.session_state.get("gemini_api_key", "")).strip() != "YOUR_GEMINI_API_KEY"


    # ==========================================
    # 4. RENDER UI CONTENT
    # ==========================================
    
    # Top Navigation & Header
    st.markdown('<div class="back-btn-wrapper"></div>', unsafe_allow_html=True)
    if st.button("⬅️ Back to Dashboard"):
        st.switch_page("pages/04_teacher_dashboard.py")
        
    st.markdown('<h1 style="font-size: 24px; color: #1a1a1a; margin-top: -10px; margin-bottom: 20px;">Create Custom Exam</h1>', unsafe_allow_html=True)

    if "temp_questions" not in st.session_state:
        st.session_state.temp_questions = []

    # --- CARD 1: Basic Exam Information ---
    with st.container():
        st.markdown('<div class="card-marker-basic"></div>', unsafe_allow_html=True)
        exam_name = st.text_input("Exam Name", placeholder="e.g. Physics Sem 1")
        
        col1, col2 = st.columns(2)
        with col1:
            exam_code = st.text_input("Exam Code", placeholder="PHY-101").strip().upper()
        with col2:
            timer = st.number_input("Timer (Mins)", min_value=1, max_value=180, value=30)

    # --- CARD 2: AI Question Generator ---
    with st.container():
        st.markdown('<div class="card-marker-ai"></div>', unsafe_allow_html=True)
        # Text color explicitly darkened for visibility on light gray
        st.markdown('<h3 style="margin-top:0; font-size: 16px; color: #6d28d9;">✨ AI Question Generator</h3>', unsafe_allow_html=True)
        
        uploaded_image = st.file_uploader("Upload Question Image (JPG/PNG)", type=["png", "jpg", "jpeg"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Your Uploaded Image", use_container_width=True)
            
            if not api_key_ready:
                st.warning("Gemini API key is missing or invalid. Paste a valid key in the sidebar and click Save.")
            else:
                st.markdown('<div class="ai-btn-wrapper"></div>', unsafe_allow_html=True)
                if st.button("Scan Questions with AI 🪄"):
                    with st.spinner("Gemini is reading the image and creating questions..."):
                        try:
                            api_key = get_gemini_api_key()
                            if not api_key or api_key == "YOUR_GEMINI_API_KEY":
                                st.error("Gemini API key is missing or invalid.")
                                st.stop()

                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel('gemini-1.5-flash')

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
                            prepared_image = prepare_image_for_ai(uploaded_image)
                            response = model.generate_content([prompt, prepared_image])
                            
                            json_text = response.text.replace("```json", "").replace("```", "").strip()
                            ai_questions = json.loads(json_text)

                            for q in ai_questions:
                                st.session_state.temp_questions.append(q)

                            st.success(f"Magic successful! {len(ai_questions)} questions added to your list.")
                        except json.JSONDecodeError:
                            st.error("Gemini could not parse the image into structured questions. Upload a clearer image.")
                        except Exception as e:
                            st.error(f"Unable to process the image right now. Details: {e}")

    # --- CARD 3: Manual Question Entry Form ---
    with st.container():
        st.markdown('<div class="card-marker-basic"></div>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="margin-top:0; font-size: 16px; color: #1a1a1a;">📝 Add Manually (Total added: {len(st.session_state.temp_questions)})</h3>', unsafe_allow_html=True)
        
        with st.form(key="question_form", clear_on_submit=True):
            q_text = st.text_area("Question Text", placeholder="Type your question here...")
            
            # Formatted exactly to a 2x2 Grid per requirements
            colA, colB = st.columns(2)
            with colA:
                opt_a = st.text_input("Option A")
                opt_c = st.text_input("Option C")
            with colB:
                opt_b = st.text_input("Option B")
                opt_d = st.text_input("Option D")

            correct_opt = st.selectbox("Correct Answer", ["A", "B", "C", "D"])

            add_q_btn = st.form_submit_button(label="Add This Question ➕")

            if add_q_btn:
                if q_text and opt_a and opt_b and opt_c and opt_d:
                    st.session_state.temp_questions.append({
                        "question_text": q_text,
                        "option_a": opt_a,
                        "option_b": opt_b,
                        "option_c": opt_c,
                        "option_d": opt_d,
                        "correct_option": correct_opt
                    })
                    st.success("Question added to the list!")
                    st.rerun()
                else:
                    st.error("Please fill in all the fields for the question.")

    # Preview Output
    if st.session_state.temp_questions:
        st.markdown('<h3 style="color: #1a1a1a;">Current Question Paper Preview:</h3>', unsafe_allow_html=True)
        for i, q in enumerate(st.session_state.temp_questions):
            st.write(f"**Q{i+1}:** {q['question_text']} *(Correct: {q['correct_option']})*")

    st.write("") # Spacer

    # --- PUBLISH EXAM BUTTON ---
    st.markdown('<div class="publish-btn-wrapper"></div>', unsafe_allow_html=True)
    if st.button("Publish & Post Entire Exam 🚀"):
        if not exam_name or not exam_code:
            st.error("Please provide the exam name and unique code.")
        elif len(st.session_state.temp_questions) == 0:
            st.error("Please add at least 1 question before publishing the exam!")
        else:
            db_file = "ExamMate.db"
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exams (
                    exam_code TEXT PRIMARY KEY,
                    exam_name TEXT NOT NULL,
                    teacher_email TEXT NOT NULL,
                    timer_minutes INTEGER NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_code TEXT,
                    question_text TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    option_c TEXT NOT NULL,
                    option_d TEXT NOT NULL,
                    correct_option TEXT NOT NULL,
                    FOREIGN KEY (exam_code) REFERENCES exams (exam_code)
                )
            """)
            conn.commit()

            try:
                t_email = st.session_state.get('user_email', 'teacher@email.com')
                cursor.execute(
                    "INSERT INTO exams (exam_code, exam_name, teacher_email, timer_minutes) VALUES (?, ?, ?, ?)",
                    (exam_code, exam_name, t_email, timer)
                )

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

                conn.commit() 
                st.balloons()
                st.success(f"🎉 Awesome! Your exam has been successfully created. Share this code with your students: {exam_code}")
                st.session_state.temp_questions = []

            except sqlite3.IntegrityError:
                st.error("⚠️ This exam code is already used by another teacher! Please provide a different unique code.")
            finally:
                conn.close()

else:
    st.warning("Please, sign-in first.")