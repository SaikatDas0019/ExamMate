import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Check if user is logged in and is a student
if st.session_state.get("logged_in") or st.session_state.get("is_logged_in") or st.session_state.get("students"):
    if st.session_state.user_catagory != "Student":
        st.error("**Access Denied!** This page is only for Students.")
        st.stop()
    
    user_name = st.session_state.get("user_name", "Student")
    user_email = st.session_state.get("user_email", "student@email.com")
    
    # Page setup
    st.set_page_config(page_title="Student Analytics", page_icon="📊", layout="wide")
    
    st.title(f"📊 Performance Analytics - {user_name}")
    st.markdown("Track your progress and identify areas for improvement")
    
    # Database connection
    conn = sqlite3.connect("ExamMate.db")
    cursor = conn.cursor()
    
    # Fetch student's exam results
    cursor.execute('''
        SELECT exam_code, exam_name, score, total_questions, date_taken 
        FROM results 
        WHERE student_email = ? 
        ORDER BY date_taken DESC
    ''', (user_email,))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        st.info("🎯 You haven't taken any exams yet. Start practicing to see your analytics here!")
        st.stop()
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(results, columns=['exam_code', 'exam_name', 'score', 'total_questions', 'date_taken'])
    df['date_taken'] = pd.to_datetime(df['date_taken'])
    df['percentage'] = (df['score'] / df['total_questions'] * 100).round(2)
    
    # Key Metrics
    st.subheader("📈 Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_exams = len(df)
        st.metric("Total Exams", total_exams)
    
    with col2:
        avg_score = df['percentage'].mean()
        st.metric("Average Score", f"{avg_score:.1f}%")
    
    with col3:
        best_score = df['percentage'].max()
        st.metric("Best Score", f"{best_score:.1f}%")
    
    with col4:
        total_questions = df['total_questions'].sum()
        st.metric("Total Questions", total_questions)
    
    st.divider()
    
    # Score Trend Chart
    st.subheader("📉 Score Progress Over Time")
    
    # Sort by date for the chart
    df_sorted = df.sort_values('date_taken')
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df_sorted['date_taken'], df_sorted['percentage'], 
            marker='o', linewidth=2, markersize=8, color='#1ea64d')
    ax.fill_between(df_sorted['date_taken'], df_sorted['percentage'], alpha=0.3, color='#1ea64d')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Score (%)', fontsize=12)
    ax.set_title('Your Performance Trend', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    
    # Add average line
    ax.axhline(y=avg_score, color='red', linestyle='--', alpha=0.7, label=f'Average: {avg_score:.1f}%')
    ax.legend()
    
    st.pyplot(fig)
    
    st.divider()
    
    # Subject-wise Performance (based on exam names)
    st.subheader("📚 Subject-wise Performance")
    
    # Extract subject from exam name (simple keyword matching)
    def extract_subject(exam_name):
        exam_lower = exam_name.lower()
        if 'physics' in exam_lower or 'phy' in exam_lower:
            return 'Physics'
        elif 'chemistry' in exam_lower or 'chem' in exam_lower:
            return 'Chemistry'
        elif 'mathematics' in exam_lower or 'math' in exam_lower:
            return 'Mathematics'
        elif 'biology' in exam_lower or 'bio' in exam_lower:
            return 'Biology'
        else:
            return 'General'
    
    df['subject'] = df['exam_name'].apply(extract_subject)
    
    if df['subject'].nunique() > 1:
        subject_performance = df.groupby('subject').agg({
            'percentage': ['mean', 'count'],
            'score': 'sum'
        }).round(2)
        subject_performance.columns = ['Average %', 'Exam Count', 'Total Score']
        
        st.dataframe(subject_performance, use_container_width=True)
        
        # Subject performance chart
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        subject_avg = df.groupby('subject')['percentage'].mean().sort_values(ascending=False)
        colors = ['#1ea64d' if x >= avg_score else '#ff6b6b' for x in subject_avg]
        subject_avg.plot(kind='bar', ax=ax2, color=colors)
        ax2.set_xlabel('Subject', fontsize=12)
        ax2.set_ylabel('Average Score (%)', fontsize=12)
        ax2.set_title('Average Performance by Subject', fontsize=14, fontweight='bold')
        ax2.axhline(y=avg_score, color='blue', linestyle='--', alpha=0.5, label=f'Overall Avg: {avg_score:.1f}%')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)
        
        st.pyplot(fig2)
    else:
        st.info("Take exams in different subjects to see subject-wise performance analysis.")
    
    st.divider()
    
    # Recent Exam History
    st.subheader("📋 Recent Exam History")
    
    # Format for display
    display_df = df.copy()
    display_df['date_taken'] = display_df['date_taken'].dt.strftime('%Y-%m-%d %H:%M')
    display_df = display_df[['date_taken', 'exam_name', 'score', 'total_questions', 'percentage']]
    display_df.columns = ['Date', 'Exam Name', 'Score', 'Total Questions', 'Percentage']
    
    st.dataframe(display_df.head(10), use_container_width=True)
    
    # Performance Insights
    st.divider()
    st.subheader("💡 Performance Insights")
    
    if len(df) >= 3:
        # Calculate trend
        recent_scores = df.head(3)['percentage'].values
        if recent_scores[0] > recent_scores[-1]:
            st.success("🎉 Your recent performance shows an upward trend! Keep up the great work!")
        elif recent_scores[0] < recent_scores[-1]:
            st.warning("📈 Your recent scores show room for improvement. Focus on weak areas.")
        else:
            st.info("📊 Your performance has been consistent. Try to push for higher scores!")
        
        # Identify best and worst performing subjects
        if df['subject'].nunique() > 1:
            best_subject = df.groupby('subject')['percentage'].mean().idxmax()
            worst_subject = df.groupby('subject')['percentage'].mean().idxmin()
            st.info(f"🏆 Strongest subject: {best_subject} | 📚 Focus area: {worst_subject}")
    else:
        st.info("Take at least 3 exams to see detailed performance insights and trends.")
    
    # Back button
    st.divider()
    if st.button("← Back to Dashboard"):
        st.switch_page("pages/03_student_dashboard.py")

else:
    st.warning("Please, sign-in first.")
