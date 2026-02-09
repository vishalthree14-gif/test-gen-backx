from flask import request, jsonify, make_response
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import QuizUserCollection, UserRole
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def register_controller():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"message": "Invalid JSON body"}), 400

        required_fields = ["email", "password", "dob", "role", "phone_number"]
        missing = validate_required_fields(data, required_fields)
        if missing:
            return jsonify({
                "message": "Missing required fields",
                "missing_fields": missing
            }), 400

        # ✅ VALIDATE ROLE ONLY
        if data["role"] not in [r.value for r in UserRole]:
            return jsonify({"message": "Invalid role value"}), 400

        if QuizUserCollection.find_by_email(data["email"]):
            return jsonify({"message": "User already exists"}), 400

        print("------------++++++++++++--------", data["role"])

        user = QuizUserCollection(
            email=data["email"],
            password=generate_password_hash(data["password"]),
            dob=data["dob"],
            role=UserRole(data["role"]),      # 🔥 STORE STRING DIRECTLY
            phone_number=data["phone_number"]
        )

        user_id = user.save()

        return jsonify({
            "message": "User registered successfully",
            "user_id": str(user_id)
        }), 201

    except Exception as e:
        print("REGISTER ERROR:", e)
        return jsonify({"message": "Internal server error"}), 500



def login_controller():

    try:
        if not request.is_json:
            return jsonify({"message": "Content-Type must be application/json"}), 400

        data = request.get_json(silent=True)

        if not data:
            return jsonify({"message": "Invalid JSON body"}), 400



        required_fields = ["email", "password"]
        missing = validate_required_fields(data, required_fields)

        if missing:
            return jsonify({
                "message": "Missing required fields",
                "missing_fields": missing
            }), 400

        user = QuizUserCollection.find_by_email(data["email"])

        if not user or not check_password_hash(user["password"], data["password"]):
            return jsonify({"message": "Invalid email or password"}), 401

        payload = {
            "user_id": str(user["_id"]),
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=24)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        response = make_response(jsonify({
            "message": "Login successful",
            "role": user["role"]
        }))

        # response.set_cookie(
        #     "access_token",
        #     token,
        #     httponly=True,
        #     samesite="Lax",
        #     max_age=24 * 60 * 60
        # )
        
        response.set_cookie(
            "access_token",
            token,
            httponly=True,
            samesite="Lax",
            secure=False,        # 🔥 REQUIRED FOR localhost
            max_age=24 * 60 * 60
        )

        return response

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"message": "Internal server error"}), 500




def validate_required_fields(data, fields):
    missing = [field for field in fields if not data.get(field)]
    return missing


