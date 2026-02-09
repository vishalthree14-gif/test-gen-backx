from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.collection import Collection
import os

load_dotenv()

MONGOURI = os.getenv("MONGO_URI")
DBNAME = os.getenv("DB_NAME")

class Database:
    def __init__(self, db_name=DBNAME, uri=MONGOURI):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_database(self):
        return self.db

    def get_collection(self, name: str) -> Collection:
        return self.db.get_collection(name)

    def close_connection(self):
        self.client.close()

