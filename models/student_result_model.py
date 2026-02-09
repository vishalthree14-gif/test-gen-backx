from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from bson.objectid import ObjectId

db = Database()

class StudentResultCollection:
    collection: Collection = db.get_collection("student_result_collection")

    def __init__(self, student_id: str, marks: int, quiz_id: str):
        self.student_id = student_id
        self.marks = marks
        self.quiz_id = quiz_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        doc = self.__dict__.copy()
        result = self.collection.insert_one(doc)
        return result.inserted_id

    # ================== QUERIES ==================
