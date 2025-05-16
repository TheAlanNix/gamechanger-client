import pytest

from gamechanger_client.http_session import HttpSession

@pytest.fixture
def auth_token():
    """Provide a test authentication token."""
    return "test_auth_token"

@pytest.fixture
def base_url():
    """Provide a test base URL."""
    return "https://api.gc.com"

@pytest.fixture
def api_version():
    """Provide a test API version."""
    return "v1"

@pytest.fixture
def http_session(auth_token, base_url, api_version):
    """Create a test HTTP session with mock configuration."""
    return HttpSession(
        gc_token=auth_token,
    )
