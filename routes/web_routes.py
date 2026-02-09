from flask import Blueprint
from controllers.web_controller import search_web_controller
from middlewares.auth_middleware import jwt_required, role_required
from models.user_model import UserRole

web_bp = Blueprint("web_routes", __name__)

# Decorator should be above the function definition
@web_bp.route("/search-web/<quiz_id>", methods=["GET"])
@jwt_required
@role_required(UserRole.MENTOR)
def search_web(quiz_id):
    return search_web_controller(quiz_id)

