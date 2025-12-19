"""
Date validation module
Now supports multiple common date formats for cross-browser compatibility
"""
from datetime import datetime
from typing import Tuple


class DateValidationError(Exception):
    """Date validation error"""
    pass


def validate_birth_date(date_string: str) -> Tuple[bool, str]:
    """
    Validate birth date format
    
    Supports multiple common date formats for cross-browser compatibility:
    - ISO 8601: YYYY-MM-DD (Chrome default)
    - US format: MM/DD/YYYY (Safari may input)
    - European format: DD/MM/YYYY (some regions)
    
    Args:
        date_string: Date string in one of the supported formats
        
    Returns:
        (is_valid, error_message or success_message)
    """
    if not date_string or not isinstance(date_string, str):
        return False, "Date cannot be empty"
    
    # Try multiple common date formats to support cross-browser compatibility
    date_formats = [
        "%Y-%m-%d",  # ISO 8601 format (Chrome default)
        "%m/%d/%Y",  # US format (Safari may input)
        "%d/%m/%Y",  # European format (some regions)
    ]
    
    date_obj = None
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_string, fmt)
            break  # Successfully parsed, exit loop
        except ValueError:
            continue  # Try next format
    
    if date_obj is None:
        # None of the formats worked
        return False, f"Invalid date format. Supported formats: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY. Received: {date_string}"
    
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
