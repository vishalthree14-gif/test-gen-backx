from flask_mail import Message
from flask import current_app

def send_quiz_email_to_students(
    student_emails,   # list of emails
    topic_name,
    duration
):
    msg = Message(
        subject="New Quiz Available 🎯. Quiz-Gen-Ai",
        recipients=student_emails,
        body=f"""Dear Student,

A new quiz has been assigned to you. Please find the details below:

Quiz Name: {topic_name}
Duration: {duration} minutes

Kindly complete the quiz within the given time.

Best of luck!

Regards,
Quiz Management System
"""
    )

    current_app.mail.send(msg)
