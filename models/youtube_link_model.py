
from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from bson.objectid import ObjectId

db = Database()

class YoutubeQuizCollection:
    collection: Collection = db.get_collection("quiz_youtube_collection")

    def __init__(self, quiz_id: str, video_link: list, status: bool = True):
        self.quiz_id = quiz_id
        self.video_link = video_link
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
        return YoutubeQuizCollection.collection.find(query, projection)
    
    @staticmethod
    def find_quiz(user_id, projection=None):
        return YoutubeQuizCollection.collection.find_one({"user_id":ObjectId(user_id)}, projection)

    @staticmethod
    def update(query, update_values):
        update_values["updated_at"] = datetime.utcnow()
        return YoutubeQuizCollection.collection.update_one(query, {"$set": update_values})

    @staticmethod
    def delete(query):
        return YoutubeQuizCollection.collection.delete_one(query)




    @staticmethod
    def find_youtube_quizId(quiz_id):
        return YoutubeQuizCollection.collection.find_one({"quiz_id": quiz_id})
    