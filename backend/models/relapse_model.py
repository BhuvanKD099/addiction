import json
from utils.database import mysql


def save_relapse_assessment(patient_id, risk_level, risk_score, triggers, recommendations):
    cur = mysql.connection.cursor()

    triggers_str = json.dumps(triggers) if isinstance(triggers, list) else str(triggers)
    recs_str = json.dumps(recommendations) if isinstance(recommendations, list) else str(recommendations)

    query = """
    INSERT INTO relapse_assessments (patient_id, risk_level, risk_score, triggers, recommendations)
    VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(query, (patient_id, risk_level, risk_score, triggers_str, recs_str))
    mysql.connection.commit()

    assessment_id = cur.lastrowid
    cur.close()

    return assessment_id


def get_patient_relapse_history(patient_id):
    cur = mysql.connection.cursor()

    query = """
    SELECT assessment_id, patient_id, assessment_date, risk_level, risk_score, triggers, recommendations
    FROM relapse_assessments
    WHERE patient_id = %s
    ORDER BY assessment_date DESC
    """

    cur.execute(query, (patient_id,))
    rows = cur.fetchall()
    cur.close()

    result = []
    for row in rows:
        triggers = row[5]
        recs = row[6]
        try:
            triggers = json.loads(triggers)
        except Exception:
            pass
        try:
            recs = json.loads(recs)
        except Exception:
            pass

        result.append({
            "assessment_id": row[0],
            "patient_id": row[1],
            "assessment_date": str(row[2]),
            "risk_level": row[3],
            "risk_score": row[4],
            "triggers": triggers,
            "recommendations": recs
        })

    return result


def get_latest_relapse_assessment(patient_id):
    cur = mysql.connection.cursor()

    query = """
    SELECT assessment_id, patient_id, assessment_date, risk_level, risk_score, triggers, recommendations
    FROM relapse_assessments
    WHERE patient_id = %s
    ORDER BY assessment_date DESC
    LIMIT 1
    """

    cur.execute(query, (patient_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        return None

    triggers = row[5]
    recs = row[6]
    try:
        triggers = json.loads(triggers)
    except Exception:
        pass
    try:
        recs = json.loads(recs)
    except Exception:
        pass

    return {
        "assessment_id": row[0],
        "patient_id": row[1],
        "assessment_date": str(row[2]),
        "risk_level": row[3],
        "risk_score": row[4],
        "triggers": triggers,
        "recommendations": recs
    }
