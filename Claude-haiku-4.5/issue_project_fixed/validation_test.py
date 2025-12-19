#!/usr/bin/env python
"""
Comprehensive validation test for fixed date validators
Tests all supported date formats and edge cases
"""
from src.validators import validate_birth_date, validate_registration_data

print("=" * 70)
print("COMPREHENSIVE DATE FORMAT VALIDATION TEST")
print("=" * 70)

test_cases = [
    ("1990-05-15", "ISO 8601 Format", True),
    ("05/15/1990", "US Format (MM/DD/YYYY)", True),
    ("15/05/1990", "European Format (DD/MM/YYYY)", True),
    ("", "Empty String", False),
    ("not-a-date", "Invalid String", False),
    ("2030-01-01", "Future Date", False),
    ("1850-01-01", "Very Old Date", False),
    ("1995-12-25", "Valid ISO Date", True),
    ("12/25/1995", "Valid US Date", True),
    ("25/12/1995", "Valid European Date", True),
]

passed = 0
failed = 0

for test_input, description, expected_valid in test_cases:
    is_valid, message = validate_birth_date(test_input)
    status = "✅ PASS" if is_valid == expected_valid else "❌ FAIL"
    
    if is_valid == expected_valid:
        passed += 1
    else:
        failed += 1
    
    print(f"\n{status} | {description}")
    print(f"      Input: '{test_input}'")
    print(f"      Expected: {expected_valid}, Got: {is_valid}")
    print(f"      Message: {message}")

print("\n" + "=" * 70)
print(f"VALIDATION RESULTS: {passed} PASSED, {failed} FAILED")
print("=" * 70)

# Test registration data validation
print("\n\n" + "=" * 70)
print("REGISTRATION DATA VALIDATION TEST")
print("=" * 70)

registration_tests = [
    {
        "name": "Valid Chrome Registration (ISO)",
        "username": "chromeuser",
        "email": "chrome@test.com",
        "birth_date": "1990-05-15",
        "should_pass": True
    },
    {
        "name": "Valid Safari Registration (US Format)",
        "username": "safariuser",
        "email": "safari@test.com",
        "birth_date": "05/15/1990",
        "should_pass": True
    },
    {
        "name": "Valid European Registration (EU Format)",
        "username": "euuser",
        "email": "eu@test.com",
        "birth_date": "15/05/1990",
        "should_pass": True
    },
    {
        "name": "Invalid - Username Too Short",
        "username": "ab",
        "email": "test@test.com",
        "birth_date": "1990-05-15",
        "should_pass": False
    },
    {
        "name": "Invalid - Bad Email",
        "username": "testuser",
        "email": "invalid-email",
        "birth_date": "1990-05-15",
        "should_pass": False
    },
    {
        "name": "Invalid - Bad Date Format",
        "username": "testuser",
        "email": "test@test.com",
        "birth_date": "not-a-date",
        "should_pass": False
    }
]

reg_passed = 0
reg_failed = 0

for test in registration_tests:
    result = validate_registration_data(
        test["username"],
        test["email"],
        test["birth_date"]
    )
    
    is_valid = result["valid"]
    expected = test["should_pass"]
    status = "✅ PASS" if is_valid == expected else "❌ FAIL"
    
    if is_valid == expected:
        reg_passed += 1
    else:
        reg_failed += 1
    
    print(f"\n{status} | {test['name']}")
    print(f"      Expected Pass: {expected}, Got: {is_valid}")
    if result["errors"]:
        print(f"      Errors: {result['errors']}")

print("\n" + "=" * 70)
print(f"REGISTRATION RESULTS: {reg_passed} PASSED, {reg_failed} FAILED")
print("=" * 70)

# Overall summary
total_passed = passed + reg_passed
total_failed = failed + reg_failed
print(f"\n{'='*70}")
print(f"OVERALL: {total_passed} PASSED, {total_failed} FAILED")
print(f"{'='*70}")
