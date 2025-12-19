#!/usr/bin/env python
"""
Test Flask API endpoints
Simulates real HTTP requests to verify the API works correctly
"""
import json
from src.app import app

print("=" * 70)
print("FLASK API ENDPOINT TESTS")
print("=" * 70)

# Create test client
app.config['TESTING'] = True
client = app.test_client()

api_tests = [
    {
        "name": "Health Check",
        "method": "GET",
        "endpoint": "/api/health",
        "data": None,
        "expected_status": 200,
    },
    {
        "name": "Register with Chrome (ISO Format)",
        "method": "POST",
        "endpoint": "/api/register",
        "data": {
            "username": "chromeuser",
            "email": "chrome@test.com",
            "birth_date": "1990-05-15"
        },
        "expected_status": 201,
    },
    {
        "name": "Register with Safari (US Format) - MAIN FIX TEST",
        "method": "POST",
        "endpoint": "/api/register",
        "data": {
            "username": "safariuser",
            "email": "safari@test.com",
            "birth_date": "05/15/1990"
        },
        "expected_status": 201,
    },
    {
        "name": "Register with European Format - MAIN FIX TEST",
        "method": "POST",
        "endpoint": "/api/register",
        "data": {
            "username": "euuser",
            "email": "eu@test.com",
            "birth_date": "15/05/1990"
        },
        "expected_status": 201,
    },
    {
        "name": "Register with Missing Data",
        "method": "POST",
        "endpoint": "/api/register",
        "data": {
            "username": "incomplete"
        },
        "expected_status": 400,
    },
    {
        "name": "Register with Invalid Email",
        "method": "POST",
        "endpoint": "/api/register",
        "data": {
            "username": "testuser",
            "email": "invalid-email",
            "birth_date": "1990-05-15"
        },
        "expected_status": 400,
    },
    {
        "name": "Register with Invalid Date Format",
        "method": "POST",
        "endpoint": "/api/register",
        "data": {
            "username": "testuser",
            "email": "test@test.com",
            "birth_date": "not-a-date"
        },
        "expected_status": 400,
    },
    {
        "name": "Register with Future Date",
        "method": "POST",
        "endpoint": "/api/register",
        "data": {
            "username": "testuser",
            "email": "test@test.com",
            "birth_date": "2030-01-01"
        },
        "expected_status": 400,
    },
    {
        "name": "Register with Invalid JSON",
        "method": "POST",
        "endpoint": "/api/register",
        "data": "not json",
        "is_invalid_json": True,
        "expected_status": 400,
    },
]

passed = 0
failed = 0

for test in api_tests:
    print(f"\n{'='*70}")
    print(f"Test: {test['name']}")
    print(f"Method: {test['method']} {test['endpoint']}")
    
    try:
        if test['method'] == 'GET':
            response = client.get(test['endpoint'])
        else:  # POST
            if test.get('is_invalid_json'):
                response = client.post(
                    test['endpoint'],
                    data=test['data'],
                    content_type='application/json'
                )
            else:
                response = client.post(
                    test['endpoint'],
                    data=json.dumps(test['data']),
                    content_type='application/json'
                )
        
        status_match = response.status_code == test['expected_status']
        status = "✅ PASS" if status_match else "❌ FAIL"
        
        if status_match:
            passed += 1
        else:
            failed += 1
        
        print(f"Status Code: {status} (Expected: {test['expected_status']}, Got: {response.status_code})")
        
        try:
            response_data = json.loads(response.data)
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response: {response.data.decode()}")
            
    except Exception as e:
        print(f"❌ FAIL | Exception: {str(e)}")
        failed += 1

print(f"\n{'='*70}")
print(f"API TEST RESULTS: {passed} PASSED, {failed} FAILED")
print(f"{'='*70}")
