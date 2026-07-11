import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ==========================================
# 1. AUTHENTICATION CHECK & STATE ROUTER INIT
# ==========================================
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in"):
    if st.session_state.get("user_catagory") != "Teacher":
        st.error("**Access Denied!** This page is only for Teachers.")
        st.stop()
else:
    st.warning("Please sign in first.")
    st.stop()

user_name = st.session_state.get("user_name", "Teacher")
teacher_email = st.session_state.get("user_email", "")

# Initialize State-Based View Router
if "current_view" not in st.session_state:
    st.session_state.current_view = "dashboard"
if "analysis_exam_code" not in st.session_state:
    st.session_state.analysis_exam_code = None
if "analysis_exam_name" not in st.session_state:
    st.session_state.analysis_exam_name = None

# Callback Functions for Routing
def go_to_dashboard():
    st.session_state.current_view = "dashboard"

def go_to_all_exams():
    st.session_state.current_view = "view_all_exams"

def go_to_analysis(exam_code, exam_name):
    st.session_state.analysis_exam_code = exam_code
    st.session_state.analysis_exam_name = exam_name
    st.session_state.current_view = "analysis"


# ==========================================
# 2. DATABASE HELPER FUNCTIONS
# ==========================================
DB_FILE = "ExamMate.db"

def fetch_dashboard_data(email):
    """Fetches all dynamic metrics and exams for the logged-in teacher."""
    data = {
        "total_exams": 0,
        "total_students": 0,
        "avg_score": 0.0,
        "active_exams": 0,
        "exams_list": []
    }
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM exams WHERE teacher_email = ?", (email,))
        data["total_exams"] = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            SELECT COUNT(DISTINCT student_email) 
            FROM results 
            WHERE exam_code IN (SELECT exam_code FROM exams WHERE teacher_email = ?)
        """, (email,))
        data["total_students"] = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            SELECT AVG(CAST(score AS FLOAT) / total_questions * 100) 
            FROM results 
            WHERE exam_code IN (SELECT exam_code FROM exams WHERE teacher_email = ?)
            AND total_questions > 0
        """, (email,))
        avg_fetch = cursor.fetchone()[0]
        data["avg_score"] = round(avg_fetch) if avg_fetch else 0
        
        try:
            cursor.execute("SELECT COUNT(*) FROM exams WHERE teacher_email = ? AND status = 'Active'", (email,))
            data["active_exams"] = cursor.fetchone()[0] or 0
        except sqlite3.OperationalError:
            data["active_exams"] = data["total_exams"] 
            
        cursor.execute("SELECT exam_name, exam_code FROM exams WHERE teacher_email = ? ORDER BY rowid DESC", (email,))
        data["exams_list"] = cursor.fetchall()
        
    except sqlite3.OperationalError as e:
        st.toast("Note: Some database tables are missing or empty.")
    finally:
        if 'conn' in locals():
            conn.close()
            
    return data

db_data = fetch_dashboard_data(teacher_email)


# ==========================================
# 3. UI/UX CSS INJECTION (LIGHT THEME)
# ==========================================
st.set_page_config(page_title="ExamMate | Teacher", page_icon="👨‍🏫", layout="centered")

st.markdown("""
<style>
    :root { color-scheme: light; }
    body, .stApp, .main .block-container { background-color: #ffffff !important; color: #333333 !important; font-family: 'Segoe UI', Roboto, sans-serif; }
    .main .block-container { max-width: 480px; padding: 1.5rem 1rem 6rem 1rem !important; margin: 0 auto; }
    header[data-testid="stHeader"], .stDeployButton, div[data-testid="stToolbar"] { display: none; }
    
    /* Header & Metrics */
    .profile-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; }
    .profile-info { display: flex; align-items: center; gap: 15px; }
    .avatar { width: 55px; height: 55px; background: #e0f2fe; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; border: 2px solid #38bdf8; }
    .greeting h3 { margin: 0; font-size: 1.3rem; font-weight: 700; color: #111827; }
    .greeting p { margin: 0; font-size: 0.85rem; color: #4b5563; }
    .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 1.5rem; }
    .metric-card { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 14px; padding: 15px; display: flex; flex-direction: column; gap: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .metric-header { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #4b5563; font-weight: 600;}
    .metric-val { font-size: 1.6rem; font-weight: 700; color: #111827; margin: 0; line-height: 1; }
    
    /* Action Buttons */
    .btn-create-wrapper + div button { background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important; border: none !important; border-radius: 12px !important; padding: 15px !important; height: auto !important; box-shadow: 0 4px 6px rgba(34, 197, 94, 0.2); }
    .btn-ai-wrapper + div button { background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%) !important; border: none !important; border-radius: 12px !important; padding: 15px !important; height: auto !important; box-shadow: 0 4px 6px rgba(139, 92, 246, 0.2); }
    .btn-create-wrapper + div button p, .btn-ai-wrapper + div button p { color: #ffffff !important; font-weight: 700 !important; margin: 0; font-size: 1rem;}
    
    /* Exam Cards (Modified for Streamlit Column alignment) */
    .exam-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px 14px 0 0; padding: 15px; display: flex; flex-direction: column; justify-content: space-between; min-height: 110px; border-bottom: none;}
    .exam-title { font-size: 0.9rem; color: #1e293b; font-weight: 700; margin-bottom: 8px; line-height: 1.2; }
    .exam-code-box { background: #f1f5f9; padding: 8px 12px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #e2e8f0; }
    .exam-code { font-family: monospace; font-size: 1.1rem; color: #0f172a; font-weight: 700; }
    
    /* Analysis Button stitched to bottom of card */
    .ana-btn-wrapper + div button { background: #f8fafc !important; border: 1px solid #e2e8f0 !important; border-radius: 0 0 14px 14px !important; width: 100% !important; color: #3b82f6 !important; font-weight: 600 !important; margin-bottom: 15px; transition: all 0.2s ease;}
    .ana-btn-wrapper + div button:hover { background: #eff6ff !important; border-color: #bfdbfe !important; }

    /* Student Analytics 2x2 */
    .btn-jee + div button { background: #ef4444 !important; border: none !important; border-radius: 12px !important; height: 50px !important;}
    .btn-neet + div button { background: #f97316 !important; border: none !important; border-radius: 12px !important; height: 50px !important;}
    .btn-wbjee + div button { background: #0ea5e9 !important; border: none !important; border-radius: 12px !important; height: 50px !important;}
    .btn-adv + div button { background: #8b5cf6 !important; border: none !important; border-radius: 12px !important; height: 50px !important;}
    div[class^="btn-"] + div button p { color: #ffffff !important; font-weight: 600 !important; margin: 0; font-size: 0.95rem;}
    
    /* Bottom Nav */
    .bottom-nav-overlay { position: fixed; bottom: 0; left: 0; right: 0; background: #ffffff; border-top: 1px solid #e5e7eb; padding: 10px 0; z-index: 999; display: flex; justify-content: space-around; max-width: 480px; margin: 0 auto; box-shadow: 0 -4px 10px rgba(0,0,0,0.05); }
    .nav-item { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 0.75rem; color: #9ca3af; width: 60px; font-weight: 600; }
    .nav-item.active { color: #22c55e; }
    .nav-icon { font-size: 1.4rem; }
    .nav-buttons-hider + div[data-testid="stHorizontalBlock"] { position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000; opacity: 0.01; max-width: 480px; margin: 0 auto; display: flex; height: 60px; }
    .nav-buttons-hider + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] { flex: 1 1 0% !important; }
    .nav-buttons-hider + div[data-testid="stHorizontalBlock"] button { height: 60px !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. VIEW RENDERING LOGIC
# ==========================================

def render_exam_card(exam_name, exam_code, col):
    """Helper to render individual exam cards inside a Streamlit column"""
    with col:
        st.markdown(f"""
        <div class="exam-card">
            <div class="exam-title">{exam_name}</div>
            <div class="exam-code-box">
                <span style="font-size: 0.7rem; color: #64748b;">Code</span>
                <span class="exam-code">{exam_code}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="ana-btn-wrapper"></div>', unsafe_allow_html=True)
        st.button("View Analysis 📈", key=f"ana_{exam_code}", on_click=go_to_analysis, args=(exam_code, exam_name))


# ------------------------------------------
# VIEW: DASHBOARD (DEFAULT)
# ------------------------------------------
if st.session_state.current_view == "dashboard":
    
    # Header
    st.markdown(f"""
    <div class="profile-header">
        <div class="profile-info">
            <div class="avatar">👤</div>
            <div class="greeting">
                <h3>Hi, {user_name}</h3>
                <p>Welcome back! Let's manage your classes.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top Metrics
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card"><div class="metric-header">🏅 Total Exams Created</div><div class="metric-val">{db_data['total_exams']:02d}</div></div>
        <div class="metric-card"><div class="metric-header">👥 Total Students</div><div class="metric-val">{db_data['total_students']}</div></div>
        <div class="metric-card"><div class="metric-header">📈 Average Score</div><div class="metric-val">{db_data['avg_score']}%</div></div>
        <div class="metric-card"><div class="metric-header">🏆 Active Exams</div><div class="metric-val">{db_data['active_exams']:02d}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Action Buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.markdown('<div class="btn-create-wrapper"></div>', unsafe_allow_html=True)
        if st.button("📝 Create New Exam", use_container_width=True):
            st.switch_page("pages/07_question_customize.py") 
    with col_btn2:
        st.markdown('<div class="btn-ai-wrapper"></div>', unsafe_allow_html=True)
        if st.button("🤖 AI Generate Questions ✨", use_container_width=True):
            st.toast("AI Generator Module launching soon!")

    # Recent Exams Section (Top 2)
    st.write("") 
    head_col1, head_col2 = st.columns([0.6, 0.4])
    with head_col1:
        st.markdown('<div style="font-size: 1.1rem; font-weight: 700; color: #111827;">Recent Exams</div>', unsafe_allow_html=True)
    with head_col2:
        if db_data['exams_list']:
            st.button("View All ➡️", on_click=go_to_all_exams, use_container_width=True)

    if not db_data['exams_list']:
        st.info("You haven't created any exams yet.")
    else:
        recent_exams = db_data['exams_list'][:2] # Get only top 2
        cols = st.columns(2)
        for idx, exam in enumerate(recent_exams):
            render_exam_card(exam[0], exam[1], cols[idx % 2])

    # Student Results Bottom Grid (2x2)
    st.markdown('<div style="font-size: 1.1rem; font-weight: 700; color: #111827; margin-top: 1rem; margin-bottom: 10px;">Student Results & Analytics</div>', unsafe_allow_html=True)
    r1c1, r1c2 = st.columns([1, 1])
    with r1c1:
        st.markdown('<div class="btn-jee"></div>', unsafe_allow_html=True)
        st.button("JEE Main", use_container_width=True)
    with r1c2:
        st.markdown('<div class="btn-neet"></div>', unsafe_allow_html=True)
        st.button("NEET", use_container_width=True)
    r2c1, r2c2 = st.columns([1, 1])
    with r2c1:
        st.markdown('<div class="btn-wbjee"></div>', unsafe_allow_html=True)
        st.button("WBJEE", use_container_width=True)
    with r2c2:
        st.markdown('<div class="btn-adv"></div>', unsafe_allow_html=True)
        st.button("JEE Advanced", use_container_width=True)


# ------------------------------------------
# VIEW: VIEW ALL EXAMS
# ------------------------------------------
elif st.session_state.current_view == "view_all_exams":
    st.button("⬅️ Back to Dashboard", on_click=go_to_dashboard)
    st.markdown('<div style="font-size: 1.5rem; font-weight: 800; color: #111827; margin-bottom: 15px;">All Created Exams</div>', unsafe_allow_html=True)
    
    exams = db_data['exams_list']
    for i in range(0, len(exams), 2):
        cols = st.columns(2)
        render_exam_card(exams[i][0], exams[i][1], cols[0])
        if i + 1 < len(exams):
            render_exam_card(exams[i+1][0], exams[i+1][1], cols[1])


# ------------------------------------------
# VIEW: ANALYSIS (REFACTORED USER CODE)
# ------------------------------------------
elif st.session_state.current_view == "analysis":
    st.button("⬅️ Back to Dashboard", on_click=go_to_dashboard, key="back_from_analysis")
    
    exam_code = st.session_state.analysis_exam_code
    exam_name = st.session_state.analysis_exam_name
    
    st.markdown(f'<div style="font-size: 1.4rem; font-weight: 800; color: #111827; margin-top:10px;">📈 {exam_name} Report</div>', unsafe_allow_html=True)
    st.caption(f"Exam Code: **{exam_code}**")
    
    # Run Database Query
    conn = sqlite3.connect(DB_FILE)
    query = """
        SELECT users.name, results.score, results.total_questions 
        FROM results 
        JOIN users ON results.student_email = users.email 
        WHERE results.exam_code = ?
    """
    df_results = pd.read_sql_query(query, conn, params=(exam_code,))
    conn.close()
    
    if df_results.empty:
        st.warning("No student results found for this exam yet.")
    else:
        # Calculate Metrics
        total_students = len(df_results)
        avg_score = df_results['score'].mean()
        total_qs = df_results['total_questions'].iloc[0] 
        df_results['Performance (%)'] = round((df_results['score'] / df_results['total_questions']) * 100, 2)
        
        # 1. Summary Metrics
        st.write("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Students", f"{total_students}")
        m2.metric("Average Score", f"{avg_score:.1f} / {total_qs}")
        m3.metric("Questions", f"{total_qs}")
        st.write("---")
        
        # 2. Top & Bottom Performers (Cleaned DataFrames)
        col_top, col_bottom = st.columns(2)
        with col_top:
            st.markdown("🏆 **Top 10 Students**")
            top_10 = df_results.nlargest(10, 'score')[['name', 'score', 'Performance (%)']]
            top_10.columns = ["Name", "Score", "%"]
            st.dataframe(top_10, use_container_width=True, hide_index=True)
            
        with col_bottom:
            st.markdown("📉 **Bottom 10 Students**")
            bottom_10 = df_results.nsmallest(10, 'score')[['name', 'score', 'Performance (%)']]
            bottom_10.columns = ["Name", "Score", "%"]
            st.dataframe(bottom_10, use_container_width=True, hide_index=True)
            
        st.write("---")
        
        # 3. Matplotlib Distribution Graph (Refactored to match Light Theme)
        st.markdown("📊 **Score Distribution**")
        fig, ax = plt.subplots(figsize=(8, 3.5))
        fig.patch.set_facecolor('#ffffff') # Match background
        ax.set_facecolor('#f8fafc')
        
        ax.hist(df_results['score'], bins=range(0, int(total_qs)+2), color='#3b82f6', edgecolor='#ffffff', align='left', rwidth=0.8)
        
        ax.set_xlabel('Score Achieved', color='#475569', fontweight='bold')
        ax.set_ylabel('Number of Students', color='#475569', fontweight='bold')
        ax.set_xticks(range(0, int(total_qs)+1))
        ax.tick_params(colors='#475569')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#cbd5e1')
        ax.spines['left'].set_color('#cbd5e1')
        ax.grid(axis='y', linestyle='--', alpha=0.5, color='#cbd5e1')
        
        st.pyplot(fig) 
        
        # 4. Full List
        with st.expander("📋 View All Student Results"):
            full_list = df_results[['name', 'score', 'Performance (%)']].sort_values(by="score", ascending=False)
            full_list.columns = ["Student Name", "Score", "Performance (%)"]
            st.dataframe(full_list, use_container_width=True, hide_index=True)


# ==========================================
# 5. RENDER BOTTOM FIXED NAVIGATION (Always Visible)
# ==========================================
st.markdown("""
<div class="bottom-nav-overlay">
    <div class="nav-item active"><div class="nav-icon">🏠</div><span>Home</span></div>
    <div class="nav-item"><div class="nav-icon">📄</div><span>Questions</span></div>
    <div class="nav-item"><div class="nav-icon">📊</div><span>Results</span></div>
    <div class="nav-item"><div class="nav-icon">👤</div><span>Profile</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="nav-buttons-hider"></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("NavHome", key="t_home"): go_to_dashboard() 
with c2: 
    if st.button("NavQues", key="t_questions"): pass 
with c3: 
    if st.button("NavRes", key="t_results"): pass 
with c4: 
    if st.button("NavProf", key="t_profile"): st.switch_page("pages/05_student_profile.py")