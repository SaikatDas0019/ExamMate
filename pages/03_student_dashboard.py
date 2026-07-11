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

    /* Teacher's Exam Code Input Section */
    .stTextInput > div > div > input { 
        background: #f9fafb !important; border: 1px solid #d1d5db !important; 
        color: #111827 !important; border-radius: 12px !important; height: 46px !important; padding: 10px 16px !important; 
    }
    
    /* Search Button Inline Alignment */
    .search-btn-wrapper + div button {
        background: transparent !important; border: 1px solid #d1d5db !important; 
        color: #0ea5e9 !important; border-radius: 12px !important; height: 46px !important; width: 100%;
        margin-top: 0px; 
        display: flex; justify-content: center; align-items: center;
    }
    .search-btn-wrapper + div button:hover { background: #f0f9ff !important; border-color: #38bdf8 !important; }
    
    /* AI Generated Exam Button */
    .ai-btn-wrapper + div button {
        background: linear-gradient(90deg, #6b21a8 0%, #4c1d95 100%) !important;
        border: none !important; color: #ffffff !important;
        border-radius: 12px !important; padding: 12px !important;
        font-weight: 600 !important; font-size: 1rem !important; margin-top: 10px;
        box-shadow: 0 4px 12px rgba(107, 33, 168, 0.3);
    }
    .ai-btn-wrapper + div button p { color: #ffffff !important; margin: 0; }
    .ai-btn-wrapper + div button:hover { opacity: 0.95; transform: translateY(-1px); }

    /* My Exams Large Cards */
    .exam-card-1 + div button { 
        background: linear-gradient(180deg, #0f766e 0%, #115e59 100%) !important; 
        border: none !important; height: 120px !important; border-radius: 16px !important; 
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .exam-card-2 + div button { 
        background: linear-gradient(180deg, #6b21a8 0%, #4c1d95 100%) !important; 
        border: none !important; height: 120px !important; border-radius: 16px !important;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .exam-card-1 + div button p, .exam-card-2 + div button p { color: #ffffff !important; font-weight: 600; }
    
    /* ========================================================
       BUG FIX 1: Popular Exams Horizontal Scroll
       ======================================================== */
    .horizontal-scroll-container + div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 10px;
        gap: 12px;
        scrollbar-width: none; 
    }
    .horizontal-scroll-container + div[data-testid="stHorizontalBlock"]::-webkit-scrollbar { display: none; }
    
    /* Force columns to act as individual scrolling items without wrapping */
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

    /* ========================================================
       BUG FIX 2: Fixed Bottom Navigation Bar & Invisible Buttons
       ======================================================== */
    .bottom-nav-overlay {
        position: fixed; bottom: 0; left: 0; right: 0; background: #ffffff;
        border-top: 1px solid #e5e7eb; padding: 10px 0; z-index: 999;
        display: flex; justify-content: space-around; max-width: 450px; margin: 0 auto;
        box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .nav-item { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 0.75rem; color: #9ca3af; position: relative; width: 60px; font-weight: 600; }
    .nav-item.active { color: #22c55e; }
    .nav-icon { font-size: 1.4rem; }

    /* Hide the native Streamlit buttons and layer them invisibly over the custom HTML nav */
    .nav-buttons-hider + div[data-testid="stHorizontalBlock"] {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        opacity: 0.01; /* Invisible but remains clickable */
        max-width: 450px;
        margin: 0 auto;
        display: flex;
        height: 60px;
    }
    .nav-buttons-hider + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        flex: 1 1 0% !important; /* Distribute hitboxes evenly across the 4 tabs */
    }
    .nav-buttons-hider + div[data-testid="stHorizontalBlock"] button {
        height: 60px !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# BACKEND LOGIC & RENDER
# ==========================================

# 1. Authentication Check
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.get("user_catagory") != "Student":
        st.error("**Access Denied!** This page is only for Students.")
        st.stop()
        
    user_name = st.session_state.get("user_name", "Student")

    # 2. Header Section
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

    # 3. My Progress Section
    st.markdown('<div class="section-title">📈 My Progress</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="progress-grid">
        <div class="progress-card"><div class="progress-icon">🏅</div><div class="progress-info"><span>Score</span><b>01</b></div></div>
        <div class="progress-card"><div class="progress-icon">📅</div><div class="progress-info"><span>Total Exams</span><b>00</b></div></div>
        <div class="progress-card"><div class="progress-icon">↗️</div><div class="progress-info"><span>Highest Marks</span><b>00</b></div></div>
        <div class="progress-card"><div class="progress-icon">🏆</div><div class="progress-info"><span>Lowest Marks</span><b>00</b></div></div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Teacher's Exam Code & AI Exam Button
    st.markdown('<div class="section-title">Teacher\'s Exam Code:</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.85, 0.15]) 
    with col1:
        st.session_state.exam_code = st.text_input("HiddenLabel", placeholder="e.g: PHY-101", label_visibility="collapsed")
    with col2:
        st.markdown('<div class="search-btn-wrapper"></div>', unsafe_allow_html=True)
        if st.button("🔍", key="search_exam"):
            st.switch_page("pages/08_student_exam.py")
            
    st.markdown('<div class="ai-btn-wrapper"></div>', unsafe_allow_html=True)
    if st.button("🤖 AI Generated Exam ✨", use_container_width=True): 
        st.toast("AI Exam feature coming soon!") 

    # 5. My Exams
    st.markdown('<div class="section-title">My Exams &nbsp; <span style="font-size:0.8rem; color:#22c55e;">></span></div>', unsafe_allow_html=True)
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        st.markdown('<div class="exam-card-1"></div>', unsafe_allow_html=True)
        clas_11 = st.button("Class 11 \n\n Sem 1 📖", use_container_width=True)
    with col_ex2:
        st.markdown('<div class="exam-card-2"></div>', unsafe_allow_html=True)
        clas_12 = st.button("Class 12 \n\n Sem 3 📖", use_container_width=True)

    # 6. Popular Exams (Horizontal Scroll)
    st.markdown('<div class="section-title">Popular Exams &nbsp; <span style="font-size:0.8rem; color:#22c55e;">></span></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="horizontal-scroll-container"></div>', unsafe_allow_html=True)
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        st.markdown('<div class="pill-jee"></div>', unsafe_allow_html=True)
        jee_main = st.button("JEE Main")
    with col_p2:
        st.markdown('<div class="pill-neet"></div>', unsafe_allow_html=True)
        neet = st.button("NEET")
    with col_p3:
        st.markdown('<div class="pill-wbjee"></div>', unsafe_allow_html=True)
        wbjee = st.button("WBJEE")
    with col_p4:
        st.markdown('<div class="pill-adv"></div>', unsafe_allow_html=True)
        jee_adv = st.button("JEE Advance")


    # 7. Bottom Navigation Bar
    st.markdown("""
    <div class="bottom-nav-overlay">
        <div class="nav-item active"><div class="nav-icon">🏠</div><span>Home</span></div>
        <div class="nav-item"><div class="nav-icon">📄</div><span>Tests</span></div>
        <div class="nav-item"><div class="nav-icon">📊</div><span>Analytics</span></div>
        <div class="nav-item"><div class="nav-icon">👤</div><span>Profile</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Wrap the routing buttons in a specific CSS marker so we can target them reliably
    st.markdown('<div class="nav-buttons-hider"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("HomeNav", key="b_home"): pass 
    with c2: 
        if st.button("TestNav", key="b_test"): pass 
    with c3: 
        if st.button("AnalyticNav", key="b_analytics"): st.switch_page("pages/09_student_analytics.py")
    with c4: 
        if st.button("ProfileNav", key="b_profile"): st.switch_page("pages/05_student_profile.py")

else:
    st.warning("Please, sign-in first.")