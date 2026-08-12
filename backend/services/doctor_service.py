from services.auth_service import register_user
from models.doctor_model import delete_doctor
from models.doctor_model import (
    create_doctor,
    get_all_doctors,
    update_doctor,
    get_user_id_from_doctor
)


def register_doctor(
    full_name,
    email,
    password,
    specialization,
    phone,
    experience_years,
    qualification
):

    user_id, response, status = register_user(
        full_name,
        email,
        password,
        "DOCTOR"
    )

    if status != 201:
        return response, status

    create_doctor(
        user_id,
        specialization,
        phone,
        experience_years,
        qualification
    )

    return {
        "message": "Doctor registered successfully",
        "user_id": user_id
    }, 201


def fetch_all_doctors():

    doctors = get_all_doctors()

    result = []

    for doctor in doctors:

        result.append({

            "doctor_id": doctor[0],
            "full_name": doctor[1],
            "email": doctor[2],
            "specialization": doctor[3],
            "phone": doctor[4],
            "experience_years": doctor[5],
            "qualification": doctor[6]

        })

    return result, 200


def edit_doctor(
    doctor_id,
    full_name,
    specialization,
    phone,
    experience_years,
    qualification
):

    # Find the corresponding user_id
    user_id = get_user_id_from_doctor(doctor_id)

    if user_id is None:

        return {
            "message": "Doctor not found"
        }, 404

    update_doctor(
        user_id,
        full_name,
        specialization,
        phone,
        experience_years,
        qualification
    )

    return {
        "message": "Doctor updated successfully"
    }, 200
def remove_doctor(doctor_id):

    deleted = delete_doctor(doctor_id)

    if not deleted:
        return {
            "message": "Doctor not found"
        },404

    return {
        "message": "Doctor deleted successfully"
    },200