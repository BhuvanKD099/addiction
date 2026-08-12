from flask import Blueprint, request

from services.patient_service import (
    register_patient,
    fetch_all_patients,
    fetch_patient,
    edit_patient,
    remove_patient
)

patient_bp = Blueprint("patient", __name__)


@patient_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    return register_patient(
        data.get("full_name"),
        data.get("email"),
        data.get("password"),
        data.get("doctor_id"),
        data.get("age"),
        data.get("gender"),
        data.get("phone"),
        data.get("address"),
        data.get("emergency_contact"),
        data.get("admission_date"),
        data.get("addiction_type"),
        data.get("addiction_severity")
    )


@patient_bp.route("/", methods=["GET"])
def get_patients():
    return fetch_all_patients()


@patient_bp.route("/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    return fetch_patient(patient_id)


@patient_bp.route("/<int:patient_id>", methods=["PUT"])
def update_patient_route(patient_id):
    data = request.get_json() or {}

    return edit_patient(
        patient_id,
        data.get("full_name"),
        data.get("email"),
        data.get("doctor_id"),
        data.get("age"),
        data.get("gender"),
        data.get("phone"),
        data.get("address"),
        data.get("emergency_contact"),
        data.get("admission_date"),
        data.get("addiction_type"),
        data.get("addiction_severity")
    )


@patient_bp.route("/<int:patient_id>", methods=["DELETE"])
def delete_patient_route(patient_id):
    return remove_patient(patient_id)