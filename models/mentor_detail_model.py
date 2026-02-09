from datetime import datetime
from models.db import Database
from pymongo.collection import Collection
from datetime import datetime

db = Database()

class MentorDetailCollection:
    collection: Collection = db.get_collection("mentor_detail_collection")

    def __init__(
        self,
        user_id: str,
        s3_storage: int,
        quiz_number: str,
        url_list: list,
        status: bool = True
    ):
        self.user_id = user_id
        self.s3_storage = s3_storage
        self.quiz_number = quiz_number
        self.url_list = url_list
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


    def save(self):
        return self.collection.insert_one(self.__dict__).inserted_id


    @staticmethod
    def update_storage(user_id, total_size, url):
        return MentorDetailCollection.collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "s3_storage": total_size,
                    "updated_at": datetime.utcnow()
                },
                "$push": {
                    "url_list": url
                },
                "$setOnInsert": {
                    "user_id": user_id,
                    "created_at": datetime.utcnow(),
                    "status": True
                }
            },
            upsert=True
        )


    @staticmethod
    def find_user_storage(user_id):

        data = MentorDetailCollection.collection.find_one({"user_id": user_id})

        if not data:
            return 0

        return data.get("s3_storage", 0)


    @staticmethod
    def update_quiz_number(user_id, quiz_number):
        
        return MentorDetailCollection.collection.update_one(
            {"user_id": user_id},
            {"$set": {"quiz_number": quiz_number}}
        )


    @staticmethod
    def find_quiz_number(user_id):

        resp = MentorDetailCollection.collection.find_one({"user_id": user_id})
        
        if not resp:
            return 0
        
        return resp.get("quiz_number", 0)


    @staticmethod
    def view_self_videos(user_id):
        videos_cursor  = MentorDetailCollection.collection.find(
            {"user_id": user_id},
            {"_id": 0, "url_list": 1}  # projection (important)
        )

        videos = list(videos_cursor)

        return videos


    @staticmethod
    def find_video_key(video_id):

        doc = MentorDetailCollection.collection.find_one(

            {"url_list.video_id": video_id},
            {"url_list.$": 1}
            )

        if not doc or "url_list" not in doc:
            return None

        return doc["url_list"][0]["video_key"]

    @staticmethod
    def get_all_videos():
        docs = MentorDetailCollection.collection.find(
            {"url_list": {"$exists": True, "$ne": []}},
            {"_id": 0, "url_list": 1}
        )
        all_videos = []
        for doc in docs:
            for video in doc.get("url_list", []):
                all_videos.append({
                    "video_id": video.get("video_id"),
                    "thumbnail_url": video.get("thumbnail_url"),
                    "size": video.get("size"),
                    "uploaded_at": video.get("uploaded_at"),
                })
        return all_videos
    


