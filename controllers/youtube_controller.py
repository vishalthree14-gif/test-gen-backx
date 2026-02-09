from flask import request, jsonify
from services.youtube_search_service import search_youtube_videos
from models.youtube_link_model import YoutubeQuizCollection
from models.quiz_model import QuizCollection

def search_youtube_controller(quiz_id):


    quiz_detail = QuizCollection.find_quiz(quiz_id)

    # print("*****************************************", quiz_detail)

    topic = quiz_detail["topic"]

    # print("-----------------------------------------", topic, difficulty)

    videos = search_youtube_videos(topic)

    youtube_docs =YoutubeQuizCollection(
        quiz_id=quiz_id,
        video_link=videos,
    )

    youtube_docs.save()


    return jsonify({
        "topic": topic,
        "count": len(videos),
        "videos": videos
    }), 200


