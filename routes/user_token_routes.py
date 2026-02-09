from flask import Blueprint, g, request
from middlewares.auth_middleware import jwt_required
from controllers.user_token_controller import token_purchase, view_tokens
from services.payment_service import client
from services.payment_service import create_order

token_bp = Blueprint("tokens", __name__)


@token_bp.route("/create-order", methods=["POST"])
@jwt_required
def create_payment_order():
    data = request.json
    amount = data.get("amount")

    order = create_order(amount)

    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": "INR"
    }



@token_bp.route("/verify-payment", methods=["POST"])
@jwt_required
def verify_payment():
    data = request.json

    params = {
        "razorpay_order_id": data["order_id"],
        "razorpay_payment_id": data["payment_id"],
        "razorpay_signature": data["signature"]
    }

    try:
        client.utility.verify_payment_signature(params)
    except:
        return {"error": "Payment verification failed"}, 400

    # ✅ VERIFIED — NOW ADD TOKENS
    user_id = g.user_id
    tokens = data["tokens"]

    return token_purchase(user_id, tokens)


@token_bp.route("/get-tokens", methods=["GET"])
@jwt_required
def get_ur_tokens():

    user_id = g.user_id
    return view_tokens(user_id)

