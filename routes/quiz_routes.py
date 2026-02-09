from controllers.quiz_controller import create_quiz, get_quiz, get_id_quiz, get_self_quiz, completed_generated_quiz
from flask import Blueprint, request, jsonify
from middlewares.auth_middleware import jwt_required, role_required
from models.user_model import UserRole

quiz_bp = Blueprint("quiz_route", __name__)

@quiz_bp.route("/create-quiz", methods=["POST"])
@jwt_required
@role_required(UserRole.MENTOR)
def create():
    data = request.json

    topic = data.get("topic")
    time_duration = data.get("time_duration")
    difficulty = data.get("difficulty")

    quiz_id = create_quiz(topic, time_duration, difficulty)

    if not quiz_id:
        return jsonify({"message": "quiz already exists"}), 404

    return jsonify({"message": "quiz created sucessfuly", "quiz_id": quiz_id}), 200


@quiz_bp.route("/get-all-quizs", methods=["GET"])
@jwt_required
def all_quiz():
    return get_quiz()


@quiz_bp.route("/only-self-quizs", methods=["GET"])
@jwt_required
@role_required(UserRole.MENTOR)
def self_quiz():
    return get_self_quiz()

@quiz_bp.route("/quiz/<quiz_id>", methods=["GET"])
@jwt_required
def get_quiz_id(quiz_id):
    data = get_id_quiz(quiz_id)
    return jsonify(data), 200


@quiz_bp.route("/quiz-gen-complete/<quiz_id>", methods=["GET"])
@jwt_required
def completed_generated(quiz_id):

    result = completed_generated_quiz(quiz_id)

    if result.matched_count == 0:
        return jsonify({
            "success": False,
            "message": "Quiz not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Quiz generation marked as completed",
        "modified": result.modified_count
    }), 200



