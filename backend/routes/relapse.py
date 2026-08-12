from flask import Blueprint, request, jsonify
from services.prediction_service import (
    assess_patient_relapse_risk,
    fetch_patient_relapse_history
)
from ai.relapse_predictor import predict_relapse_risk
from ai.dataset_manager import append_relapse_sample
from utils.database import mysql

relapse_bp = Blueprint("relapse", __name__)


@relapse_bp.route("/predict", methods=["POST"])
def predict():
    """
    Runs Random Forest AI Relapse Risk Predictor
    """
    data = request.get_json() or {}
    mood = data.get("mood", "Normal")
    sleep_quality = data.get("sleep_quality", "Good")
    craving_level = int(data.get("craving_level", 5))
    medication_adherence = int(data.get("medication_adherence", 1))
    counseling_attendance = int(data.get("counseling_attendance", 1))
    stress_level = int(data.get("stress_level", 3))
    previous_relapses = int(data.get("previous_relapses", 0))
    addiction_severity = data.get("addiction_severity", "MODERATE")

    result = predict_relapse_risk(
        mood=mood,
        sleep_quality=sleep_quality,
        craving_level=craving_level,
        medication_adherence=medication_adherence,
        counseling_attendance=counseling_attendance,
        stress_level=stress_level,
        previous_relapses=previous_relapses,
        addiction_severity=addiction_severity
    )

    # Ingest sample into Real-Time Relapse Dataset
    try:
        mood_map = {"EXCELLENT": 5.0, "GOOD": 4.0, "NORMAL": 3.0, "FAIR": 3.0, "BAD": 2.0, "VERY BAD": 1.0}
        sleep_map = {"VERY GOOD": 5.0, "GOOD": 4.0, "FAIR": 3.0, "POOR": 2.0, "VERY POOR": 1.0}
        severity_map = {"MILD": 1, "MODERATE": 2, "SEVERE": 3}
        
        m_num = mood_map.get(str(mood).upper(), 3.0)
        s_num = sleep_map.get(str(sleep_quality).upper(), 3.0)
        sev_num = severity_map.get(str(addiction_severity).upper(), 2)

        append_relapse_sample(
            m_num, s_num, craving_level, medication_adherence,
            counseling_attendance, stress_level, previous_relapses, sev_num,
            result["predicted_risk_level"]
        )
    except Exception as e:
        print("Warning: Real-time relapse dataset ingestion skipped:", e)

    return jsonify(result), 200


@relapse_bp.route("/record", methods=["POST"])
def record_relapse():
    """
    Logs a relapse incident for a patient
    """
    data = request.get_json() or {}
    patient_id = data.get("patient_id", 1)
    relapse_date = data.get("relapse_date")
    cause = data.get("cause", "")
    trigger_factors = data.get("trigger_factors", "")
    stress_level = int(data.get("stress_level", 8))
    substance_used = data.get("substance_used", "")
    counselor_notes = data.get("counselor_notes", "")
    recovery_action = data.get("recovery_action", "")
    support_required = data.get("support_required", "")

    try:
        cur = mysql.connection.cursor()
        query = """
            INSERT INTO relapse_records
            (patient_id, relapse_date, cause, trigger_factors, stress_level, substance_used, counselor_notes, recovery_action, support_required)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            patient_id, relapse_date, cause, trigger_factors, stress_level,
            substance_used, counselor_notes, recovery_action, support_required
        ))
        mysql.connection.commit()
        relapse_id = cur.lastrowid
        cur.close()
        return jsonify({"message": "Relapse record saved", "relapse_id": relapse_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@relapse_bp.route("/assess/<int:patient_id>", methods=["POST"])
def assess(patient_id):
    return assess_patient_relapse_risk(patient_id)


@relapse_bp.route("/history/<int:patient_id>", methods=["GET"])
def history(patient_id):
    return fetch_patient_relapse_history(patient_id)


@relapse_bp.route("/record/<int:relapse_id>", methods=["PUT"])
def update_relapse_record(relapse_id):
    data = request.get_json() or {}
    relapse_date = data.get("relapse_date")
    cause = data.get("cause", "")
    trigger_factors = data.get("trigger_factors", "")
    stress_level = int(data.get("stress_level", 8))
    substance_used = data.get("substance_used", "")
    counselor_notes = data.get("counselor_notes", "")
    recovery_action = data.get("recovery_action", "")
    support_required = data.get("support_required", "")

    try:
        cur = mysql.connection.cursor()
        query = """
            UPDATE relapse_records
            SET relapse_date=%s, cause=%s, trigger_factors=%s, stress_level=%s,
                substance_used=%s, counselor_notes=%s, recovery_action=%s, support_required=%s
            WHERE relapse_id=%s
        """
        cur.execute(query, (
            relapse_date, cause, trigger_factors, stress_level,
            substance_used, counselor_notes, recovery_action, support_required, relapse_id
        ))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Relapse record updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@relapse_bp.route("/record/<int:relapse_id>", methods=["DELETE"])
def delete_relapse_record(relapse_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM relapse_records WHERE relapse_id=%s", (relapse_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Relapse record deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

