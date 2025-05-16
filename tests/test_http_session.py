import pytest
import responses

from gamechanger_client.exceptions import ApiError
from gamechanger_client.config import DEFAULT_BASE_DOMAIN
from gamechanger_client.http_session import HttpSession


@pytest.fixture
def http_session():
    """Create a test HTTP session."""
    return HttpSession(gc_token="test_token")

@responses.activate
def test_successful_get_request(http_session):
    """Test a successful GET request."""
    base_url = f"https://{DEFAULT_BASE_DOMAIN}"
    responses.add(
        responses.GET,
        f"{base_url}/test",
        json={"data": "test_response"},
        status=200
    )

    response = http_session.get(f"{base_url}/test")
    assert response.json() == {"data": "test_response"}

@responses.activate
def test_api_error(http_session):
    """Test handling of API errors."""
    base_url = f"https://{DEFAULT_BASE_DOMAIN}"
    responses.add(
        responses.GET,
        f"{base_url}/test",
        json={"error": "Internal server error"},
        status=500
    )
    
    with pytest.raises(ApiError):
        http_session.get(f"{base_url}/test")
