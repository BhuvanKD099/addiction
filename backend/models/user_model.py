from utils.database import mysql


def get_user_by_email(email):
    cur = mysql.connection.cursor()

    query = """
        SELECT user_id, full_name, email, password_hash, role, status
        FROM users
        WHERE email = %s
    """

    cur.execute(query, (email,))
    user = cur.fetchone()

    cur.close()

    return user


def create_user(full_name, email, password_hash, role):
    cur = mysql.connection.cursor()

    query = """
    INSERT INTO users(full_name, email, password_hash, role)
    VALUES (%s,%s,%s,%s)
    """

    cur.execute(query, (
        full_name,
        email,
        password_hash,
        role
    ))

    mysql.connection.commit()

    user_id = cur.lastrowid

    cur.close()

    return user_id