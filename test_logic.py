import pytest
from unittest.mock import patch, MagicMock
from app import SYSTEM_INSTRUCTION, get_representatives

def test_system_prompt_safety_rules():
    """Validates that core non-partisan rules exist."""
    instruction_lower = SYSTEM_INSTRUCTION.lower()
    assert "non-partisan" in instruction_lower
    assert "bias" in instruction_lower
    
def test_app_architecture_files():
    """Validates deployment readiness."""
    import os
    assert os.path.exists("Dockerfile")
    assert os.path.exists("requirements.txt")

# --- MOCKING INTEGRATION FLOWS & EDGE CASES ---

@patch('app.requests.get')
def test_get_representatives_success(mock_get):
    """Test successful API response parsing."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "officials": [{"name": "Jane Doe", "party": "Independent"}]
    }
    mock_get.return_value = mock_response
    
    result = get_representatives("123 Main St")
    assert "Jane Doe" in result
    assert "Independent" in result

@patch('app.requests.get')
def test_get_representatives_404_deprecation(mock_get):
    """Test handling of the 2025 Google Civic API deprecation (edge case)."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    result = get_representatives("1600 Pennsylvania Ave")
    assert "Deprecation Notice" in result

@patch('app.requests.get')
def test_get_representatives_500_error(mock_get):
    """Test handling of internal server errors."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    
    result = get_representatives("123 Main St")
    assert "API Error: 500" in result

def test_get_representatives_empty_address():
    """Test edge case for empty input."""
    assert "Error: Address cannot be empty." in get_representatives("")
    assert "Error: Address cannot be empty." in get_representatives("   ")
