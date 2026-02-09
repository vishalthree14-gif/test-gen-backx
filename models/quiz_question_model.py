from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from bson.objectid import ObjectId

db = Database()

class QuizQuestionCollection:
    collection: Collection = db.get_collection("quiz_question_collection")

    def __init__(self, quiz_id: str, questions: list, status: bool = True):
        self.quiz_id = quiz_id
        self.questions = questions
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        doc = self.__dict__.copy()
        result = self.collection.insert_one(doc)
        return result.inserted_id

    # ================== QUERIES ==================
    @staticmethod
    def find_question(quiz_id):
        return QuizQuestionCollection.collection.find_one({"quiz_id": quiz_id})
    
    @staticmethod
    def find_quiz(user_id, projection=None):
        return QuizQuestionCollection.collection.find_one({"user_id":ObjectId(user_id)}, projection)

    @staticmethod
    def update(query, update_values):
        update_values["updated_at"] = datetime.utcnow()
        return QuizQuestionCollection.collection.update_one(query, {"$set": update_values})

    @staticmethod
    def delete(query):
        return QuizQuestionCollection.collection.delete_one(query)

    @staticmethod
    def find_ques_quizId(quiz_id):
        return QuizQuestionCollection.collection.find_one({"quiz_id": quiz_id})
    
    