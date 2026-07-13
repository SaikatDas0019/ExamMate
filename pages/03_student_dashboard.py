import streamlit as st

# ==========================================
# UI/UX CSS INJECTION (LIGHT THEME & MOBILE FIRST)
# ==========================================
st.set_page_config(page_title="ExamMate | Dashboard", page_icon="🚀", layout="centered")

st.markdown("""
<style>
    /* Global Theme (Light Theme) */
    :root { color-scheme: light; }
    body, .stApp, .main .block-container { 
        background-color: #ffffff !important; 
        color: #333333 !important; 
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .main .block-container { max-width: 450px; padding: 1.5rem 1rem 5rem 1rem !important; margin: 0 auto; }
    
    /* Hide default Streamlit elements */
    header[data-testid="stHeader"] { display: none; }
    .stDeployButton { display: none; }
    div[data-testid="stToolbar"] { display: none; }
    
    /* Header Section */
    .profile-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
    .profile-left { display: flex; align-items: center; gap: 12px; }
    .avatar { width: 50px; height: 50px; background: #e0f2fe; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; border: 2px solid #38bdf8; }
    .greeting h3 { margin: 0; font-size: 1.2rem; font-weight: 700; color: #111827; }
    .greeting p { margin: 0; font-size: 0.8rem; color: #6b7280; }
    .bell-icon { font-size: 1.2rem; color: #4b5563; background: #f3f4f6; padding: 8px; border-radius: 50%; border: 1px solid #e5e7eb; }

    /* My Progress Grid */
    .section-title { font-size: 0.95rem; font-weight: 700; color: #1f2937; margin: 1.5rem 0 0.8rem 0; display: flex; align-items: center; gap: 6px; }
    .progress-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 1.5rem; }
    .progress-card { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 12px; display: flex; align-items: center; gap: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .progress-icon { font-size: 1.5rem; color: #22c55e; }
    .progress-info span { font-size: 0.75rem; color: #4b5563; display: block; margin-bottom: 2px; }
    .progress-info b { font-size: 1.1rem; color: #111827; }

    /* Popular Exams Horizontal Scroll */
    .horizontal-scroll-container + div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 10px;
        gap: 12px;
        scrollbar-width: none; 
    }
    .horizontal-scroll-container + div[data-testid="stHorizontalBlock"]::-webkit-scrollbar { display: none; }
    .horizontal-scroll-container + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        width: auto !important;
        min-width: max-content !important; 
        flex: 0 0 auto !important;
    }
    
    /* Popular Exams Pills styling */
    .pill-jee + div button { background: #ef4444 !important; border: none !important; border-radius: 25px !important; padding: 6px 20px !important; }
    .pill-neet + div button { background: #f97316 !important; border: none !important; border-radius: 25px !important; padding: 6px 20px !important; }
    .pill-wbjee + div button { background: #0ea5e9 !important; border: none !important; border-radius: 25px !important; padding: 6px 20px !important; }
    .pill-adv + div button { background: #8b5cf6 !important; border: none !important; border-radius: 25px !important; padding: 6px 20px !important; }
    div[class^="pill-"] + div button p { color: #ffffff !important; font-weight: 600; margin: 0; font-size: 0.9rem;}

    /* Navigation flow state buttons */
    .flow-btn + div button { border-radius: 12px !important; font-weight: 600 !important; }

    /* Fixed Bottom Navigation Bar & Invisible Buttons */
    .bottom-nav-overlay {
        position: fixed; bottom: 0; left: 0; right: 0; background: #ffffff;
        border-top: 1px solid #e5e7eb; padding: 10px 0; z-index: 999;
        display: flex; justify-content: space-around; max-width: 450px; margin: 0 auto;
        box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .nav-item { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 0.75rem; color: #9ca3af; position: relative; width: 60px; font-weight: 600; }
    .nav-item.active { color: #22c55e; }
    .nav-icon { font-size: 1.4rem; }
    .nav-buttons-hider + div[data-testid="stHorizontalBlock"] {
        position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000; opacity: 0.01; 
        max-width: 450px; margin: 0 auto; display: flex; height: 60px;
    }
    .nav-buttons-hider + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] { flex: 1 1 0% !important; }
    .nav-buttons-hider + div[data-testid="stHorizontalBlock"] button { height: 60px !important; width: 100% !important; margin: 0 !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# BACKEND LOGIC & RENDER
# ==========================================

# State management for Exam Navigation Flow
if "dash_flow_step" not in st.session_state:
    st.session_state.dash_flow_step = "categories"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = ""
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = ""

# Authentication Check
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.get("user_catagory") != "Student":
        st.error("**Access Denied!** This page is only for Students.")
        st.stop()
        
    user_name = st.session_state.get("user_name", "Student")

    # Header Section
    st.markdown(f"""
    <div class="profile-header">
        <div class="profile-left">
            <div class="avatar">👤</div>
            <div class="greeting">
                <h3>Hi, {user_name}</h3>
                <p>Let's ace your exams! 🚀</p>
            </div>
        </div>
        <div class="bell-icon">🔔</div>
    </div>
    """, unsafe_allow_html=True)

    # My Progress Section
    st.markdown('<div class="section-title">📈 My Progress</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="progress-grid">
        <div class="progress-card"><div class="progress-icon">🏅</div><div class="progress-info"><span>Score</span><b>01</b></div></div>
        <div class="progress-card"><div class="progress-icon">📅</div><div class="progress-info"><span>Total Exams</span><b>00</b></div></div>
        <div class="progress-card"><div class="progress-icon">↗️</div><div class="progress-info"><span>Highest Marks</span><b>00</b></div></div>
        <div class="progress-card"><div class="progress-icon">🏆</div><div class="progress-info"><span>Lowest Marks</span><b>00</b></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")


# ==========================================
# 0. INITIALIZE SESSION STATES
# ==========================================
# Ensure states exist so the app doesn't throw an error on the first load
if "dash_flow_step" not in st.session_state:
    st.session_state.dash_flow_step = "categories"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = ""
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = ""

# ==========================================
# 1. DEFINE RENDER FUNCTIONS
# ==========================================
def exam_flow():
    st.markdown(f"**Selected:** {st.session_state.selected_category} > {st.session_state.selected_subject}")
    
    if st.button("⬅️ Change Subject"):
        st.session_state.dash_flow_step = "subjects"
        st.rerun()
        
    st.write("")
    
    # Build prefix based on selections to construct the DB exam code
    cat_formatted = st.session_state.selected_category.replace(" ", "").upper()
    sub_formatted = st.session_state.selected_subject
    
    st.markdown('<div class="flow-btn"></div>', unsafe_allow_html=True)
    if st.button("Class 12 Chemistry - Group 18 Elements (Noble Gases)", type="primary", use_container_width=True):
        st.session_state.exam_code = 'EXAM-1723'
        st.switch_page("pages/08_student_exam.py")
    
    st.markdown('<div class="flow-btn"></div>', unsafe_allow_html=True)
    if st.button("Exam 2", type="primary", use_container_width=True):
        st.session_state.exam_code = f"{cat_formatted}-{sub_formatted}-02"
        st.switch_page("pages/08_student_exam.py")
    
    st.markdown('<div class="flow-btn"></div>', unsafe_allow_html=True)
    if st.button("Exam 3", type="primary", use_container_width=True):
        st.session_state.exam_code = f"{cat_formatted}-{sub_formatted}-03"
        st.switch_page("pages/08_student_exam.py")

def subject_flow():
    st.markdown(f"**Selected:** {st.session_state.selected_category}")
    
    if st.button("⬅️ Change Category"):
        st.session_state.dash_flow_step = "categories"
        st.rerun()
        
    st.write("")
    
    if st.button("Physics ⚛️", use_container_width=True):
        st.session_state.selected_subject = "PHY"
        st.session_state.dash_flow_step = "exams"
        st.rerun() 
        # Notice we removed exam_flow() from here
    
    if st.button("Chemistry 🧪", use_container_width=True):
        st.session_state.selected_subject = "CHEM"
        st.session_state.dash_flow_step = "exams"
        st.rerun()
    
    if st.button("Math 📐", use_container_width=True):
        st.session_state.selected_subject = "MATH"
        st.session_state.dash_flow_step = "exams"
        st.rerun()

# ==========================================
# 2. MAIN EXECUTION ROUTER
# ==========================================
st.markdown('<div class="section-title">Explore Exams &nbsp; <span style="font-size:0.8rem; color:#22c55e;">></span></div>', unsafe_allow_html=True)

# Route the user to the correct UI based on the current state
if st.session_state.dash_flow_step == "categories":
    st.markdown('<div class="horizontal-scroll-container"></div>', unsafe_allow_html=True)
    
    if st.button("JEE Main", use_container_width=True):
        st.session_state.selected_category = "JEE Main"
        st.session_state.dash_flow_step = "subjects"
        st.rerun()
        # Removed subject_flow() from here
        
    if st.button("NEET", use_container_width=True):
        st.session_state.selected_category = "NEET"
        st.session_state.dash_flow_step = "subjects"
        st.rerun()
        
    if st.button("WBJEE", use_container_width=True):
        st.session_state.selected_category = "WBJEE"
        st.session_state.dash_flow_step = "subjects"
        st.rerun()
        
    if st.button("JEE Advance", use_container_width=True):
        st.session_state.selected_category = "JEE Advance"
        st.session_state.dash_flow_step = "subjects"
        st.rerun()

elif st.session_state.dash_flow_step == "subjects":
    subject_flow()

elif st.session_state.dash_flow_step == "exams":
    exam_flow()
else:
    st.warning("Please, sign-in first.")
    if st.button("⬅️ Sign In page"):
        st.switch_page("pages/02_signin.py")