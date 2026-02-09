from flask import request, jsonify
from services.resource_service import get_learning_resource
from models.web_link_model import WebQuizCollection
from models.quiz_model import QuizCollection

def search_web_controller(quiz_id):

    quiz_detail = QuizCollection.find_quiz(quiz_id)

    # print("*****************************************", quiz_detail)

    topic = quiz_detail["topic"]

    # print("-----------------------------------------", topic, difficulty)

    results = get_learning_resource(topic)

    web_docs = WebQuizCollection(
        quiz_id=quiz_id,
        web_links=results,
    )

    web_docs.save()


    return jsonify({
        "topic": topic,
        "results": results,
        "count": len(results)
    }), 200

