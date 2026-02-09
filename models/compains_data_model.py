from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from bson.objectid import ObjectId

db = Database()

class CompainsDataCollection:
    collection: Collection = db.get_collection("compains_data_collection")

    def __init__(self, name: str, compains_id: str, email_address: str, whatsapp_number: str,  status: bool = True):
        self.name = name
        self.compains_id = ObjectId(compains_id)
        self.email_address = email_address
        self.whatsapp_number = whatsapp_number
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        doc = self.__dict__.copy()
        result = self.collection.insert_one(doc)
        return result.inserted_id

    # ================== QUERIES ==================

    @staticmethod
    def find_email(email, compains_id):
        return CompainsDataCollection.collection.find_one({"email_address": email, "compains_id": ObjectId(compains_id)})


    @staticmethod
    def find_members(compains_id):
        return CompainsDataCollection.collection.find({"compains_id": ObjectId(compains_id)})


    @staticmethod
    def update(query, update_values):
        update_values["updated_at"] = datetime.utcnow()
        return CompainsDataCollection.collection.update_one(query, {"$set": update_values})



    @staticmethod
    def delete(query):
        return CompainsDataCollection.collection.delete_one(query)




