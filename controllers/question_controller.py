from services.quiz_service import generate_quiz
from models.quiz_question_model import QuizQuestionCollection
from models.quiz_model import QuizCollection


def gen_quiz(quiz_id):

    quiz_detail = QuizCollection.find_quiz(quiz_id)

    # print("*****************************************", quiz_detail)

    topic = quiz_detail["topic"]
    difficulty = quiz_detail["difficulty"]

    # print("-----------------------------------------", topic, difficulty)


    # topic, difficulty, 

    topic = f"""
    Generate exactly 10 multiple-choice question on {topic}.
    Difficulty: {difficulty}
    use 4 options (A,B,C,D)
    answer
    Return only JSON
    """

    quiz_exist = QuizQuestionCollection.find_question(quiz_id)

    if quiz_exist:
        return None

    questions = generate_quiz(topic)


    quiz_doc = QuizQuestionCollection(
        quiz_id= quiz_id,
        questions= questions
    )

    quiz_doc.save()

    return questions

