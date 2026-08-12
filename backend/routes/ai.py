import os
from flask import Blueprint, jsonify, send_file, request
from ai.retrain_model import retrain_and_evaluate_screening, retrain_relapse_model
from ai.dataset_manager import (
    SCREENING_CSV,
    RELAPSE_CSV,
    METADATA_JSON,
    _get_metadata
)

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/retrain/screening", methods=["POST"])
def retrain_screening():
    """
    Runs Section 13 Safe Retraining Pipeline:
    Evaluates candidate model on test set, computes Accuracy, Precision, Recall, F1, Confusion Matrix & ROC-AUC.
    Promotes candidate model ONLY if performance criteria is met; otherwise preserves previous best model.
    """
    result, status = retrain_and_evaluate_screening()
    return jsonify(result), status


@ai_bp.route("/retrain/relapse", methods=["POST"])
def retrain_relapse():
    result, status = retrain_relapse_model()
    return jsonify(result), status


@ai_bp.route("/dataset-info", methods=["GET"])
def dataset_info():
    screening_count = 0
    relapse_count = 0

    if os.path.exists(SCREENING_CSV):
        with open(SCREENING_CSV, "r", encoding="utf-8") as f:
            screening_count = max(0, sum(1 for line in f) - 1)

    if os.path.exists(RELAPSE_CSV):
        with open(RELAPSE_CSV, "r", encoding="utf-8") as f:
            relapse_count = max(0, sum(1 for line in f) - 1)

    meta = _get_metadata()

    return jsonify({
        "dataset_version": meta.get("dataset_version", "v1.0.0"),
        "screening_samples": screening_count,
        "relapse_samples": relapse_count,
        "total_dataset_records": screening_count + relapse_count,
        "consent_required": True,
        "anonymized": True,
        "screening_csv_path": SCREENING_CSV,
        "relapse_csv_path": RELAPSE_CSV
    }), 200


@ai_bp.route("/download-dataset/<dataset_type>", methods=["GET"])
def download_dataset(dataset_type):
    if dataset_type == "screening":
        if not os.path.exists(SCREENING_CSV):
            return jsonify({"error": "Screening dataset file not found"}), 404
        return send_file(SCREENING_CSV, as_attachment=True, download_name="realtime_multimodal_screening_dataset.csv")
    elif dataset_type == "relapse":
        if not os.path.exists(RELAPSE_CSV):
            return jsonify({"error": "Relapse dataset file not found"}), 404
        return send_file(RELAPSE_CSV, as_attachment=True, download_name="realtime_relapse_prediction_dataset.csv")
    else:
        return jsonify({"error": "Invalid dataset type requested"}), 400
