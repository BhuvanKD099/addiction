from flask import Blueprint, request
from models.medication_model import (
    create_medication,
    get_patient_medications,
    update_medication,
    delete_medication
)

medications_bp = Blueprint("medications", __name__)


@medications_bp.route("/patient/<int:patient_id>", methods=["GET"])
def get_medications(patient_id):
    meds = get_patient_medications(patient_id)
    return {"medications": meds}, 200


@medications_bp.route("/", methods=["POST"])
def add_medication():
    data = request.get_json()
    med_id = create_medication(
        patient_id=data["patient_id"],
        doctor_id=data["doctor_id"],
        medication_name=data["medication_name"],
        dosage=data["dosage"],
        frequency=data["frequency"],
        start_date=data["start_date"],
        end_date=data.get("end_date"),
        status=data.get("status", "ACTIVE")
    )
    return {"message": "Medication prescribed successfully", "medication_id": med_id}, 201


@medications_bp.route("/<int:medication_id>", methods=["PUT"])
def edit_medication(medication_id):
    data = request.get_json()
    updated = update_medication(
        medication_id=medication_id,
        medication_name=data["medication_name"],
        dosage=data["dosage"],
        frequency=data["frequency"],
        status=data.get("status", "ACTIVE")
    )
    if not updated:
        return {"error": "Medication not found"}, 404
    return {"message": "Medication updated successfully"}, 200


@medications_bp.route("/<int:medication_id>", methods=["DELETE"])
def remove_medication(medication_id):
    deleted = delete_medication(medication_id)
    if not deleted:
        return {"error": "Medication not found"}, 404
    return {"message": "Medication deleted successfully"}, 200
