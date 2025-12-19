"""
Date validation module
Issue: Only accepts ISO 8601 format (YYYY-MM-DD), does not handle other common formats
"""
from datetime import datetime
from typing import Tuple


class DateValidationError(Exception):
    """Date validation error"""
    pass


def validate_birth_date(date_string: str) -> Tuple[bool, str]:
    """
    Validate birth date format
    
    Issue: This function only accepts YYYY-MM-DD format
    In Safari browser, users may input MM/DD/YYYY format, causing validation failure
    
    Args:
        date_string: Date string
        
    Returns:
        (is_valid, error_message or success_message)
    """
    if not date_string or not isinstance(date_string, str):
        return False, "Date cannot be empty"
    
    # Issue: Only attempts to parse ISO 8601 format (YYYY-MM-DD)
    # Does not handle MM/DD/YYYY, DD/MM/YYYY and other common formats
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        # Returns failure directly, does not try other formats
        return False, f"Invalid date format, must be YYYY-MM-DD format, received: {date_string}"
    
    # Check if date is within reasonable range
    current_year = datetime.now().year
    if date_obj.year < 1900 or date_obj.year > current_year:
        return False, f"Birth year must be between 1900 and {current_year}"
    
    # Check if future date
    if date_obj > datetime.now():
        return False, "Birth date cannot be in the future"
    
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
