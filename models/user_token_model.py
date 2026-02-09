from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from bson.objectid import ObjectId
from enum import Enum


db = Database()


class UserTokenCollection:
    collection: Collection = db.get_collection("user_token_collection")

    def __init__(
        self,
        user_id: str,
        tokens: str,
        status: bool = True
    ):
        self.user_id = user_id
        self.tokens = tokens
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


    def save(self):
        return self.collection.insert_one(self.__dict__).inserted_id


    # # ========= QUERIES =========
    @staticmethod
    def find_user_token(user_id):
        curr_tokens = UserTokenCollection.collection.find_one(
            {"user_id": user_id},
            {"_id": 0, "tokens": 1}
            )

        return curr_tokens.get("tokens", 0) if curr_tokens else 0

    @staticmethod
    def spend_token(user_id, amount):

        return UserTokenCollection.collection.update_one(
            
            {
            "user_id": user_id,
            # "token": {"$gte": amount}
            "tokens": {"$gte": amount}   # ✅ correct field


            },
            {
                "$inc": {"tokens": -amount},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )


    @staticmethod
    def purchase_token(user_id, new_token):

        return UserTokenCollection.collection.update_one(
            
            {"user_id": user_id},

            {"$set": {
                "tokens": new_token,
                "updated_at": datetime.utcnow()
                },
                "$setOnInsert":{
                    "user_id": user_id,
                    "status": True,
                    "created_at": datetime.utcnow()
                }
            },
            upsert=True
        )



