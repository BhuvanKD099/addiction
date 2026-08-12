from services.auth_service import register_user

from models.doctor_model import doctor_exists

from models.patient_model import (
    create_patient,
    get_all_patients,
    get_patient_by_id,
    update_patient,
    delete_patient
)


def register_patient(
    full_name,
    email,
    password,
    doctor_id,
    age,
    gender,
    phone,
    address,
    emergency_contact,
    admission_date,
    addiction_type,
    addiction_severity
):

    user_id, response, status = register_user(
        full_name,
        email,
        password,
        "PATIENT"
    )

    if status != 201:
        return response, status

    if not doctor_exists(doctor_id):
        return {
            "error": "Doctor not found"
        }, 404

    patient_id = create_patient(
        user_id,
        doctor_id,
        age,
        gender,
        phone,
        address,
        emergency_contact,
        admission_date,
        addiction_type,
        addiction_severity
    )

    return {
        "message": "Patient registered successfully",
        "patient_id": patient_id,
        "user_id": user_id
    }, 201


def fetch_all_patients():

    patients = get_all_patients()

    result = []

    for patient in patients:

        result.append({
            "patient_id": patient[0],
            "full_name": patient[1],
            "email": patient[2],
            "doctor_id": patient[3],
            "doctor_name": patient[4],
            "age": patient[5],
            "gender": patient[6],
            "phone": patient[7],
            "addiction_type": patient[8],
            "addiction_severity": patient[9],
            "admission_date": str(patient[10])
        })

    return result, 200


def fetch_patient(patient_id):

    patient = get_patient_by_id(patient_id)

    if not patient:
        return {"error": "Patient not found"}, 404

    return {
        "patient_id": patient[0],
        "full_name": patient[1],
        "email": patient[2],

        "doctor": {
            "doctor_id": patient[3],
            "name": patient[4],
            "specialization": patient[5]
        },

        "patient": {
            "age": patient[6],
            "gender": patient[7],
            "phone": patient[8],
            "address": patient[9],
            "emergency_contact": patient[10],
            "admission_date": str(patient[11]),
            "addiction_type": patient[12],
            "addiction_severity": patient[13]
        }

    }, 200


def edit_patient(
    patient_id,
    full_name,
    email,
    doctor_id,
    age,
    gender,
    phone,
    address,
    emergency_contact,
    admission_date,
    addiction_type,
    addiction_severity
):
    try:
        doctor_id = int(doctor_id) if doctor_id else 1
    except (ValueError, TypeError):
        doctor_id = 1

    try:
        age = int(age) if age else 30
    except (ValueError, TypeError):
        age = 30

    if not doctor_exists(doctor_id):
        return {
            "message": "Doctor not found"
        }, 404

    updated = update_patient(
        patient_id,
        full_name,
        email,
        doctor_id,
        age,
        gender,
        phone,
        address,
        emergency_contact,
        admission_date,
        addiction_type,
        addiction_severity
    )

    if not updated:
        return {
            "message": "Patient not found"
        }, 404

    return {
        "message": "Patient updated successfully"
    }, 200


def remove_patient(patient_id):

    deleted = delete_patient(patient_id)

    if not deleted:
        return {
            "message": "Patient not found"
        }, 404

    return {
        "message": "Patient deleted successfully"
    }, 200