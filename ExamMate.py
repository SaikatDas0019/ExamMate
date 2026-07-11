import streamlit as st

st.set_page_config(page_title='ExamMate', page_icon="📝", layout="centered")

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }
    body {
        background-color: #05070f;
        color: #e8eef8;
    }
    .css-1d391kg {
        background-color: transparent;
    }
    .stApp {
        background: linear-gradient(180deg, #08101f 0%, #04060d 100%);
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    .hero-card {
        background: rgba(17, 29, 52, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 26px;
        padding: 30px;
        margin-bottom: 1.8rem;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.25);
    }
    .hero-card h1 {
        margin: 0 0 0.35rem 0;
        color: #f5f9ff;
        font-size: 2.6rem;
        letter-spacing: -0.03em;
    }
    .hero-card p {
        margin: 0;
        color: #c8d3ea;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    .button-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 1.25rem;
        margin-bottom: 1.8rem;
    }
    .button-card h2 {
        margin: 0 0 1rem 0;
        color: #f2f7ff;
        font-size: 1.4rem;
    }
    .stButton button {
        width: 100%;
        background-color: #1ea64d !important;
        color: #ffffff !important;
        border-radius: 999px !important;
        padding: 0.95rem 1.2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 18px 28px rgba(30, 166, 77, 0.22);
        transition: transform 150ms ease, background-color 150ms ease, box-shadow 150ms ease;
    }
    .stButton button:hover {
        background-color: #22c05d !important;
        transform: translateY(-1px);
        box-shadow: 0 22px 30px rgba(34, 192, 93, 0.28);
    }
    .stButton button:focus-visible {
        outline: 2px solid rgba(34, 192, 93, 0.65) !important;
        outline-offset: 2px;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.4rem;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        color: #e8eef8;
    }
    .feature-card h3 {
        margin: 0 0 0.55rem 0;
        font-size: 1.05rem;
        color: #f4fbff;
    }
    .feature-card p {
        margin: 0;
        color: #a9b7d8;
        line-height: 1.65;
        font-size: 0.98rem;
    }
    .divider {
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin: 1.8rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <h1>ExamMate</h1>
        <p>Best app for MCQ practice of any exam.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="button-card">
        <h2>✅ Sign-Up or Sign-In</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Sign Up", use_container_width=True):
        st.switch_page("pages/01_signup.py")
with col2:
    if st.button("Sign In", use_container_width=True):
        st.switch_page("pages/02_signin.py")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero-card">
        <h2 style="margin-bottom:1rem; color:#d7f1d6;">🟢 Features</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <h3>Time Management</h3>
                <p>Testing with timers like the real thing to build exam rhythm and pacing.</p>
            </div>
            <div class="feature-card">
                <h3>Customize Exam</h3>
                <p>Teachers can set their own question style and personalize practice sessions.</p>
            </div>
            <div class="feature-card">
                <h3>Perfect Prep</h3>
                <p>Unlimited MCQ practice for steady improvement and exam readiness.</p>
            </div>
            <div class="feature-card">
                <h3>Instant Result</h3>
                <p>See correct answers and final score immediately when the test ends.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
