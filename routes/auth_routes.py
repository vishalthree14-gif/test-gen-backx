from flask import Blueprint, request, jsonify
from controllers.auth_controller import register_controller, login_controller
from middlewares.auth_middleware import jwt_required, role_required
from models.user_model import UserRole
import jwt
import os

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = os.getenv("SECRET_KEY")

# Public
auth_bp.route("/auth/login", methods=["POST"])(login_controller)
auth_bp.route("/auth/register", methods=["POST"])(register_controller)

# Protected examples
@auth_bp.route("/mentor", methods=["GET"])
@jwt_required
@role_required(UserRole.MENTOR)
def mentor_only():
    return {"message": "Mentor access granted"}


@auth_bp.route("/student", methods=["GET"])
@jwt_required
@role_required(UserRole.STUDENT)
def student_only():
    return {"message": "Student access granted"}


@auth_bp.route("/auth/me", methods=["GET"])
def me():
    token = request.cookies.get("access_token")

    if not token:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({
            "user_id": payload["user_id"],
            "role": payload["role"]
        })
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401


@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged out successfully"})
    response.set_cookie("access_token", "", expires=0)
    return response

