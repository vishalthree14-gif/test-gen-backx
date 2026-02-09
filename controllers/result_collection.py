from models.student_result_model import StudentResultCollection
from datetime import datetime
from flask import g

def create_student_result(marks, quiz_id):
    student_id = g.user_id

    db_doc = StudentResultCollection(

        student_id=student_id,
        marks= marks,
        quiz_id=quiz_id
    )

    return db_doc.save()


