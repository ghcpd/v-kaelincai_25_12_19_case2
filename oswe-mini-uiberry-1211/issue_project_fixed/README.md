Issue Project (Fixed)

This is a fixed version of the original issue_project that addressed cross-browser
date format compatibility in the birth-date validator.

What's changed:
- src/validators.py: validate_birth_date now accepts ISO (YYYY-MM-DD),
  US (MM/DD/YYYY) and European (DD/MM/YYYY) formats.
- Added SOLUTION.md explaining the fix and verification.
- Updated sample_requests.json to reflect successful parsing of common formats.

To run tests:
- Create a virtualenv and install requirements.txt
- Run: pytest tests/ -v

All tests should pass (17 total).