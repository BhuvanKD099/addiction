from models.appointment_model import (
    create_appointment,
    get_all_appointments,
    get_appointment_by_id,
    update_appointment,
    delete_appointment
)
from models.patient_model import get_patient_by_id
from models.doctor_model import doctor_exists


def register_appointment(
    patient_id,
    doctor_id,
    appointment_date,
    appointment_time,
    status,
    notes
):
    if not patient_id or not doctor_id or not appointment_date or not appointment_time:
        return {"error": "Patient, Doctor, Date, and Time are required."}, 400

    try:
        patient_id = int(patient_id)
        doctor_id = int(doctor_id)
    except (ValueError, TypeError):
        return {"error": "Invalid Patient ID or Doctor ID format."}, 400

    patient = get_patient_by_id(patient_id)
    if not patient:
        return {"error": f"Patient with ID {patient_id} not found. Please register the patient first."}, 404

    doctor = doctor_exists(doctor_id)
    if not doctor:
        return {"error": f"Doctor with ID {doctor_id} not found. Please register the doctor first."}, 404

    appointment_id = create_appointment(
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status or "SCHEDULED",
        notes or ""
    )

    return {
        "message": "Appointment scheduled successfully",
        "appointment_id": appointment_id
    }, 201


def fetch_all_appointments():
    try:
        appointments = get_all_appointments()
        result = []

        for appointment in appointments:
            result.append({
                "appointment_id": appointment[0],
                "patient": {
                    "patient_id": appointment[1],
                    "name": appointment[2]
                },
                "doctor": {
                    "doctor_id": appointment[3],
                    "name": appointment[4]
                },
                "appointment_date": str(appointment[5]),
                "appointment_time": str(appointment[6]),
                "status": appointment[7],
                "notes": appointment[8]
            })

        return result, 200
    except Exception as e:
        print("Error fetching appointments:", e)
        return [], 200


def fetch_appointment(appointment_id):
    appointment = get_appointment_by_id(appointment_id)

    if not appointment:
        return {"error": "Appointment not found"}, 404

    return {
        "appointment_id": appointment[0],
        "patient_id": appointment[1],
        "doctor_id": appointment[2],
        "appointment_date": str(appointment[3]),
        "appointment_time": str(appointment[4]),
        "status": appointment[5],
        "notes": appointment[6]
    }, 200


def edit_appointment(
    appointment_id,
    patient_id,
    doctor_id,
    appointment_date,
    appointment_time,
    status,
    notes
):
    if not patient_id or not doctor_id or not appointment_date or not appointment_time:
        return {"error": "Patient, Doctor, Date, and Time are required."}, 400

    try:
        patient_id = int(patient_id)
        doctor_id = int(doctor_id)
    except (ValueError, TypeError):
        return {"error": "Invalid Patient ID or Doctor ID format."}, 400

    if not get_patient_by_id(patient_id):
        return {"error": "Patient not found"}, 404

    if not doctor_exists(doctor_id):
        return {"error": "Doctor not found"}, 404

    updated = update_appointment(
        appointment_id,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status,
        notes
    )

    if not updated:
        return {"error": "Appointment not found or no changes made"}, 404

    return {"message": "Appointment updated successfully"}, 200


def remove_appointment(appointment_id):
    deleted = delete_appointment(appointment_id)

    if not deleted:
        return {"error": "Appointment not found"}, 404

    return {"message": "Appointment deleted successfully"}, 200