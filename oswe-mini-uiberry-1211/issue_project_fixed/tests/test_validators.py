"""
Date validator unit tests (copied from original) - no changes
"""
import pytest
from src.validators import validate_birth_date, validate_registration_data


class TestDateValidation:
    """Date validation test class"""
    
    def test_valid_iso_format_date(self):
        """✅ Test ISO format date (Chrome browser format) - should pass"""
        is_valid, message = validate_birth_date("1990-05-15")
        assert is_valid is True
        assert "valid" in message
    
    def test_us_format_date_fails(self):
        """❌ Test US format date (Safari may input) - currently fails"""
        # Safari users may input MM/DD/YYYY format
        is_valid, message = validate_birth_date("05/15/1990")
        
        # Expected: Should be accepted and parsed correctly
        # Actual: Rejected because validator only accepts YYYY-MM-DD format
        assert is_valid is True, f"Should accept US date format, but rejected: {message}"
    
    def test_european_format_date_fails(self):
        """❌ Test European format date - currently fails"""
        # Some region users may input DD/MM/YYYY format
        is_valid, message = validate_birth_date("15/05/1990")
        
        # Expected: Should be accepted and parsed correctly
        # Actual: Rejected
        assert is_valid is True, f"Should accept European date format, but rejected: {message}"
    
    def test_empty_date(self):
        """✅ Test empty date - should fail"""
        is_valid, message = validate_birth_date("")
        assert is_valid is False
        assert "empty" in message
    
    def test_invalid_date_format(self):
        """✅ Test completely invalid format - should fail"""
        is_valid, message = validate_birth_date("not-a-date")
        assert is_valid is False
    
    def test_future_date(self):
        """✅ Test future date - should fail"""
        is_valid, message = validate_birth_date("2030-01-01")
        assert is_valid is False
        assert "future" in message
    
    def test_very_old_date(self):
        """✅ Test very old date - should fail"""
        is_valid, message = validate_birth_date("1850-01-01")
        assert is_valid is False


class TestRegistrationValidation:
    """Complete registration data validation tests"""
    
    def test_valid_registration_chrome_format(self):
        """✅ Test complete registration with Chrome browser format - should pass"""
        result = validate_registration_data(
            username="testuser",
            email="test@example.com",
            birth_date="1990-05-15"
        )
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_registration_with_safari_date_format_fails(self):
        """❌ Test registration with Safari date format - currently fails"""
        # Simulate US date format input by Safari user
        result = validate_registration_data(
            username="safariuser",
            email="safari@example.com",
            birth_date="05/15/1990"  # Format Safari users may input
        )
        
        # Expected: Should succeed
        # Actual: Fails because date format is not accepted
        assert result["valid"] is True, \
            f"Safari date format should be accepted, but registration failed: {result['errors']}"
        assert len(result["errors"]) == 0
    
    def test_invalid_username(self):
        """✅ Test invalid username - should fail"""
        result = validate_registration_data(
            username="ab",  # Too short
            email="test@example.com",
            birth_date="1990-05-15"
        )
        assert result["valid"] is False
        assert any("Username" in err for err in result["errors"])
    
    def test_invalid_email(self):
        """✅ Test invalid email - should fail"""
        result = validate_registration_data(
            username="testuser",
            email="invalid-email",
            birth_date="1990-05-15"
        )
        assert result["valid"] is False
        assert any("email" in err for err in result["errors"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])