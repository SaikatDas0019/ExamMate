import json
import sqlite3
import random
import os
import sys

# Configuration
DB_FILE = "ExamMate.db"
JSON_FILE = "exam_data.json"

def generate_unique_code(cursor):
    """
    Generates a unique alphanumeric exam code (e.g., EXAM-7492).
    Queries the database to ensure the code does not already exist.
    """
    while True:
        code = f"EXAM-{random.randint(1000, 9999)}"
        cursor.execute("SELECT 1 FROM exams WHERE exam_code = ?", (code,))
        # If fetchone() returns None, the code is unique
        if cursor.fetchone() is None:
            return code

def upload_exam_data():
    """Reads JSON data and safely inserts it into the SQLite database."""
    
    # 1. Verify JSON file exists
    if not os.path.exists(JSON_FILE):
        print(f"❌ Error: Could not find '{JSON_FILE}'. Please ensure the file exists in the same directory.")
        sys.exit(1)

    # 2. Load and parse JSON Data
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            exam_data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error reading JSON file: {e}")
        sys.exit(1)

    # 3. Database Insertion with Transaction Safety
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Auto-generate a unique exam code
        exam_code = generate_unique_code(cursor)

        # Insert main exam details into the 'exams' table
        cursor.execute(
            """
            INSERT INTO exams (exam_code, exam_name, teacher_email, timer_minutes) 
            VALUES (?, ?, ?, ?)
            """,
            (exam_code, exam_data['exam_name'], exam_data['teacher_email'], exam_data['timer_minutes'])
        )

        # Retrieve questions array from JSON
        questions = exam_data.get('questions', [])
        
        # Insert each question into the 'questions' table
        for q in questions:
            cursor.execute(
                """
                INSERT INTO questions 
                (exam_code, question_text, option_a, option_b, option_c, option_d, correct_option) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    exam_code,
                    q['question_text'],
                    q['option_a'],
                    q['option_b'],
                    q['option_c'],
                    q['option_d'],
                    q['correct_option'].strip().upper()  # Normalize to uppercase A, B, C, D
                )
            )

        # Commit the transaction if everything succeeds
        conn.commit()
        
        print("\n" + "="*40)
        print("✅ SUCCESS: Mock Exam Uploaded!")
        print("="*40)
        print(f"📌 Exam Name:  {exam_data['exam_name']}")
        print(f"🔑 Exam Code:  {exam_code}")
        print(f"📚 Questions:  {len(questions)} added")
        print("="*40 + "\n")

    except KeyError as e:
        print(f"\n❌ JSON Structure Error: Missing expected key {e}")
        print("Please ensure your JSON matches the required schema.")
    except sqlite3.Error as e:
        # If any database error occurs, rollback the transaction to prevent partial inserts
        if 'conn' in locals():
            conn.rollback()
        print(f"\n❌ SQLite Database Error: {e}")
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"\n❌ An unexpected error occurred: {e}")
    finally:
        # Ensure the database connection is safely closed
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    upload_exam_data()