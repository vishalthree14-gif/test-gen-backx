from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from bson.objectid import ObjectId
from enum import Enum

db = Database()


class UserRole(str, Enum):
    MENTOR = "mentor"
    STUDENT = "student"


class QuizUserCollection:
    collection: Collection = db.get_collection("user_collection")

    def __init__(
        self,
        email: str,
        password: str,
        dob: str,
        role: UserRole,
        phone_number: str,
        status: bool = True
    ):
        self.email = email
        self.password = password
        self.dob = dob
        self.role = role.value
        self.phone_number = phone_number
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        return self.collection.insert_one(self.__dict__).inserted_id

    # ========= QUERIES =========
    @staticmethod
    def find_by_email(email):
        return QuizUserCollection.collection.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return QuizUserCollection.collection.find_one(
            {"_id": ObjectId(user_id)}
        )
