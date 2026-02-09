from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from bson.objectid import ObjectId
from enum import Enum

db = Database()


class CompainsCollection:
    collection: Collection = db.get_collection("compains_collection")

    def __init__(self, user_id: str, name: str,  status: bool = True):
        self.user_id = ObjectId(user_id)
        self.name = name
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
        return CompainsCollection.collection.find(quiz_id, projection)


    @staticmethod
    def find_compains(name, user_id):
        return CompainsCollection.collection.find_one({"name": name, "user_id": ObjectId(user_id)})



    @staticmethod
    def find_user_compains(user_id):
        data = CompainsCollection.collection.find({"user_id": ObjectId(user_id)})

        return data




    @staticmethod
    def update(query, update_values):
        update_values["updated_at"] = datetime.utcnow()
        return CompainsCollection.collection.update_one(query, {"$set": update_values})

    @staticmethod
    def delete(query):
        return CompainsCollection.collection.delete_one(query)




