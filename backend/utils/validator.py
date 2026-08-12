"""
Validation Helpers for Request Payloads
"""
import re

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, str(email)) is not None

def validate_required_fields(data, required_fields):
    if not isinstance(data, dict):
        return False, ["Invalid payload format"]
    missing = [field for field in required_fields if field not in data or data[field] is None or str(data[field]).strip() == ""]
    if missing:
        return False, [f"Missing required field: {field}" for field in missing]
    return True, []
