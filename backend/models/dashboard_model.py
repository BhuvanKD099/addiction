from utils.database import mysql

def get_dashboard_stats():

    cur = mysql.connection.cursor()

    # Total Patients
    cur.execute("SELECT COUNT(*) FROM patients")
    patients = cur.fetchone()[0]

    # Total Doctors
    cur.execute("SELECT COUNT(*) FROM doctors")
    doctors = cur.fetchone()[0]

    # Total Appointments
    cur.execute("SELECT COUNT(*) FROM appointments")
    appointments = cur.fetchone()[0]

    cur.close()

    return patients, doctors, appointments
def get_patient_dashboard(patient_id):
    cur = mysql.connection.cursor()

    query = """
    SELECT
        u.full_name AS patient_name,
        du.full_name AS doctor_name,
        p.addiction_type,
        p.addiction_severity,

        dp.mood,
        dp.sleep_hours,
        dp.craving_level,
        dp.medication_compliance,
        dp.counselling_attended,

        a.appointment_date,
        a.appointment_time

    FROM patients p

    JOIN users u
        ON p.user_id = u.user_id

    JOIN doctors d
        ON p.doctor_id = d.doctor_id

    JOIN users du
        ON d.user_id = du.user_id

    LEFT JOIN daily_progress dp
        ON p.patient_id = dp.patient_id

    LEFT JOIN appointments a
        ON p.patient_id = a.patient_id

    WHERE p.patient_id = %s

    ORDER BY dp.progress_date DESC,
             a.appointment_date ASC

    LIMIT 1;
    """

    cur.execute(query, (patient_id,))
    result = cur.fetchone()

    cur.close()

    return result