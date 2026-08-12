from utils.database import mysql


def create_medication(patient_id, doctor_id, medication_name, dosage, frequency, start_date, end_date=None, status="ACTIVE"):
    cur = mysql.connection.cursor()

    query = """
    INSERT INTO medications (patient_id, doctor_id, medication_name, dosage, frequency, start_date, end_date, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        patient_id,
        doctor_id,
        medication_name,
        dosage,
        frequency,
        start_date,
        end_date,
        status
    ))

    mysql.connection.commit()
    med_id = cur.lastrowid
    cur.close()

    return med_id


def get_patient_medications(patient_id):
    cur = mysql.connection.cursor()

    query = """
    SELECT m.medication_id, m.patient_id, m.doctor_id, du.full_name AS doctor_name,
           m.medication_name, m.dosage, m.frequency, m.start_date, m.end_date, m.status
    FROM medications m
    JOIN doctors d ON m.doctor_id = d.doctor_id
    JOIN users du ON d.user_id = du.user_id
    WHERE m.patient_id = %s
    ORDER BY m.start_date DESC
    """

    cur.execute(query, (patient_id,))
    rows = cur.fetchall()
    cur.close()

    result = []
    for row in rows:
        result.append({
            "medication_id": row[0],
            "patient_id": row[1],
            "doctor_id": row[2],
            "doctor_name": row[3],
            "medication_name": row[4],
            "dosage": row[5],
            "frequency": row[6],
            "start_date": str(row[7]),
            "end_date": str(row[8]) if row[8] else None,
            "status": row[9]
        })

    return result


def update_medication(medication_id, medication_name, dosage, frequency, status):
    cur = mysql.connection.cursor()

    query = """
    UPDATE medications
    SET medication_name = %s, dosage = %s, frequency = %s, status = %s
    WHERE medication_id = %s
    """

    cur.execute(query, (medication_name, dosage, frequency, status, medication_id))
    mysql.connection.commit()
    rows = cur.rowcount
    cur.close()

    return rows > 0


def delete_medication(medication_id):
    cur = mysql.connection.cursor()

    query = "DELETE FROM medications WHERE medication_id = %s"
    cur.execute(query, (medication_id,))
    mysql.connection.commit()
    rows = cur.rowcount
    cur.close()

    return rows > 0
