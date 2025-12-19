"""
Date validation module - Fixed
Now accepts multiple common date formats (ISO, US, European)
"""
from datetime import datetime, date
from typing import Tuple


class DateValidationError(Exception):
    """Date validation error"""
    pass


def validate_birth_date(date_string: str) -> Tuple[bool, str]:
    """
    Validate birth date format

    Accepts the following formats:
      - ISO 8601: YYYY-MM-DD
      - US: MM/DD/YYYY
      - European: DD/MM/YYYY

    Returns (is_valid, message)
    """
    if not date_string or not isinstance(date_string, str):
        return False, "Date cannot be empty"

    # Try supported formats in a robust order
    supported_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]
    parsed = None
    for fmt in supported_formats:
        try:
            parsed = datetime.strptime(date_string, fmt).date()
            break
        except ValueError:
            continue

    if parsed is None:
        return False, (
            "Invalid date format, accepted formats: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY"
        )

    # Check if future date first (important for clear messaging)
    if parsed > date.today():
        return False, "Birth date cannot be in the future"

    # Check if date is within reasonable range
    current_year = date.today().year
    if parsed.year < 1900 or parsed.year > current_year:
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
