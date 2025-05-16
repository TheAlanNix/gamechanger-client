import pytest

from gamechanger_client.config import (
    DEFAULT_ACCESS_TOKEN_EXPIRATION,
    DEFAULT_BASE_DOMAIN,
    DEFAULT_SUCCESS_RESPONSE_CODES
)

def test_config_constants():
    """Test configuration constants."""
    assert isinstance(DEFAULT_BASE_DOMAIN, str)
    assert DEFAULT_BASE_DOMAIN.startswith("api.")
    assert isinstance(DEFAULT_ACCESS_TOKEN_EXPIRATION, int)
    assert DEFAULT_ACCESS_TOKEN_EXPIRATION > 0
    assert isinstance(DEFAULT_SUCCESS_RESPONSE_CODES, list)
    assert all(isinstance(code, int) for code in DEFAULT_SUCCESS_RESPONSE_CODES)
    assert 200 in DEFAULT_SUCCESS_RESPONSE_CODES
