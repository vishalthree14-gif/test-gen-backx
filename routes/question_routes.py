from flask import Blueprint, request, jsonify
from controllers.question_controller import gen_quiz
from middlewares.auth_middleware import jwt_required, role_required
from models.user_model import UserRole


question_bp = Blueprint("question_routes", __name__)

@question_bp.route("/generate-question/<quiz_id>", methods=["GET"])
@jwt_required
@role_required(UserRole.MENTOR)
def generate_quiz_api(quiz_id):

    quiz = gen_quiz(quiz_id)

    if not quiz:
        return jsonify({"message":"quiz question already exists"})

    return jsonify(quiz), 200



