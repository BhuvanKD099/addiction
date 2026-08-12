from flask_jwt_extended import create_access_token
from auth.password import bcrypt
from models.user_model import create_user, get_user_by_email



def register_user(full_name, email, password, role):

    existing_user = get_user_by_email(email)

    if existing_user:
        return None, {
            "error": "Email already registered"
        }, 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user_id = create_user(full_name, email, hashed_password, role)

    return user_id, {
        "message": "User registered successfully"
    }, 201


def login_user(email, password):

    user = get_user_by_email(email)

    if not user:
        return {"error": "Invalid email or password"}, 401

    if not bcrypt.check_password_hash(user[3], password):
        return {"error": "Invalid email or password"}, 401

    token = create_access_token(identity=str(user[0]))

    return {
        "message": "Login successful",
        "access_token": token,
        "user": {
            "user_id": user[0],
            "full_name": user[1],
            "email": user[2],
            "role": user[4]
        }
    }, 200