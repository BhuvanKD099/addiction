from flask import Blueprint
from services.dashboard_service import (
    patient_dashboard,
    dashboard_stats
)

dashboard_bp = Blueprint("dashboard", __name__)


# Patient Dashboard
@dashboard_bp.route("/patient/<int:patient_id>", methods=["GET"])
def dashboard(patient_id):
    return patient_dashboard(patient_id)


# Admin Dashboard Statistics
@dashboard_bp.route("/stats", methods=["GET"])
def stats():
    return dashboard_stats()