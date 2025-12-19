"""
Manual API testing script
Tests the registration API with different date formats
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test health check endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_registration(date_format_name, birth_date):
    """Test registration with specific date format"""
    print(f"\n=== Testing {date_format_name} ===")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "birth_date": birth_date
    }
    response = requests.post(
        f"{BASE_URL}/api/register",
        json=data
    )
    print(f"Date: {birth_date}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201

if __name__ == "__main__":
    print("Starting Manual API Tests...")
    
    try:
        # Test health check
        health_ok = test_health()
        
        # Test different date formats
        iso_ok = test_registration("ISO Format (Chrome)", "1990-05-15")
        us_ok = test_registration("US Format (Safari)", "05/15/1990")
        eu_ok = test_registration("European Format", "15/05/1990")
        
        # Summary
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
        print(f"ISO Format: {'✅ PASS' if iso_ok else '❌ FAIL'}")
        print(f"US Format: {'✅ PASS' if us_ok else '❌ FAIL'}")
        print(f"European Format: {'✅ PASS' if eu_ok else '❌ FAIL'}")
        
        all_passed = health_ok and iso_ok and us_ok and eu_ok
        print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the Flask server is running on http://127.0.0.1:5000")
