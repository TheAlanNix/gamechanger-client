import json
import pytest
import responses

from gamechanger_client.exceptions import ApiError, SchemaValidationError
from gamechanger_client.config import DEFAULT_BASE_DOMAIN
from gamechanger_client.http_session import HttpSession


@pytest.fixture
def http_session():
    """Create a test HTTP session."""
    return HttpSession(gc_token="test_token")


@pytest.fixture
def base_url():
    """Get the base URL for API requests."""
    return f"https://{DEFAULT_BASE_DOMAIN}"


class TestHttpSession:
    """Test the HttpSession class."""

    @responses.activate
    def test_successful_get_request(self, http_session, base_url):
        """Test a successful GET request."""
        responses.add(
            responses.GET,
            f"{base_url}/test",
            json={"data": "test_response"},
            status=200
        )

        response = http_session.get(f"{base_url}/test")
        assert response.json() == {"data": "test_response"}

    @responses.activate
    def test_successful_post_request(self, http_session, base_url):
        """Test a successful POST request."""
        responses.add(
            responses.POST,
            f"{base_url}/test",
            json={"created": True, "id": "123"},
            status=201
        )

        response = http_session.post(f"{base_url}/test", json={"name": "test"})
        assert response.json() == {"created": True, "id": "123"}

    @responses.activate
    def test_api_error_500(self, http_session, base_url):
        """Test handling of 500 API errors."""
        responses.add(
            responses.GET,
            f"{base_url}/test",
            json={"error": "Internal server error"},
            status=500
        )
        
        with pytest.raises(ApiError) as exc_info:
            http_session.get(f"{base_url}/test")
        
        error = exc_info.value
        assert error.status_code == 500
        assert error.message == "Internal server error"

    @responses.activate
    def test_api_error_400_regular(self, http_session, base_url):
        """Test handling of regular 400 errors (non-schema validation)."""
        responses.add(
            responses.POST,
            f"{base_url}/test",
            json={"message": "Bad request"},
            status=400
        )
        
        with pytest.raises(ApiError) as exc_info:
            http_session.post(f"{base_url}/test", json={"invalid": "data"})
        
        error = exc_info.value
        assert error.status_code == 400
        assert error.message == "Bad request"
        assert not isinstance(error, SchemaValidationError)

    @responses.activate
    def test_schema_validation_error(self, http_session, base_url):
        """Test handling of schema validation errors."""
        schema_response = {
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sport": {"type": "string"}
                },
                "required": ["name"],
                "additionalProperties": False
            },
            "errors": [
                {
                    "instancePath": "",
                    "schemaPath": "#/additionalProperties",
                    "keyword": "additionalProperties",
                    "params": {"additionalProperty": "page"},
                    "message": "must NOT have additional properties"
                }
            ]
        }
        
        responses.add(
            responses.POST,
            f"{base_url}/search",
            json=schema_response,
            status=400
        )
        
        with pytest.raises(SchemaValidationError) as exc_info:
            http_session.post(f"{base_url}/search", json={"name": "test", "page": 0})
        
        error = exc_info.value
        assert error.status_code == 400
        assert "page" in error.invalid_fields
        assert "Remove the 'page' field" in error.suggested_fixes[0]

    @responses.activate
    def test_is_schema_validation_error_detection(self, http_session, base_url):
        """Test schema validation error detection method."""
        # Test with schema validation response
        schema_response = {
            "schema": {"type": "object"},
            "errors": [{"keyword": "additionalProperties"}]
        }
        responses.add(
            responses.POST,
            f"{base_url}/test1",
            json=schema_response,
            status=400
        )
        
        with pytest.raises(SchemaValidationError):
            http_session.post(f"{base_url}/test1", json={})

    @responses.activate
    def test_is_not_schema_validation_error(self, http_session, base_url):
        """Test that regular 400 errors are not treated as schema validation."""
        # Regular 400 error without schema/errors structure
        responses.add(
            responses.POST,
            f"{base_url}/test2",
            json={"error": "Bad request"},
            status=400
        )
        
        with pytest.raises(ApiError) as exc_info:
            http_session.post(f"{base_url}/test2", json={})
        
        # Should be regular ApiError, not SchemaValidationError
        assert not isinstance(exc_info.value, SchemaValidationError)

    @responses.activate
    def test_patch_request(self, http_session, base_url):
        """Test PATCH request functionality."""
        responses.add(
            responses.PATCH,
            f"{base_url}/test/123",
            json={"updated": True, "id": "123"},
            status=200
        )

        response = http_session.patch(f"{base_url}/test/123", json={"name": "updated"})
        assert response.json() == {"updated": True, "id": "123"}

    @responses.activate
    def test_put_request(self, http_session, base_url):
        """Test PUT request functionality."""
        responses.add(
            responses.PUT,
            f"{base_url}/test/123",
            json={"replaced": True, "id": "123"},
            status=200
        )

        response = http_session.put(f"{base_url}/test/123", json={"name": "replaced"})
        assert response.json() == {"replaced": True, "id": "123"}

    @responses.activate
    def test_delete_request(self, http_session, base_url):
        """Test DELETE request functionality."""
        responses.add(
            responses.DELETE,
            f"{base_url}/test/123",
            body="Deleted successfully",
            status=200
        )

        response = http_session.delete(f"{base_url}/test/123")
        assert response.text == "Deleted successfully"
