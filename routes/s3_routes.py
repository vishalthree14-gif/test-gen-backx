from flask import Blueprint, request, jsonify, g
from controllers.s3_controller import upload_video_controller, see_videos, get_student_video_stream, get_all_videos_controller
from middlewares.auth_middleware import jwt_required, role_required
from models.user_model import UserRole
from dotenv import load_dotenv
import os

load_dotenv()

TOTAL_MENTOR_STORAGE = os.getenv("TOTAL_MENTOR_STORAGE")


upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload-video", methods=["POST"])
@jwt_required
@role_required(UserRole.MENTOR)
def upload_video():

    if "video" not in request.files:
        return jsonify({"message": "No video file provided"}), 400

    file = request.files["video"]


    file.seek(0, 2)
    size_bytes = file.tell()
    file.seek(0)


    if size_bytes > 300 * 1024 * 1024:
        return jsonify({"message": "File too large. Max 300MB allowed"}), 400

    user_id = g.user_id

    return upload_video_controller(file, size_bytes, user_id)


@upload_bp.route("/view-video", methods=["GET"])
@jwt_required
@role_required(UserRole.MENTOR)
def get_see_vidoes():
    
    user_id = g.user_id
    
    return see_videos(user_id)


@upload_bp.route("/all-videos", methods=["GET"])
@jwt_required
def get_all_videos():
    return get_all_videos_controller()


@upload_bp.route("/video-stream/<video_id>", methods=["GET"])
@jwt_required
def stream_vid(video_id):
    return get_student_video_stream(video_id)


