"""
API integration tests
Test complete registration workflow
"""
import pytest
import json
from src.app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestRegistrationAPI:
    """Registration API test class"""
    
    def test_health_check(self, client):
        """✅ Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
    
    def test_register_with_chrome_date_format(self, client):
        """✅ Test registration with Chrome date format - should succeed"""
        payload = {
            "username": "chromeuser",
            "email": "chrome@test.com",
            "birth_date": "1995-08-20"  # Chrome: YYYY-MM-DD
        }
        
        response = client.post(
            '/api/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'user_id' in data
    
    def test_register_with_safari_date_format(self, client):
        """❌ Test registration with Safari date format - currently fails"""
        payload = {
            "username": "safariuser",
            "email": "safari@test.com",
            "birth_date": "08/20/1995"  # Safari: MM/DD/YYYY
        }
        
        response = client.post(
            '/api/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Expected: 201 Created (success)
        # Actual: 400 Bad Request (failure)
        assert response.status_code == 201, \
            f"Safari date format should be accepted, but returned error: {response.status_code}"
        
        data = json.loads(response.data)
        assert data['success'] is True, \
            f"Registration should succeed, but returned error: {data.get('errors', [])}"
    
    def test_register_with_european_date_format(self, client):
        """❌ Test registration with European date format - currently fails"""
        payload = {
            "username": "europeanuser",
            "email": "eu@test.com",
            "birth_date": "20/08/1995"  # European: DD/MM/YYYY
        }
        
        response = client.post(
            '/api/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Expected: Should succeed
        # Actual: Fails
        assert response.status_code == 201, \
            "European date format should be accepted"
    
    def test_register_with_missing_data(self, client):
        """✅ Test registration with missing data - should fail"""
        payload = {
            "username": "testuser"
            # Missing email and birth_date
        }
        
        response = client.post(
            '/api/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_register_with_invalid_json(self, client):
        """✅ Test invalid JSON - should fail"""
        response = client.post(
            '/api/register',
            data="not json",
            content_type='application/json'
        )
        
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
