from flask import Blueprint, request, jsonify
from utils.database import mysql
from datetime import date

counselling_bp = Blueprint("counselling", __name__)

@counselling_bp.route("/patient/<int:patient_id>", methods=["GET"])
def get_patient_counseling_sessions(patient_id):
    try:
        cur = mysql.connection.cursor()
        query = """
        SELECT session_id, patient_id, counselor_id, session_date, discussion_topics,
               patient_participation, mood_assessment, session_summary, recommendations,
               homework, next_session_date, created_at
        FROM counseling_sessions
        WHERE patient_id = %s
        ORDER BY session_date DESC
        """
        cur.execute(query, (patient_id,))
        rows = cur.fetchall()
        cur.close()

        sessions = []
        for r in rows:
            sessions.append({
                "session_id": r[0],
                "patient_id": r[1],
                "counselor_id": r[2],
                "session_date": str(r[3]),
                "discussion_topics": r[4],
                "patient_participation": r[5],
                "mood_assessment": r[6],
                "session_summary": r[7],
                "recommendations": r[8],
                "homework": r[9],
                "next_session_date": str(r[10]) if r[10] else None,
                "created_at": str(r[11])
            })
        return jsonify({"patient_id": patient_id, "sessions": sessions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@counselling_bp.route("/", methods=["POST"])
def create_counseling_session():
    data = request.get_json() or {}
    patient_id = data.get("patient_id", 1)
    counselor_id = data.get("counselor_id", 1)
    session_date = data.get("session_date", str(date.today()))
    discussion_topics = data.get("discussion_topics", "")
    patient_participation = data.get("patient_participation", "ACTIVE")
    mood_assessment = data.get("mood_assessment", "STABLE")
    session_summary = data.get("session_summary", "")
    recommendations = data.get("recommendations", "")
    homework = data.get("homework", "")
    next_session_date = data.get("next_session_date", None)

    try:
        cur = mysql.connection.cursor()
        query = """
        INSERT INTO counseling_sessions
        (patient_id, counselor_id, session_date, discussion_topics, patient_participation, mood_assessment, session_summary, recommendations, homework, next_session_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            patient_id, counselor_id, session_date, discussion_topics,
            patient_participation, mood_assessment, session_summary,
            recommendations, homework, next_session_date
        ))
        mysql.connection.commit()
        session_id = cur.lastrowid
        cur.close()

        return jsonify({
            "message": "Counseling session logged successfully",
            "session_id": session_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@counselling_bp.route("/<int:session_id>", methods=["PUT"])
def update_counseling_session(session_id):
    data = request.get_json() or {}
    session_date = data.get("session_date", str(date.today()))
    discussion_topics = data.get("discussion_topics", "")
    patient_participation = data.get("patient_participation", "ACTIVE")
    mood_assessment = data.get("mood_assessment", "STABLE")
    session_summary = data.get("session_summary", "")
    recommendations = data.get("recommendations", "")
    homework = data.get("homework", "")
    next_session_date = data.get("next_session_date", None)

    try:
        cur = mysql.connection.cursor()
        query = """
        UPDATE counseling_sessions
        SET session_date=%s, discussion_topics=%s, patient_participation=%s,
            mood_assessment=%s, session_summary=%s, recommendations=%s,
            homework=%s, next_session_date=%s
        WHERE session_id=%s
        """
        cur.execute(query, (
            session_date, discussion_topics, patient_participation,
            mood_assessment, session_summary, recommendations,
            homework, next_session_date, session_id
        ))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Counseling session updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@counselling_bp.route("/<int:session_id>", methods=["DELETE"])
def delete_counseling_session(session_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM counseling_sessions WHERE session_id=%s", (session_id,))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Counseling session deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

