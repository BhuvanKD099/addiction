from flask import Blueprint, jsonify, request
from utils.database import mysql

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_notifications(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT notification_id, title, message, type, is_read, created_at
            FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 10
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()

        notifications = []
        for r in rows:
            notifications.append({
                "notification_id": r[0],
                "title": r[1],
                "message": r[2],
                "type": r[3],
                "is_read": bool(r[4]),
                "created_at": str(r[5])
            })
        return jsonify({"notifications": notifications}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
