import sqlite3

def init_db():
    conn = sqlite3.connect("ExamMate.db")
    cursor = conn.cursor()

    # User er data rakhar jonno table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        password TEXT NOT NULL,
                        category TEXT NOT NULL,
                        gender TEXT
                   )
    """)

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
    conn.close()

# file run korlei sob table aksathe toyri hoya jabe.
init_db()
print("All table created successfully.")