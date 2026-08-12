from models.patient_model import get_patient_by_id
from models.progress_model import get_all_progress
from models.relapse_model import save_relapse_assessment, get_patient_relapse_history, get_latest_relapse_assessment
from ai.relapse_predictor import predict_relapse_risk


def assess_patient_relapse_risk(patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        return {"error": "Patient not found"}, 404

    # Extract patient addiction severity
    # patient[13] is addiction_severity in get_patient_by_id query
    addiction_severity = patient[13] if len(patient) > 13 else "MODERATE"

    # Fetch recent progress logs for this patient
    all_progress = get_all_progress()
    patient_progress = [p for p in all_progress if p[1] == patient_id]

    craving_level = 5
    withdrawal_level = 5
    mood = "Normal"
    recovery_score = 70

    if patient_progress:
        # Latest progress entry
        latest = patient_progress[0]
        # p: [progress_id, patient_id, full_name, progress_date, mood, craving_level, withdrawal_level, recovery_score, counselor_notes]
        mood = latest[4] if len(latest) > 4 and latest[4] else "Normal"
        craving_level = latest[5] if len(latest) > 5 and latest[5] is not None else 5
        withdrawal_level = latest[6] if len(latest) > 6 and latest[6] is not None else 5
        recovery_score = latest[7] if len(latest) > 7 and latest[7] is not None else 70

    # Execute AI Predictor
    ai_result = predict_relapse_risk(
        craving_level=craving_level,
        withdrawal_level=withdrawal_level,
        mood=mood,
        sleep_hours=7.0,
        medication_compliance=True,
        counselling_attended=True,
        addiction_severity=addiction_severity,
        recent_recovery_score=recovery_score
    )

    # Save assessment to Database
    assessment_id = save_relapse_assessment(
        patient_id=patient_id,
        risk_level=ai_result["risk_level"],
        risk_score=ai_result["risk_score"],
        triggers=ai_result["triggers"],
        recommendations=ai_result["recommendations"]
    )

    ai_result["assessment_id"] = assessment_id
    ai_result["patient_id"] = patient_id
    ai_result["patient_name"] = patient[1]

    return ai_result, 200


def fetch_patient_relapse_history(patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        return {"error": "Patient not found"}, 404

    history = get_patient_relapse_history(patient_id)
    return {
        "patient_id": patient_id,
        "patient_name": patient[1],
        "history": history
    }, 200
