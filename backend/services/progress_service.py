from models.progress_model import (
    create_progress,
    get_all_progress,
    get_progress_by_id,
    update_progress,
    delete_progress
)

from models.patient_model import get_patient_by_id


def register_progress(
    patient_id,
    progress_date,
    mood,
    craving_level,
    withdrawal_level,
    recovery_score,
    counselor_notes
):

    if not get_patient_by_id(patient_id):
        return {
            "error": "Patient not found"
        }, 404

    progress_id = create_progress(
        patient_id,
        progress_date,
        mood,
        craving_level,
        withdrawal_level,
        recovery_score,
        counselor_notes
    )

    return {
        "message": "Progress added successfully",
        "progress_id": progress_id
    }, 201


def fetch_all_progress():

    progress = get_all_progress()

    result = []

    for item in progress:

        result.append({

            "progress_id": item[0],

            "patient": {
                "patient_id": item[1],
                "name": item[2]
            },

            "progress_date": str(item[3]),
            "mood": item[4],
            "craving_level": item[5],
            "withdrawal_level": item[6],
            "recovery_score": item[7],
            "counselor_notes": item[8]

        })

    return result, 200


def fetch_progress(progress_id):

    progress = get_progress_by_id(progress_id)

    if not progress:
        return {
            "error": "Progress record not found"
        }, 404

    return {

        "progress_id": progress[0],
        "patient_id": progress[1],
        "progress_date": str(progress[2]),
        "mood": progress[3],
        "craving_level": progress[4],
        "withdrawal_level": progress[5],
        "recovery_score": progress[6],
        "counselor_notes": progress[7]

    }, 200


def edit_progress(
    progress_id,
    patient_id,
    progress_date,
    mood,
    craving_level,
    withdrawal_level,
    recovery_score,
    counselor_notes
):

    if not get_patient_by_id(patient_id):
        return {
            "error": "Patient not found"
        }, 404

    updated = update_progress(
        progress_id,
        patient_id,
        progress_date,
        mood,
        craving_level,
        withdrawal_level,
        recovery_score,
        counselor_notes
    )

    if not updated:
        return {
            "error": "Progress record not found"
        }, 404

    return {
        "message": "Progress updated successfully"
    }, 200


def remove_progress(progress_id):

    deleted = delete_progress(progress_id)

    if not deleted:
        return {
            "error": "Progress record not found"
        }, 404

    return {
        "message": "Progress deleted successfully"
    }, 200