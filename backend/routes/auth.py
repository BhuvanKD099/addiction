from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__)


# -----------------------------
# Test Route
# -----------------------------
@auth_bp.route("/test", methods=["GET"])
def test():
    return {
        "message": "Authentication Route Working"
    }, 200


# -----------------------------
# Register User
# -----------------------------
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    user_id, response, status = register_user(
        data["full_name"],
        data["email"],
        data["password"],
        data["role"]
    )

    if user_id:
        response["user_id"] = user_id

    return response, status


# -----------------------------
# Login User
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    return login_user(email, password)


# -----------------------------
# Protected Profile
# -----------------------------
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    return {
        "message": "Access granted",
        "logged_in_user": user_id
    }, 200