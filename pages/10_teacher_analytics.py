import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Check if user is logged in and is a teacher
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("teachers"):
    if st.session_state.user_catagory != "Teacher":
        st.error("**Access Denied!** This page is only for Teachers.")
        st.stop()
    
    user_name = st.session_state.get("user_name", "Teacher")
    user_email = st.session_state.get("user_email", "teacher@email.com")
    
    # Page setup
    st.set_page_config(page_title="Teacher Analytics", page_icon="📊", layout="wide")
    
    st.title(f"📊 Class Analytics - {user_name}")
    st.markdown("Monitor student performance and exam statistics")
    
    # Database connection
    conn = sqlite3.connect("ExamMate.db")
    cursor = conn.cursor()
    
    # Fetch all exams created by this teacher
    cursor.execute('''
        SELECT exam_code, exam_name, timer_minutes 
        FROM exams 
        WHERE teacher_email = ? 
        ORDER BY exam_name
    ''', (user_email,))
    
    teacher_exams = cursor.fetchall()
    
    if not teacher_exams:
        st.info("📝 You haven't created any exams yet. Create your first exam to see analytics!")
        conn.close()
        st.stop()
    
    # Fetch all results for teacher's exams
    exam_codes = [exam[0] for exam in teacher_exams]
    placeholders = ','.join(['?' for _ in exam_codes])
    
    cursor.execute(f'''
        SELECT r.student_email, r.exam_code, r.exam_name, r.score, r.total_questions, r.date_taken
        FROM results r
        WHERE r.exam_code IN ({placeholders})
        ORDER BY r.date_taken DESC
    ''', exam_codes)
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        st.info("🎯 No students have taken your exams yet. Share the exam codes with your students!")
        st.stop()
    
    # Convert to DataFrame
    df = pd.DataFrame(results, columns=['student_email', 'exam_code', 'exam_name', 'score', 'total_questions', 'date_taken'])
    df['date_taken'] = pd.to_datetime(df['date_taken'])
    df['percentage'] = (df['score'] / df['total_questions'] * 100).round(2)
    
    # Key Metrics
    st.subheader("📈 Class Overview Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_students = df['student_email'].nunique()
        st.metric("Total Students", total_students)
    
    with col2:
        total_attempts = len(df)
        st.metric("Total Attempts", total_attempts)
    
    with col3:
        class_avg = df['percentage'].mean()
        st.metric("Class Average", f"{class_avg:.1f}%")
    
    with col4:
        highest_score = df['percentage'].max()
        st.metric("Highest Score", f"{highest_score:.1f}%")
    
    with col5:
        total_exams = df['exam_code'].nunique()
        st.metric("Active Exams", total_exams)
    
    st.divider()
    
    # Exam-wise Performance
    st.subheader("📝 Exam-wise Performance")
    
    exam_stats = df.groupby('exam_name').agg({
        'percentage': ['mean', 'max', 'min', 'count'],
        'student_email': 'nunique'
    }).round(2)
    
    exam_stats.columns = ['Average %', 'Highest %', 'Lowest %', 'Total Attempts', 'Unique Students']
    exam_stats = exam_stats.sort_values('Average %', ascending=False)
    
    st.dataframe(exam_stats, use_container_width=True)
    
    # Exam performance chart
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    exam_avg = df.groupby('exam_name')['percentage'].mean().sort_values(ascending=False)
    exam_avg.plot(kind='bar', ax=ax1, color='#1ea64d')
    ax1.set_xlabel('Exam Name', fontsize=12)
    ax1.set_ylabel('Average Score (%)', fontsize=12)
    ax1.set_title('Class Performance by Exam', fontsize=14, fontweight='bold')
    ax1.axhline(y=class_avg, color='red', linestyle='--', alpha=0.7, label=f'Class Avg: {class_avg:.1f}%')
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    
    st.pyplot(fig1)
    
    st.divider()
    
    # Student Performance Leaderboard
    st.subheader("🏆 Student Performance Leaderboard")
    
    student_stats = df.groupby('student_email').agg({
        'percentage': ['mean', 'max', 'count'],
        'score': 'sum'
    }).round(2)
    
    student_stats.columns = ['Average %', 'Best %', 'Exams Taken', 'Total Score']
    student_stats = student_stats.sort_values('Average %', ascending=False)
    student_stats = student_stats.head(15)  # Top 15 students
    
    st.dataframe(student_stats, use_container_width=True)
    
    # Student performance distribution
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    avg_scores = df.groupby('student_email')['percentage'].mean()
    ax2.hist(avg_scores, bins=10, color='#1ea64d', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Average Score (%)', fontsize=12)
    ax2.set_ylabel('Number of Students', fontsize=12)
    ax2.set_title('Distribution of Student Average Scores', fontsize=14, fontweight='bold')
    ax2.axvline(x=class_avg, color='red', linestyle='--', alpha=0.7, label=f'Class Avg: {class_avg:.1f}%')
    ax2.legend()
    
    st.pyplot(fig2)
    
    st.divider()
    
    # Individual Student Analysis
    st.subheader("👤 Individual Student Analysis")
    
    # Student selector
    selected_student = st.selectbox(
        "Select a student to view detailed performance:",
        options=df['student_email'].unique(),
        key="student_selector"
    )
    
    if selected_student:
        student_data = df[df['student_email'] == selected_student].sort_values('date_taken')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Student Average", f"{student_data['percentage'].mean():.1f}%")
        with col2:
            st.metric("Best Score", f"{student_data['percentage'].max():.1f}%")
        with col3:
            st.metric("Exams Taken", len(student_data))
        
        # Student progress chart
        fig3, ax3 = plt.subplots(figsize=(12, 4))
        ax3.plot(student_data['date_taken'], student_data['percentage'], 
                marker='o', linewidth=2, markersize=8, color='#1ea64d')
        ax3.fill_between(student_data['date_taken'], student_data['percentage'], alpha=0.3, color='#1ea64d')
        ax3.set_xlabel('Date', fontsize=12)
        ax3.set_ylabel('Score (%)', fontsize=12)
        ax3.set_title(f'Performance Progress: {selected_student}', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        ax3.axhline(y=class_avg, color='red', linestyle='--', alpha=0.7, label=f'Class Avg: {class_avg:.1f}%')
        ax3.legend()
        
        st.pyplot(fig3)
        
        # Student's exam history
        st.write(f"**Exam History for {selected_student}:**")
        student_history = student_data[['date_taken', 'exam_name', 'score', 'total_questions', 'percentage']].copy()
        student_history['date_taken'] = student_history['date_taken'].dt.strftime('%Y-%m-%d %H:%M')
        student_history.columns = ['Date', 'Exam Name', 'Score', 'Total Questions', 'Percentage']
        st.dataframe(student_history, use_container_width=True)
    
    st.divider()
    
    # Performance Insights
    st.subheader("💡 Teaching Insights")
    
    # Identify struggling students
    struggling_students = df.groupby('student_email')['percentage'].mean()
    struggling_students = struggling_students[struggling_students < class_avg - 10]
    
    if not struggling_students.empty:
        st.warning(f"⚠️ {len(struggling_students)} students are performing below class average:")
        for student, score in struggling_students.head(5).items():
            st.write(f"• {student}: {score:.1f}%")
    else:
        st.success("✅ All students are performing close to or above class average!")
    
    # Identify easy vs difficult exams
    exam_difficulty = df.groupby('exam_name')['percentage'].mean().sort_values()
    easiest_exam = exam_difficulty.idxmax()
    hardest_exam = exam_difficulty.idxmin()
    
    st.info(f"📊 Easiest exam: {easiest_exam} ({exam_difficulty.max():.1f}%) | Hardest exam: {hardest_exam} ({exam_difficulty.min():.1f}%)")
    
    # Recent activity
    recent_activity = df[df['date_taken'] > (datetime.now() - pd.Timedelta(days=7))]
    if not recent_activity.empty:
        st.success(f"📈 {len(recent_activity)} exam attempts in the last 7 days")
    
    # Back button
    st.divider()
    if st.button("← Back to Dashboard"):
        st.switch_page("pages/04_teacher_dashboard.py")

else:
    st.warning("Please, sign-in first.")
