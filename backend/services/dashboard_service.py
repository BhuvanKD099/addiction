from models.dashboard_model import get_patient_dashboard

from models.dashboard_model import (
    get_patient_dashboard,
    get_dashboard_stats
)
def dashboard_stats():

    patients, doctors, appointments = get_dashboard_stats()

    return {
        "patients": patients,
        "doctors": doctors,
        "appointments": appointments
    }, 200
def calculate_score(mood, sleep, craving, medication, counselling):

    score = 0

    if mood == "GOOD":
        score += 20

    if sleep and sleep >= 7:
        score += 20

    if craving is not None and craving <= 3:
        score += 20

    if medication:
        score += 20

    if counselling:
        score += 20

    if score >= 80:
        risk = "LOW"
    elif score >= 50:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return score, risk


def patient_dashboard(patient_id):

    data = get_patient_dashboard(patient_id)

    if not data:
        return {"error": "Patient not found"}, 404

    score, risk = calculate_score(
        data[4],
        data[5],
        data[6],
        data[7],
        data[8]
    )

    return {
        "patient_name": data[0],
        "doctor_name": data[1],
        "addiction_type": data[2],
        "severity": data[3],

        "today_progress": {
            "mood": data[4],
            "sleep_hours": float(data[5]) if data[5] else None,
            "craving_level": data[6]
        },

        "next_appointment": {
            "date": str(data[9]) if data[9] else None,
            "time": str(data[10]) if data[10] else None
        },

        "recovery_score": score,
        "risk": risk
    }, 200