import pytest
import requests

from gamechanger_client.exceptions import ApiError, MalformedResponse

def test_api_error():
    """Test ApiError exception."""
    response = requests.Response()
    response.status_code = 500
    response._content = b'{"error": "Test error"}'
    with pytest.raises(ApiError) as exc_info:
        raise ApiError(response)
    assert isinstance(exc_info.value, ApiError)

def test_malformed_response_error():
    """Test MalformedResponse exception."""
    error_msg = "Test malformed response"
    with pytest.raises(MalformedResponse) as exc_info:
        raise MalformedResponse(error_msg)
    assert str(exc_info.value) == error_msg
