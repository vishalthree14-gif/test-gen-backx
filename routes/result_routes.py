from flask import Blueprint, request, jsonify
from controllers.result_collection import create_student_result
from middlewares.auth_middleware import jwt_required, role_required
from models.user_model import UserRole

result_bp = Blueprint("result_routes", __name__)

@result_bp.route("/save-results", methods=["POST"])
@jwt_required
@role_required(UserRole.STUDENT)
def save_test_results():
    
    data = request.json

    marks = data.get("marks")
    quiz_id = data.get("quiz_id")

    create_student_result(marks, quiz_id)

    return jsonify({"message": "result saved successfully"}), 200
