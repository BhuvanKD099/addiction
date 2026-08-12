import json
from datetime import date
from flask import Blueprint, request, jsonify
from utils.database import mysql
from ai.addictionsense_engine import predict_addiction_risk
from ai.dataset_manager import ingest_screening_sample, append_screening_sample

addictionsense_bp = Blueprint("addictionsense", __name__)


@addictionsense_bp.route("/detect", methods=["POST"])
def detect_addiction_risk():
    """
    Runs Advanced Multimodal AI Addiction Risk Detection (Phases 1 & 2)
    Payload:
    {
        "patient_id": int (optional),
        "q_responses": [q1...q15],
        "parent_q_responses": [par1...par10],
        "smile_score": float,
        "eye_openness": float,
        "blink_rate": float,
        "facial_stress": float,
        "voice_stress": float,
        "hand_tremor": float,
        "user_consent": bool
    }
    """
    data = request.get_json() or {}
    patient_id = data.get("patient_id", 1)
    q_responses = data.get("q_responses", [3]*15)
    parent_q_responses = data.get("parent_q_responses", [3]*10)
    smile_score = float(data.get("smile_score", 0.5))
    eye_openness = float(data.get("eye_openness", 0.75))
    blink_rate = float(data.get("blink_rate", 16.0))
    facial_stress = float(data.get("facial_stress", 0.3))
    voice_stress = float(data.get("voice_stress", 0.25))
    hand_tremor = float(data.get("hand_tremor", 0.15))
    user_consent = bool(data.get("user_consent", True)) # Default True for UI testing

    # Run Multimodal AI Inference & Cross-Verification Engine
    result = predict_addiction_risk(
        q_responses=q_responses,
        parent_q_responses=parent_q_responses,
        smile_score=smile_score,
        eye_openness=eye_openness,
        blink_rate=blink_rate,
        facial_stress=facial_stress,
        voice_stress=voice_stress,
        hand_tremor=hand_tremor,
        user_consent=user_consent
    )

    # Ingest sample into Real-Time Multimodal Dataset (with User Consent Check)
    try:
        ingest_screening_sample(
            patient_q=q_responses,
            parent_q=parent_q_responses,
            smile_score=smile_score,
            eye_openness=eye_openness,
            blink_rate=blink_rate,
            facial_stress=facial_stress,
            voice_stress=voice_stress,
            hand_tremor=hand_tremor,
            verified_label=result["risk_level"],
            user_consent=user_consent
        )
    except Exception as e:
        print("Warning: Real-time dataset ingestion skipped:", e)

    # Persist Assessment Record to Database
    try:
        cur = mysql.connection.cursor()
        triggers_json = json.dumps(result["triggers"])
        recs_json = json.dumps(result["recommendations"])

        query = """
        INSERT INTO addiction_sense_assessments
        (patient_id, q_responses_json, questionnaire_score, facial_stress_score, blink_rate, eye_openness, voice_stress_score, hand_tremor_score, predicted_risk_level, confidence_score, risk_score, ai_explanation, triggers, recommendations)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            patient_id,
            json.dumps(q_responses),
            result["questionnaire_avg"],
            result["facial_stress_score"],
            result["blink_rate"],
            result["eye_openness"],
            result["voice_stress_score"],
            result["hand_tremor_score"],
            result["predicted_risk_level"],
            result["confidence_score"],
            result["risk_score"],
            result["ai_explanation"],
            triggers_json,
            recs_json
        ))
        mysql.connection.commit()
        if hasattr(cur, 'lastrowid'):
            result["assessment_id"] = cur.lastrowid
        cur.close()
    except Exception as e:
        pass

    return jsonify(result), 200


@addictionsense_bp.route("/analyze-face", methods=["POST"])
def analyze_face():
    data = request.get_json() or {}
    smile_score = float(data.get("smile_score", 0.6))
    eye_openness = float(data.get("eye_openness", 0.8))
    blink_rate = float(data.get("blink_rate", 16.0))

    raw_stress = 1.0 - (0.6 * smile_score + 0.4 * eye_openness)
    facial_stress_score = int(round(max(0.0, min(100.0, raw_stress * 100.0))))

    stress_level = "HIGH" if facial_stress_score >= 60 else ("MODERATE" if facial_stress_score >= 35 else "LOW")

    return jsonify({
        "smile_score": round(smile_score, 2),
        "eye_openness": round(eye_openness, 2),
        "blink_rate": round(blink_rate, 1),
        "facial_stress_score": facial_stress_score,
        "stress_level": stress_level
    }), 200


@addictionsense_bp.route("/analyze-voice", methods=["POST"])
def analyze_voice():
    data = request.get_json() or {}
    voice_tremor_index = float(data.get("voice_tremor_index", 0.25))
    voice_stress_score = int(round(voice_tremor_index * 100))

    return jsonify({
        "voice_stress_score": voice_stress_score,
        "pitch_stability": "Normal" if voice_stress_score < 40 else "Tremor Detected",
        "status": "Voice Analysis Complete"
    }), 200


@addictionsense_bp.route("/habits/<int:patient_id>", methods=["GET"])
def get_patient_habits(patient_id):
    try:
        cur = mysql.connection.cursor()
        query = """
        SELECT habit_id, habit_date, clean_day, meditation, exercise, support_group, hydration_liters, medication_taken
        FROM habit_tracker
        WHERE patient_id = %s
        ORDER BY habit_date DESC
        LIMIT 14
        """
        cur.execute(query, (patient_id,))
        rows = cur.fetchall()
        cur.close()

        habits = []
        for r in rows:
            habits.append({
                "habit_id": r[0],
                "habit_date": str(r[1]),
                "clean_day": r[2],
                "meditation": bool(r[3]),
                "exercise": bool(r[4]),
                "support_group": bool(r[5]),
                "hydration_liters": r[6],
                "medication_taken": bool(r[7])
            })
        return jsonify({"patient_id": patient_id, "habits": habits}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@addictionsense_bp.route("/habits", methods=["POST"])
def log_patient_habit():
    data = request.get_json() or {}
    patient_id = data.get("patient_id", 1)
    habit_date = data.get("habit_date", str(date.today()))
    clean_day = 1 if data.get("clean_day", True) else 0
    meditation = 1 if data.get("meditation", False) else 0
    exercise = 1 if data.get("exercise", False) else 0
    support_group = 1 if data.get("support_group", False) else 0
    hydration_liters = float(data.get("hydration_liters", 2.0))
    medication_taken = 1 if data.get("medication_taken", True) else 0

    try:
        cur = mysql.connection.cursor()
        query = """
        INSERT INTO habit_tracker
        (patient_id, habit_date, clean_day, meditation, exercise, support_group, hydration_liters, medication_taken)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            patient_id, habit_date, clean_day, meditation, exercise, support_group, hydration_liters, medication_taken
        ))
        mysql.connection.commit()
        habit_id = cur.lastrowid
        cur.close()

        return jsonify({
            "message": "Habit logged successfully",
            "habit_id": habit_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@addictionsense_bp.route("/emergency-contacts", methods=["GET"])
def get_emergency_contacts():
    return jsonify({
        "helplines": [
            {
                "title": "National Drug De-Addiction Helpline",
                "number": "1800-11-0031",
                "available": "24/7 Toll-Free",
                "description": "National Helpline for Substance Abuse & Rehabilitation."
            },
            {
                "title": "Emergency Medical Services",
                "number": "112 / 108",
                "available": "24/7 Instant Emergency",
                "description": "Immediate medical intervention for acute overdose or severe distress."
            },
            {
                "title": "Tele-MANAS Mental Health Helpline",
                "number": "14416",
                "available": "24/7 Toll-Free Support",
                "description": "Comprehensive Tele-Mental Health Assistance and Counseling Network."
            }
        ]
    }), 200
