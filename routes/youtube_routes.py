from flask import Blueprint
from controllers.youtube_controller import search_youtube_controller
from middlewares.auth_middleware import jwt_required, role_required
from models.user_model import UserRole

youtube_bp = Blueprint("youtube_routes", __name__)

@youtube_bp.route("/youtube-search/<quiz_id>", methods=["GET"])
@jwt_required
@role_required(UserRole.MENTOR)
def search_youtube(quiz_id):

    return search_youtube_controller(quiz_id)


