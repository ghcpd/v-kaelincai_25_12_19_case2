# Cross-Browser Form Validation Compatibility Issue - Minimal Reproduction Project

## Scenario Description

This is a minimal reproduction project for an e-commerce website user registration form, demonstrating cross-browser date format compatibility issues:

- **Chrome Browser**: Uses HTML5 `<input type="date">` automatically formatted as `YYYY-MM-DD`, backend validation passes
- **Safari Browser**: Users may manually input `MM/DD/YYYY` format, causing backend validation failure
- **Impact**: Safari user registration success rate drops by 30%

## Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   ├── app.py              # Flask application main entry
│   ├── validators.py       # Date validation logic (issue location)
│   └── templates/
│       └── register.html   # Registration form page
├── tests/
│   ├── __init__.py
│   ├── test_validators.py  # Validator unit tests
│   └── test_api.py         # API integration tests
├── data/
│   └── sample_requests.json # Sample request data
├── requirements.txt
├── README.md
└── KNOWN_ISSUE.md          # Known issue documentation
```

## Quick Start

### 1. Install Dependencies and Run Tests

```powershell
# Install dependencies
pip install -r requirements.txt

# Run tests (currently will fail, demonstrating the issue)
pytest tests/ -v

# View test coverage
pytest tests/ --cov=src --cov-report=term-missing
```

### 2. Start Application

```powershell
python src/app.py
```

Visit: http://localhost:5000

### 3. Manual Testing

Open browser and visit http://localhost:5000, try entering dates in different formats:
- `2024-12-18` (Chrome format) - ✅ Success
- `12/18/2024` (Safari manual input) - ❌ Failed

## Issue Description

See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for details

## Tech Stack

- Python 3.8+
- Flask 3.0
- Pytest 7.4
- HTML5
