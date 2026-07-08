# ExamMate

ExamMate is a Streamlit-based application designed for MCQ practice, user account management, and secure OTP-based sign-up and sign-in.

## Features

- **Streamlit Interface**: Clean and responsive web UI.
- **Sign Up / Sign In**: Create and log in with email and password.
- **OTP Verification**: Email-based OTP verification during registration.
- **Teacher / Student Roles**: Separate dashboards for teachers and students.
- **Profile Page**: Upload profile photos and view personal information.

## File Structure

- `ExamMate.py` - Main landing page and welcome dashboard.
- `pages/01_signup.py` - New user registration and OTP sending logic.
- `pages/02_signin.py` - User login form and navigation flow.
- `pages/03_student_dashboard.py` - Student dashboard page.
- `pages/04_teacher_dashboard.py` - Teacher dashboard page.
- `pages/05_student_profile.py` - Student profile page.
- `pages/06_teacher_profile.py` - Teacher profile page.
- `users.json` - JSON file used as a simple user database.
- `images/` - Folder containing app logos and default profile images.

## Dependencies

This project requires Python and Streamlit:

```bash
pip install streamlit
```

## Run Instructions

```bash
cd ExamMate
streamlit run ExamMate.py
```

## Usage

1. Start the application.
2. Select `Sign Up` to create a new account.
3. Enter your email to receive an OTP during registration.
4. Log in to access your dashboard or profile.

## Notes

- `pages/01_signup.py` includes `sender_email` and `sender_password` settings for sending OTP emails via Gmail.
- For local testing, ensure the `images/` folder and `users.json` file are present.

## License

This project is intended for personal learning and demonstration purposes.
