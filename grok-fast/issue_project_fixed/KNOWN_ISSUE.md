# Known Issue Documentation

## Issue Type

**Date Format Validation Defect - Missing Cross-Browser Format Compatibility Handling**

## Issue Description

### Root Cause
The backend date validator (`src/validators.py`) only accepts **ISO 8601 format** (`YYYY-MM-DD`), without handling other common date formats, preventing Safari and other browser users from registering successfully.

### Affected Files and Locations

**Main Issue Point:**
- File: [src/validators.py](src/validators.py)
- Function: `validate_birth_date()`
- Line Numbers: **Lines 28-34**

```python
# Problem code snippet (Lines 28-34)
try:
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
except ValueError:
    # Returns failure directly, does not try other formats
    return False, f"Invalid date format, must be YYYY-MM-DD format, received: {date_string}"
```

## Trigger Conditions

### Scenario 1: Safari Browser Users
- **Browser**: Safari (macOS/iOS)
- **User Action**: Manually input `05/15/1990` (US format) in date field
- **Expected Behavior**: System should recognize and accept this format, successful registration
- **Actual Behavior**: Returns `"Invalid date format, must be YYYY-MM-DD format"`, registration fails

### Scenario 2: European Region Users
- **Date Convention**: Use `DD/MM/YYYY` format (e.g., `15/05/1990`)
- **Expected Behavior**: System should recognize and accept this format
- **Actual Behavior**: Validation fails, cannot register

### Scenario 3: Other Browsers
- **Firefox/Edge**: May also input non-ISO formats under certain configurations
- **Mobile Devices**: Different operating systems have different default date formats

## Reproduction Tests

### Running Failed Tests

```powershell
# Run all tests (view failed tests)
pytest tests/ -v

# Run specific failed tests
pytest tests/test_validators.py::TestDateValidation::test_us_format_date_fails -v
pytest tests/test_api.py::TestRegistrationAPI::test_register_with_safari_date_format -v
```

### Current Test Results

❌ **Expected Failed Tests** (5 total):
1. `test_us_format_date_fails` - Safari US format date
2. `test_european_format_date_fails` - European format date
3. `test_registration_with_safari_date_format_fails` - Safari complete registration flow
4. `test_register_with_safari_date_format` - Safari API test
5. `test_register_with_european_date_format` - European format API test

✅ **Should Pass Tests** (8 total):
- All ISO format tests
- Invalid data validation tests

## Business Impact

### Statistics
- **Impact Scope**: Safari users, European region users
- **Safari Market Share**: ~18% (desktop) + ~27% (mobile)
- **Estimated Impact**: Registration success rate drops by **30%**

### User Experience Issues
1. Users receive error messages after inputting dates according to their habits
2. Unfriendly error messages, users don't know how to correct
3. Leads to user churn, affects conversion rate

## Fix Approaches

### Approach 1: Multi-Format Parsing Attempt (Recommended)
Modify `validate_birth_date()` function to try multiple date formats:

```python
def validate_birth_date(date_string: str) -> Tuple[bool, str]:
    date_formats = [
        "%Y-%m-%d",      # ISO 8601: 1990-05-15
        "%m/%d/%Y",      # US: 05/15/1990
        "%d/%m/%Y",      # European: 15/05/1990
        "%Y/%m/%d",      # Alternative ISO
        "%d-%m-%Y",      # Alternative European
    ]
    
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_string, fmt)
            # Continue with subsequent validation...
            return True, "Date format is valid"
        except ValueError:
            continue
    
    return False, f"Unable to recognize date format: {date_string}"
```

### Approach 2: Use Third-Party Library
Use `python-dateutil` library's `parser.parse()` for automatic format recognition:

```python
from dateutil import parser

def validate_birth_date(date_string: str) -> Tuple[bool, str]:
    try:
        date_obj = parser.parse(date_string, dayfirst=False)
        # Continue validation...
    except (ValueError, parser.ParserError):
        return False, f"Unable to parse date: {date_string}"
```

### Approach 3: Frontend Unified Formatting
In frontend JavaScript, convert all date formats to ISO format before sending:

```javascript
const dateInput = document.getElementById('birthDate').value;
const date = new Date(dateInput);
const isoDate = date.toISOString().split('T')[0]; // YYYY-MM-DD
```

## Expected Fix Results

After fix, all 5 failed tests should pass:
```
tests/test_validators.py::TestDateValidation::test_us_format_date_fails PASSED
tests/test_validators.py::TestDateValidation::test_european_format_date_fails PASSED
tests/test_validators.py::TestRegistrationValidation::test_registration_with_safari_date_format_fails PASSED
tests/test_api.py::TestRegistrationAPI::test_register_with_safari_date_format PASSED
tests/test_api.py::TestRegistrationAPI::test_register_with_european_date_format PASSED
```

## Related Standards

- **ISO 8601**: International standard date format `YYYY-MM-DD`
- **RFC 3339**: Internet date-time format
- **HTML5 Date Input**: Specification requires `value` to be `YYYY-MM-DD`

## References

- [MDN: HTML Date Input](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date)
- [Can I Use: Date Input](https://caniuse.com/input-datetime)
- [Python strptime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
