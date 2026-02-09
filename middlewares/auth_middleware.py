from functools import wraps
from flask import request, jsonify, g
import jwt
from models.user_model import QuizUserCollection
from bson import ObjectId
from models.user_model import UserRole

import os
SECRET_KEY = os.getenv("SECRET_KEY")

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        # token = request.cookies.get("access_token")
        token = request.cookies.get("access_token")  # ✅ SAME NAME

        if not token:
            return jsonify({"message": "Authentication required"}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = QuizUserCollection.find_by_id(payload["user_id"])

            if not user:
                return jsonify({"message": "User not found"}), 401

            g.current_user = user
            g.user_id = str(user["_id"])   # ✅ ADD THIS

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return fn(*args, **kwargs)
    return wrapper


def role_required(role: UserRole):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = g.current_user

            if user["role"] != role.value:
                return jsonify({"message": "Access denied"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator



