"""
Date validation module (fixed)

This version accepts multiple common date formats so it is compatible with
different browsers (Chrome, Safari, Firefox) and regional input styles.

Accepted formats:
 - ISO 8601: YYYY-MM-DD
 - US style: MM/DD/YYYY
 - European style: DD/MM/YYYY
"""
from datetime import datetime
from typing import Tuple


class DateValidationError(Exception):
    """Date validation error"""
    pass


def _try_parse_date(date_string: str):
    """Try parsing the date string with several common formats.

    Returns a datetime object on success or raises ValueError if none match.
    """
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]
    last_error = None
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError as exc:
            last_error = exc
    raise last_error or ValueError("time data does not match any supported format")


def validate_birth_date(date_string: str) -> Tuple[bool, str]:
    """
    Validate birth date format and reasonable date values.

    This function now accepts ISO, US and European formatted dates to accommodate
    browser and regional differences (Safari often provides MM/DD/YYYY, some
    locales use DD/MM/YYYY, while Chrome tends to use YYYY-MM-DD).
    """
    if not date_string or not isinstance(date_string, str):
        return False, "Date cannot be empty"

    # Try parsing with any supported format
    try:
        date_obj = _try_parse_date(date_string)
    except ValueError:
        return False, (
            "Invalid date format, supported formats: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY"
            f", received: {date_string}"
        )

    # Check if future date (do this first so message for future dates is specific)
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

    Args:
        username: Username
        email: Email address
        birth_date: Birth date

    Returns:
        Validation result dictionary
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