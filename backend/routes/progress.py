from flask import Blueprint, request
from services.progress_service import (
    register_progress,
    fetch_all_progress,
    fetch_progress,
    edit_progress,
    remove_progress
)

progress_bp = Blueprint("progress", __name__)


@progress_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    return register_progress(
        data.get("patient_id"),
        data.get("progress_date"),
        data.get("mood"),
        data.get("craving_level"),
        data.get("withdrawal_level"),
        data.get("recovery_score"),
        data.get("counselor_notes")
    )


@progress_bp.route("/", methods=["GET"])
def get_progress():
    return fetch_all_progress()


@progress_bp.route("/<int:progress_id>", methods=["GET"])
def get_progress_by_id(progress_id):
    return fetch_progress(progress_id)


@progress_bp.route("/<int:progress_id>", methods=["PUT"])
def update_progress_route(progress_id):
    data = request.get_json() or {}

    return edit_progress(
        progress_id,
        data.get("patient_id"),
        data.get("progress_date"),
        data.get("mood"),
        data.get("craving_level"),
        data.get("withdrawal_level"),
        data.get("recovery_score"),
        data.get("counselor_notes")
    )


@progress_bp.route("/<int:progress_id>", methods=["DELETE"])
def delete_progress_route(progress_id):
    return remove_progress(progress_id)