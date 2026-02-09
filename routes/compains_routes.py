from controllers.compains_controller import create_compains, add_people, get_compains, get_all_people, email_compains
from flask import Blueprint, request, jsonify, g
from middlewares.auth_middleware import jwt_required, role_required
from models.user_model import UserRole

compains_bp = Blueprint("compains_routes", __name__)

@compains_bp.route("/create-compains", methods=["POST"])
@jwt_required
@role_required(UserRole.MENTOR)
def create():

    data = request.json

    name = data.get("name")

    return create_compains(name)


@compains_bp.route("/add-member", methods=["POST"])
@jwt_required
@role_required(UserRole.MENTOR)
def add_member():
    data = request.json

    name = data.get("name")
    compain_id = data.get("compain_id")
    email_address = data.get("email_address")
    whatsapp_number = data.get("whatsapp_number")

    return add_people(name, compain_id, email_address, whatsapp_number)


@compains_bp.route("/get-members/<compains_id>", methods=["GET"])
@jwt_required
@role_required(UserRole.MENTOR)
def get_members(compains_id):

    return get_all_people(compains_id)


@compains_bp.route("/get-compains", methods=["GET"])
@jwt_required
@role_required(UserRole.MENTOR)
def get_user_compains():

    return get_compains()


@compains_bp.route("/compains/send-emails", methods=["POST"])
@jwt_required
@role_required(UserRole.MENTOR)
def send_emails_students():

    data = request.json

    quiz_id = data.get("quiz_id")

    user_id = g.user_id

    # accept both email / emails
    emails = data.get("emails") or data.get("email")

    if not emails:
        return jsonify({"message": "No email provided"}), 400

    # normalize to list of strings
    if isinstance(emails, str):
        emails = [emails]

    if not isinstance(emails, list):
        return jsonify({"message": "Invalid email format"}), 400

    res = email_compains(emails, quiz_id, user_id)

    if not res:
        return jsonify({"error": "token not enough. to send emails"})

    return jsonify({"message": "Mail sent successfully"}), 200

