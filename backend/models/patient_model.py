from utils.database import mysql


def create_patient(
    user_id,
    doctor_id,
    age,
    gender,
    phone,
    address,
    emergency_contact,
    admission_date,
    addiction_type,
    addiction_severity
):
    cur = mysql.connection.cursor()

    query = """
    INSERT INTO patients(
        user_id,
        doctor_id,
        age,
        gender,
        phone,
        address,
        emergency_contact,
        admission_date,
        addiction_type,
        addiction_severity
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cur.execute(query, (
        user_id,
        doctor_id,
        age,
        gender,
        phone,
        address,
        emergency_contact,
        admission_date,
        addiction_type,
        addiction_severity
    ))

    mysql.connection.commit()

    patient_id = cur.lastrowid

    cur.close()

    return patient_id


def get_all_patients():

    cur = mysql.connection.cursor()

    query = """
    SELECT
        p.patient_id,
        u.full_name,
        u.email,
        d.doctor_id,
        du.full_name,
        p.age,
        p.gender,
        p.phone,
        p.addiction_type,
        p.addiction_severity,
        p.admission_date
    FROM patients p
    JOIN users u
        ON p.user_id = u.user_id
    LEFT JOIN doctors d
        ON p.doctor_id = d.doctor_id
    LEFT JOIN users du
        ON d.user_id = du.user_id
    ORDER BY p.patient_id
    """

    cur.execute(query)

    patients = cur.fetchall()

    cur.close()

    return patients


def get_patient_by_id(patient_id):

    cur = mysql.connection.cursor()

    query = """
    SELECT
        p.patient_id,
        u.full_name,
        u.email,

        d.doctor_id,
        du.full_name,
        d.specialization,

        p.age,
        p.gender,
        p.phone,
        p.address,
        p.emergency_contact,
        p.admission_date,
        p.addiction_type,
        p.addiction_severity

    FROM patients p

    JOIN users u
        ON p.user_id = u.user_id

    LEFT JOIN doctors d
        ON p.doctor_id = d.doctor_id

    LEFT JOIN users du
        ON d.user_id = du.user_id

    WHERE p.patient_id=%s
    """

    cur.execute(query, (patient_id,))

    patient = cur.fetchone()

    cur.close()

    return patient


def update_patient(
    patient_id,
    full_name,
    email,
    doctor_id,
    age,
    gender,
    phone,
    address,
    emergency_contact,
    admission_date,
    addiction_type,
    addiction_severity
):

    cur = mysql.connection.cursor()

    # Find user_id of this patient
    cur.execute(
        "SELECT user_id FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    result = cur.fetchone()

    if not result:
        cur.close()
        return False

    user_id = result[0]

    # Update users table
    cur.execute("""
        UPDATE users
        SET
            full_name=%s,
            email=%s
        WHERE user_id=%s
    """, (
        full_name,
        email,
        user_id
    ))

    # Update patients table
    cur.execute("""
        UPDATE patients
        SET
            doctor_id=%s,
            age=%s,
            gender=%s,
            phone=%s,
            address=%s,
            emergency_contact=%s,
            admission_date=%s,
            addiction_type=%s,
            addiction_severity=%s
        WHERE patient_id=%s
    """, (
        doctor_id,
        age,
        gender,
        phone,
        address,
        emergency_contact,
        admission_date,
        addiction_type,
        addiction_severity,
        patient_id
    ))

    mysql.connection.commit()

    cur.close()

    return True


def delete_patient(patient_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT user_id FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    result = cur.fetchone()

    if not result:
        cur.close()
        return False

    user_id = result[0]

    cur.execute(
        "DELETE FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    cur.execute(
        "DELETE FROM users WHERE user_id=%s",
        (user_id,)
    )

    mysql.connection.commit()

    cur.close()

    return True