from flask import Blueprint, request
from services.appointment_service import (
    register_appointment,
    fetch_all_appointments,
    fetch_appointment,
    edit_appointment,
    remove_appointment
)

appointment_bp = Blueprint("appointment", __name__)


@appointment_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    return register_appointment(
        data.get("patient_id"),
        data.get("doctor_id"),
        data.get("appointment_date"),
        data.get("appointment_time"),
        data.get("status", "SCHEDULED"),
        data.get("notes", "")
    )


@appointment_bp.route("/", methods=["GET"])
def get_appointments():
    return fetch_all_appointments()


@appointment_bp.route("/<int:appointment_id>", methods=["GET"])
def get_appointment(appointment_id):
    return fetch_appointment(appointment_id)


@appointment_bp.route("/<int:appointment_id>", methods=["PUT"])
def update_appointment_route(appointment_id):
    data = request.get_json() or {}

    return edit_appointment(
        appointment_id,
        data.get("patient_id"),
        data.get("doctor_id"),
        data.get("appointment_date"),
        data.get("appointment_time"),
        data.get("status", "SCHEDULED"),
        data.get("notes", "")
    )


@appointment_bp.route("/<int:appointment_id>", methods=["DELETE"])
def delete_appointment_route(appointment_id):
    return remove_appointment(appointment_id)