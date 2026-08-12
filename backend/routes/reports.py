import io
from flask import Blueprint, send_file, jsonify, request
from services.report_service import get_summary_report, get_patient_report_data
from reports.pdf_generator import generate_patient_pdf_report

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/summary", methods=["GET"])
def summary():
    """
    Get aggregated system recovery summary & analytics report
    """
    return get_summary_report()


@reports_bp.route("/patient/<int:patient_id>/pdf", methods=["GET"])
def download_patient_pdf(patient_id):
    """
    Generates and returns downloadable clinical PDF report for a patient
    """
    patient_data = get_patient_report_data(patient_id)
    if not patient_data:
        return jsonify({"error": "Patient not found"}), 404

    pdf_bytes = generate_patient_pdf_report(patient_data)
    
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"AddictionSense_Clinical_Report_PAT_{patient_id}.pdf"
    )
