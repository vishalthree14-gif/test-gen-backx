from models.user_model import QuizUserCollection
from flask import jsonify, make_response
from services.password_service import hash_password, verify_password
from services.jwt_service import generate_jwt, decode_jwt


def login_func(email: str, password: str):

    user = QuizUserCollection.find_by_email(email)

    if not user:
        return jsonify({"message": "user doesn't exist"})


    if not verify_password(password, user["password"]):
        return jsonify({"message": "Invalid credentials"}), 401
    

    token = generate_jwt(user_id=str(user["_id"]))

    # return jsonify({
    #     "message": "Login sccessful",
    #     "acces_token": token
    # }), 200

    response = make_response(jsonify({
        "message": "Login successful"
    }))

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,     # 🔐 JS can't access
        secure=False,      # True ONLY in HTTPS
        samesite="Lax",    # Good for same-site requests
        max_age=60 * 60 * 24  # 1 day
    )

    return response, 200



def register_user(email: str, password: str, dob: str, job_role: str, phone_number: int):

    hash_pass = hash_password(password)

    register_user = QuizUserCollection(
        email, hash_pass, dob, job_role, phone_number
    )

    register_user.save()

    if not register_user:
        return jsonify({"message": "user created account"}), 200

    
    return jsonify({"message": "user created account"}), 200

