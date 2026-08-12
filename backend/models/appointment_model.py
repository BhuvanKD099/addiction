from utils.database import mysql


def create_appointment(
    patient_id,
    doctor_id,
    appointment_date,
    appointment_time,
    status,
    notes
):

    cur = mysql.connection.cursor()

    query = """
    INSERT INTO appointments(
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status,
        notes
    )
    VALUES(%s,%s,%s,%s,%s,%s)
    """

    cur.execute(query, (
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status,
        notes
    ))

    mysql.connection.commit()

    appointment_id = cur.lastrowid

    cur.close()

    return appointment_id


def get_all_appointments():

    cur = mysql.connection.cursor()

    query = """
    SELECT

        a.appointment_id,

        p.patient_id,
        pu.full_name,

        d.doctor_id,
        du.full_name,

        a.appointment_date,
        a.appointment_time,
        a.status,
        a.notes

    FROM appointments a

    JOIN patients p
        ON a.patient_id = p.patient_id

    JOIN users pu
        ON p.user_id = pu.user_id

    JOIN doctors d
        ON a.doctor_id = d.doctor_id

    JOIN users du
        ON d.user_id = du.user_id

    ORDER BY
        a.appointment_date DESC,
        a.appointment_time DESC
    """

    cur.execute(query)

    appointments = cur.fetchall()

    cur.close()

    return appointments


def get_appointment_by_id(appointment_id):

    cur = mysql.connection.cursor()

    query = """
    SELECT

        appointment_id,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status,
        notes

    FROM appointments

    WHERE appointment_id=%s
    """

    cur.execute(query, (appointment_id,))

    appointment = cur.fetchone()

    cur.close()

    return appointment


def update_appointment(
    appointment_id,
    patient_id,
    doctor_id,
    appointment_date,
    appointment_time,
    status,
    notes
):

    cur = mysql.connection.cursor()

    query = """
    UPDATE appointments
    SET

        patient_id=%s,
        doctor_id=%s,
        appointment_date=%s,
        appointment_time=%s,
        status=%s,
        notes=%s

    WHERE appointment_id=%s
    """

    cur.execute(query, (
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status,
        notes,
        appointment_id
    ))

    mysql.connection.commit()

    rows = cur.rowcount

    cur.close()

    return rows > 0


def delete_appointment(appointment_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM appointments WHERE appointment_id=%s",
        (appointment_id,)
    )

    mysql.connection.commit()

    rows = cur.rowcount

    cur.close()

    return rows > 0