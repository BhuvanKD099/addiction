"""
Utility Helper Functions for API Response Formatting and Date Handling
"""
from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    payload = {"status": "success", "message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code

def error_response(message="An error occurred", status_code=400, errors=None):
    payload = {"status": "error", "error": message}
    if errors is not None:
        payload["details"] = errors
    return jsonify(payload), status_code
