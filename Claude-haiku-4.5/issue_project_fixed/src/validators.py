"""
Date validation module - FIXED VERSION
Now accepts multiple common date formats for cross-browser compatibility
"""
from datetime import datetime
from typing import Tuple


class DateValidationError(Exception):
    """Date validation error"""
    pass


def validate_birth_date(date_string: str) -> Tuple[bool, str]:
    """
    Validate birth date format with support for multiple common formats
    
    Supported formats:
    - ISO 8601: YYYY-MM-DD (1990-05-15)
    - US format: MM/DD/YYYY (05/15/1990)
    - European format: DD/MM/YYYY (15/05/1990)
    
    Args:
        date_string: Date string in any of the supported formats
        
    Returns:
        (is_valid, error_message or success_message)
    """
    if not date_string or not isinstance(date_string, str):
        return False, "Date cannot be empty"
    
    # List of date formats to try, in order of preference
    date_formats = [
        "%Y-%m-%d",      # ISO 8601: 1990-05-15
        "%m/%d/%Y",      # US: 05/15/1990
        "%d/%m/%Y",      # European: 15/05/1990
    ]
    
    date_obj = None
    
    # Try to parse the date string with each format
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_string, fmt)
            break  # Successfully parsed, exit loop
        except ValueError:
            continue  # Try next format
    
    # If no format matched, return error
    if date_obj is None:
        return False, f"Invalid date format. Supported formats: YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY. Received: {date_string}"
    
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
