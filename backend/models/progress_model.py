from utils.database import mysql


def create_progress(
    patient_id,
    progress_date,
    mood,
    craving_level,
    withdrawal_level,
    recovery_score,
    counselor_notes
):

    cur = mysql.connection.cursor()

    query = """
    INSERT INTO progress(
        patient_id,
        progress_date,
        mood,
        craving_level,
        withdrawal_level,
        recovery_score,
        counselor_notes
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s)
    """

    cur.execute(query, (

        patient_id,
        progress_date,
        mood,
        craving_level,
        withdrawal_level,
        recovery_score,
        counselor_notes

    ))

    mysql.connection.commit()

    progress_id = cur.lastrowid

    cur.close()

    return progress_id


def get_all_progress():

    cur = mysql.connection.cursor()

    query = """
    SELECT

        p.progress_id,

        pt.patient_id,
        u.full_name,

        p.progress_date,
        p.mood,
        p.craving_level,
        p.withdrawal_level,
        p.recovery_score,
        p.counselor_notes

    FROM progress p

    JOIN patients pt
        ON p.patient_id = pt.patient_id

    JOIN users u
        ON pt.user_id = u.user_id

    ORDER BY p.progress_date DESC
    """

    cur.execute(query)

    progress = cur.fetchall()

    cur.close()

    return progress


def get_progress_by_id(progress_id):

    cur = mysql.connection.cursor()

    query = """
    SELECT

        progress_id,
        patient_id,
        progress_date,
        mood,
        craving_level,
        withdrawal_level,
        recovery_score,
        counselor_notes

    FROM progress

    WHERE progress_id=%s
    """

    cur.execute(query, (progress_id,))

    progress = cur.fetchone()

    cur.close()

    return progress


def update_progress(

    progress_id,
    patient_id,
    progress_date,
    mood,
    craving_level,
    withdrawal_level,
    recovery_score,
    counselor_notes

):

    cur = mysql.connection.cursor()

    query = """
    UPDATE progress

    SET

        patient_id=%s,
        progress_date=%s,
        mood=%s,
        craving_level=%s,
        withdrawal_level=%s,
        recovery_score=%s,
        counselor_notes=%s

    WHERE progress_id=%s
    """

    cur.execute(query, (

        patient_id,
        progress_date,
        mood,
        craving_level,
        withdrawal_level,
        recovery_score,
        counselor_notes,
        progress_id

    ))

    mysql.connection.commit()

    rows = cur.rowcount

    cur.close()

    return rows > 0


def delete_progress(progress_id):

    cur = mysql.connection.cursor()

    cur.execute(

        "DELETE FROM progress WHERE progress_id=%s",

        (progress_id,)

    )

    mysql.connection.commit()

    rows = cur.rowcount

    cur.close()

    return rows > 0