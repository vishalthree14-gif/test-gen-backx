import tempfile
from services.s3_service import upload_video, generate_signed_url
from services.thumb_service import generate_thumbnail
from datetime import datetime
from models.mentor_detail_model import MentorDetailCollection
import uuid
import os
from flask import jsonify
from models.user_token_model import UserTokenCollection
import math

TOTAL_MENTOR_STORAGE = int(os.getenv("TOTAL_MENTOR_STORAGE"))  # BYTES
STORAGE_TOKEN_PER_MB = int(os.getenv("STORAGE_TOKEN_PER_MB"))


def upload_video_controller(file, size_bytes, user_id):

    video_id = uuid.uuid4().hex
    video_key = f"videos/user_{user_id}/{video_id}_{file.filename}"
    thumb_key = f"thumbnails/user_{user_id}/{video_id}.jpg"

    curr_storage = MentorDetailCollection.find_user_storage(user_id)
    new_total_storage = curr_storage + size_bytes

    tokens_charged = 0

    # 🔐 STORAGE CHECK
    if new_total_storage > TOTAL_MENTOR_STORAGE:

        extra_bytes = new_total_storage - TOTAL_MENTOR_STORAGE

        # ✅ 1 MB = 1 token
        tokens_required = max(
            1,
            math.ceil(extra_bytes / (1024 * 1024))
        )

        user_tokens = int(UserTokenCollection.find_user_token(user_id))

        if user_tokens < tokens_required:
            return jsonify({
                "error": "Storage limit exceeded",
                "extra_mb": round(extra_bytes / (1024 * 1024), 2),
                "tokens_required": tokens_required
            }), 400

        # deduct tokens BEFORE upload
        UserTokenCollection.spend_token(user_id, tokens_required)
        tokens_charged = tokens_required

    # save temp video
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        file.save(tmp_video.name)
        temp_video_path = tmp_video.name

    # upload video
    with open(temp_video_path, "rb") as v:
        video_url = upload_video(v, video_key, file.content_type)

    # generate & upload thumbnail
    temp_thumb_path = temp_video_path.replace(".mp4", ".jpg")
    generate_thumbnail(temp_video_path, temp_thumb_path)

    with open(temp_thumb_path, "rb") as t:
        thumb_url = upload_video(t, thumb_key, "image/jpeg")

    os.remove(temp_video_path)
    os.remove(temp_thumb_path)

    # update DB
    MentorDetailCollection.update_storage(
        user_id,
        new_total_storage,
        {
            "video_id": video_id,
            "video_key": video_key,
            "video_url": video_url,
            "thumbnail_url": thumb_url,
            "size": size_bytes,
            "uploaded_at": datetime.utcnow()
        }
    )

    return jsonify({
        "message": "Video uploaded successfully",
        "video_url": video_url,
        "thumbnail_url": thumb_url,
        "tokens_charged": tokens_charged,
        "used_mb": round(new_total_storage / (1024 * 1024), 2)
    })

def see_videos(user_id):

    res = MentorDetailCollection.view_self_videos(user_id)

    return res


def get_all_videos_controller():
    videos = MentorDetailCollection.get_all_videos()
    return jsonify({"videos": videos})


def get_student_video_stream(video_id):

    video_key = MentorDetailCollection.find_video_key(video_id)

    if not video_key:
        return jsonify({"error": "Video not found"}), 404

    # 2️⃣ generate signed url
    signed_url = generate_signed_url(video_key, expires_in=3600)

    return jsonify({
        "stream_url": signed_url
    })

