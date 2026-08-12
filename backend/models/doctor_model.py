from utils.database import mysql


def create_doctor(user_id, specialization, phone, experience_years, qualification):

    cur = mysql.connection.cursor()

    query = """
    INSERT INTO doctors
    (user_id, specialization, phone, experience_years, qualification)
    VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        user_id,
        specialization,
        phone,
        experience_years,
        qualification
    ))

    mysql.connection.commit()
    cur.close()


def get_all_doctors():

    cur = mysql.connection.cursor()

    query = """
    SELECT
        d.doctor_id,
        u.full_name,
        u.email,
        d.specialization,
        d.phone,
        d.experience_years,
        d.qualification
    FROM doctors d
    INNER JOIN users u
        ON d.user_id = u.user_id
    ORDER BY d.doctor_id
    """

    cur.execute(query)

    doctors = cur.fetchall()

    cur.close()

    return doctors


def doctor_exists(doctor_id):

    print("Received doctor_id:", doctor_id, type(doctor_id))

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT doctor_id FROM doctors WHERE doctor_id=%s",
        (doctor_id,)
    )

    doctor = cur.fetchone()

    print("Query Result:", doctor)

    cur.close()

    return doctor


def get_user_id_from_doctor(doctor_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT user_id FROM doctors WHERE doctor_id=%s",
        (doctor_id,)
    )

    result = cur.fetchone()

    cur.close()

    if result is None:
        return None

    return result[0]


def update_doctor(
    user_id,
    full_name,
    specialization,
    phone,
    experience_years,
    qualification
):

    cur = mysql.connection.cursor()

    # Update users table
    cur.execute(
        """
        UPDATE users
        SET full_name=%s
        WHERE user_id=%s
        """,
        (
            full_name,
            user_id
        )
    )

    # Update doctors table
    cur.execute(
        """
        UPDATE doctors
        SET
            specialization=%s,
            phone=%s,
            experience_years=%s,
            qualification=%s
        WHERE user_id=%s
        """,
        (
            specialization,
            phone,
            experience_years,
            qualification,
            user_id
        )
    )

    mysql.connection.commit()

    cur.close()
def delete_doctor(doctor_id):

    cur = mysql.connection.cursor()

    # Get user_id before deleting
    cur.execute(
        "SELECT user_id FROM doctors WHERE doctor_id=%s",
        (doctor_id,)
    )

    result = cur.fetchone()

    if result is None:
        cur.close()
        return False

    user_id = result[0]

    # Delete from doctors
    cur.execute(
        "DELETE FROM doctors WHERE doctor_id=%s",
        (doctor_id,)
    )

    # Delete corresponding user
    cur.execute(
        "DELETE FROM users WHERE user_id=%s",
        (user_id,)
    )

    mysql.connection.commit()
    cur.close()

    return True