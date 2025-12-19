# Cross-Browser Form Validation Fix - Minimal Reproduction Project

This is the fixed version of the minimal reproduction project demonstrating cross-browser date format compatibility issues.

## Summary
The backend date validation now accepts ISO (YYYY-MM-DD), US (MM/DD/YYYY), and European (DD/MM/YYYY) formats so users of Chrome, Safari, and Firefox can register successfully.

## Quick Start

Install dependencies and run tests:

```powershell
pip install -r requirements.txt
pytest tests/ -v
```

Start application:

```powershell
python src/app.py
```

Visit: http://localhost:5000
