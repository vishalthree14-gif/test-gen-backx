from models.user_token_model import UserTokenCollection
from flask import jsonify

def token_purchase(user_id, amount):

    pres_token = UserTokenCollection.find_user_token(user_id)

    pres_token += amount

    UserTokenCollection.purchase_token(user_id, pres_token)

    return jsonify({"message": "Payment verified & tokens added"})


def view_tokens(user_id):

    tokens = UserTokenCollection.find_user_token(user_id)

    return jsonify({"message": "tokens found", "token_cnt": tokens})


