from flask import Blueprint, request
from services.doctor_service import (
    register_doctor,
    fetch_all_doctors,
    edit_doctor,
    remove_doctor
)

doctor_bp = Blueprint("doctor", __name__)


@doctor_bp.route("/", methods=["GET"])
def get_doctors():
    return fetch_all_doctors()


@doctor_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    return register_doctor(
        data.get("full_name"),
        data.get("email"),
        data.get("password"),
        data.get("specialization"),
        data.get("phone"),
        data.get("experience_years"),
        data.get("qualification")
    )


@doctor_bp.route("/<int:doctor_id>", methods=["PUT"])
def update(doctor_id):
    data = request.get_json() or {}

    return edit_doctor(
        doctor_id,
        data.get("full_name"),
        data.get("specialization"),
        data.get("phone"),
        data.get("experience_years"),
        data.get("qualification")
    )


@doctor_bp.route("/<int:doctor_id>", methods=["DELETE"])
def delete(doctor_id):
    return remove_doctor(doctor_id)