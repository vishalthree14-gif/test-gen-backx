from models.compains_model import CompainsCollection
from models.compains_data_model import CompainsDataCollection
from flask import g, jsonify
from services.email_service import send_quiz_email_to_students
from models.quiz_model import QuizCollection
from models.user_token_model import UserTokenCollection
import os
from dotenv import load_dotenv

load_dotenv()

def create_compains(name):

    user_id = g.user_id

    already_exist = CompainsCollection.find_compains(name, user_id)

    if already_exist:
        return jsonify({"message": "compains already exist!"}), 200

    try:
        doc_comp = CompainsCollection(
            user_id=user_id,
            name=name
        )

        doc_comp.save()

    except Exception as e:
        return jsonify({"error": e})

    return jsonify({"message": "compains created successfully!"}), 201


def get_compains():
    user_id = g.user_id

    cursor = CompainsCollection.find_user_compains(user_id)

    all_compains = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["user_id"] = str(doc["user_id"])
        all_compains.append(doc)

    return jsonify({"data": list(all_compains)}), 200


def add_people(name, compain_id, email_address, whatsapp_number):

    already_exist = CompainsDataCollection.find_email(email_address, compain_id)

    if already_exist:
        return jsonify({"message": "member already exist"}), 200
    
    doc_save = CompainsDataCollection(
        name=name,
        compains_id=compain_id,
        email_address=email_address,
        whatsapp_number=whatsapp_number
    )

    doc_save.save()

    return jsonify({"message": "member added successfully"}), 201


def get_all_people(compains_id):

    cursor = CompainsDataCollection.find_members(compains_id)

    all_data = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["compains_id"] = str(doc["_id"])

        # print("******************", doc)

        all_data.append(doc)

    return jsonify({"data": all_data}), 200


def email_compains(emails, quiz_id, user_id):

    quiz_detail = QuizCollection.find_quiz(quiz_id)

    # print("-------------------------------", quiz_detail)

    topic_name=quiz_detail.get("topic")
    duration=quiz_detail.get("time_duration")

    emails_no = len(emails)
    cost_per_email = int(os.getenv("TOKEN_COST_EMAIL", 100))

    total_cost = emails_no * cost_per_email

    token_present = UserTokenCollection.find_user_token(user_id)

    if token_present < total_cost:
        return {"error": "Not enough tokens"}, 400

    UserTokenCollection.spend_token(user_id, total_cost)

    email_send = send_quiz_email_to_students(

        student_emails=emails,   # ✅ FIXED
        topic_name=topic_name,
        duration=duration
    )

    return email_send

