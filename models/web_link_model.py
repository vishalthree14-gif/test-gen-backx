
from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from bson.objectid import ObjectId

db = Database()

class WebQuizCollection:
    collection: Collection = db.get_collection("quiz_website_collection")

    def __init__(self, quiz_id: str, web_links: list, status: bool = True):
        self.web_links = web_links
        self.quiz_id = quiz_id
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        doc = self.__dict__.copy()
        result = self.collection.insert_one(doc)
        return result.inserted_id

    # ================== QUERIES ==================
    @staticmethod
    def find(query, projection=None):
        return WebQuizCollection.collection.find(query, projection)
    
    @staticmethod
    def find_quiz(user_id, projection=None):
        return WebQuizCollection.collection.find_one({"user_id":ObjectId(user_id)}, projection)

    @staticmethod
    def update(query, update_values):
        update_values["updated_at"] = datetime.utcnow()
        return WebQuizCollection.collection.update_one(query, {"$set": update_values})

    @staticmethod
    def delete(query):
        return WebQuizCollection.collection.delete_one(query)


    @staticmethod
    def find_blog_quizId(quiz_id):
        return WebQuizCollection.collection.find_one({"quiz_id": quiz_id})
    

