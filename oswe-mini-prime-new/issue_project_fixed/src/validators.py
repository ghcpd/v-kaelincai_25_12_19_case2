"""
Date validation module - Fixed
Now accepts multiple common formats: ISO (YYYY-MM-DD), US (MM/DD/YYYY), European (DD/MM/YYYY)
"""
from datetime import datetime
from typing import Tuple


class DateValidationError(Exception):
    """Date validation error"""
    pass


def _try_parse_date(date_string: str):
    """Try multiple date formats and return a datetime instance or raise ValueError"""
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    raise ValueError("unrecognized date format")


def validate_birth_date(date_string: str) -> Tuple[bool, str]:
    """
    Validate birth date format and basic business rules.

    Accepts:
      - ISO 8601: YYYY-MM-DD
      - US: MM/DD/YYYY
      - European: DD/MM/YYYY

    Returns (is_valid, message)
    """
    if not date_string or not isinstance(date_string, str):
        return False, "Date cannot be empty"

    ds = date_string.strip()

    try:
        date_obj = _try_parse_date(ds)
    except ValueError:
        return False, f"Invalid date format, expected YYYY-MM-DD, MM/DD/YYYY or DD/MM/YYYY, received: {date_string}"

# Check if future date
    if date_obj > datetime.now():
        return False, "Birth date cannot be in the future"

    # Check if date is within reasonable range
    current_year = datetime.now().year
    if date_obj.year < 1900 or date_obj.year > current_year:
        return False, f"Birth year must be between 1900 and {current_year}"

    return True, "Date format is valid"


def validate_registration_data(username: str, email: str, birth_date: str) -> dict:
    """
    Validate complete registration data
    """
    errors = []

    # Validate username
    if not username or len(username) < 3:
        errors.append("Username must be at least 3 characters")

    # Validate email
    if not email or "@" not in email:
        errors.append("Invalid email format")

    # Validate birth date
    is_valid, message = validate_birth_date(birth_date)
    if not is_valid:
        errors.append(message)

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
