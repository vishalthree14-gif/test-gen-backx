from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from bson.objectid import ObjectId

db = Database()

class QuizCollection:
    collection: Collection = db.get_collection("quiz_collection")

    def __init__(self, quiz_id: str, user_id: str, topic: str, time_duration: str, difficulty: str, generate_status: bool, status: bool = True):
        self.quiz_id =  quiz_id
        self.user_id = ObjectId(user_id)
        self.topic = topic
        self.time_duration = time_duration
        self.difficulty = difficulty
        self.generate_status = generate_status
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        doc = self.__dict__.copy()
        result = self.collection.insert_one(doc)
        return result.inserted_id

    # ================== QUERIES ==================
    @staticmethod
    def find(quiz_id, projection=None):
        return QuizCollection.collection.find(quiz_id, projection)


    @staticmethod
    def find_topic(topic):
        return QuizCollection.collection.find_one({"topic": topic})


    @staticmethod
    def find_quiz(quiz_id: str):
        data = QuizCollection.collection.find_one({"quiz_id": quiz_id})
        return data


    def get_all_self_quiz(user_id):
        return QuizCollection.collection.find({"user_id": ObjectId(user_id)})


    def get_all_quiz():
        return QuizCollection.collection.find().sort("created_at", -1).limit(10)


    @staticmethod
    def update(query, update_values):
        update_values["updated_at"] = datetime.utcnow()
        return QuizCollection.collection.update_one(query, {"$set": update_values})

    @staticmethod
    def delete(query):
        return QuizCollection.collection.delete_one(query)

    @staticmethod
    def completed_gen(quiz_id):
        return QuizCollection.collection.update_one({"quiz_id": quiz_id}, {"$set": {"generate_status": True}})

