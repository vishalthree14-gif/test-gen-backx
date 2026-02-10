import logging
from flask_mail import Message
from flask import current_app

logger = logging.getLogger(__name__)

def send_quiz_email_to_students(
    student_emails,
    topic_name,
    duration
):
    if not student_emails:
        print("[EMAIL] No students to notify - skipping")
        logger.warning("No student emails provided")
        return

    msg = Message(
        subject="New Quiz Available 🎯 - Quiz-Gen-Ai",
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

    try:
        print(f"[EMAIL] Attempting to send quiz notification → {len(student_emails)} students | {topic_name}")
        logger.info(f"Sending quiz email to {len(student_emails)} students - {topic_name}")

        current_app.mail.send(msg)

        print(f"[EMAIL] SUCCESS: Quiz notification sent to {len(student_emails)} students")
        logger.info(f"Quiz email sent successfully - {topic_name}")

    except Exception as e:
        error_msg = f"[EMAIL] FAILED: {str(e)} | topic: {topic_name} | recipients: {len(student_emails)}"
        print(error_msg)
        logger.error(error_msg, exc_info=True)



# from flask_mail import Message
# from flask import current_app

# def send_quiz_email_to_students(
#     student_emails,   # list of emails
#     topic_name,
#     duration
# ):
#     msg = Message(
#         subject="New Quiz Available 🎯. Quiz-Gen-Ai",
#         recipients=student_emails,
#         body=f"""Dear Student,

# A new quiz has been assigned to you. Please find the details below:

# Quiz Name: {topic_name}
# Duration: {duration} minutes

# Kindly complete the quiz within the given time.

# Best of luck!

# Regards,
# Quiz Management System
# """
#     )

#     current_app.mail.send(msg)
