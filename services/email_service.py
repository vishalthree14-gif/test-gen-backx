import threading
import logging

from flask_mail import Message
from flask import current_app


logger = logging.getLogger(__name__)

def send_quiz_email_to_students(student_emails, topic_name, duration):
    if not student_emails:
        logger.warning("No student emails provided - skipping")
        return

    def send_in_background():
        try:
            msg = Message(
                subject="New Quiz Available 🎯 - Quiz-Gen-Ai",
                recipients=student_emails,
                body=...  # your body
            )
            current_app.mail.send(msg)
            logger.info(f"Email sent successfully to {len(student_emails)} students | {topic_name}")
        except Exception as e:
            logger.error(f"Background email failed: {str(e)}", exc_info=True)

    # Fire and forget
    thread = threading.Thread(target=send_in_background)
    thread.daemon = True  # optional: don't block shutdown
    thread.start()

    logger.info(f"Started background email send for {len(student_emails)} students")


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
