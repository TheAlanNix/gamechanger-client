import json
import pytest
import requests

from gamechanger_client.exceptions import ApiError, MalformedResponse, SchemaValidationError


class MockResponse(requests.Response):
    """Mock response class for testing that inherits from requests.Response."""
    def __init__(self, status_code, json_data=None, headers=None):
        super().__init__()
        self.status_code = status_code
        self.reason = "Test Reason"
        self._json_data = json_data or {}
        self.headers = headers or {}
        self._content = json.dumps(json_data).encode() if json_data else b''
        
        # Create a mock request object
        self.request = requests.PreparedRequest()
        self.request.method = "POST"
        self.request.url = "https://api.test.com/endpoint"
    
    def json(self):
        if self._json_data:
            return self._json_data
        raise ValueError("No JSON object could be decoded")


class TestApiError:
    """Test the ApiError exception class."""

    def test_api_error_with_error_field(self):
        """Test ApiError with 'error' field in response."""
        response = MockResponse(
            status_code=500,
            json_data={"error": "Test error message"},
            headers={"Content-Type": "application/json"}
        )
        
        with pytest.raises(ApiError) as exc_info:
            raise ApiError(response)
        
        error = exc_info.value
        assert error.status_code == 500
        assert error.message == "Test error message"
        assert "Test error message" in str(error)

    def test_api_error_with_message_field(self):
        """Test ApiError with 'message' field in response."""
        response = MockResponse(
            status_code=400,
            json_data={"message": "Bad request message"},
            headers={"Content-Type": "application/json"}
        )
        
        with pytest.raises(ApiError) as exc_info:
            raise ApiError(response)
        
        error = exc_info.value
        assert error.message == "Bad request message"

    def test_api_error_no_json_content(self):
        """Test ApiError when response has no JSON content."""
        response = MockResponse(status_code=404)
        
        with pytest.raises(ApiError) as exc_info:
            raise ApiError(response)
        
        error = exc_info.value
        assert error.message is None
        assert "Unknown Error" in str(error)

    def test_api_error_invalid_json(self):
        """Test ApiError with invalid JSON response."""
        response = MockResponse(
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
        response._content = b'invalid json{'
        
        with pytest.raises(ApiError) as exc_info:
            raise ApiError(response)
        
        error = exc_info.value
        assert error.message is None


class TestSchemaValidationError:
    """Test the SchemaValidationError exception class."""

    def test_schema_validation_error_with_additional_properties(self):
        """Test SchemaValidationError with additional properties error."""
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
                    "params": {"additionalProperty": "invalid_field"},
                    "message": "must NOT have additional properties"
                }
            ]
        }
        
        response = MockResponse(
            status_code=400,
            json_data=schema_response,
            headers={"Content-Type": "application/json"}
        )
        
        with pytest.raises(SchemaValidationError) as exc_info:
            raise SchemaValidationError(response)
        
        error = exc_info.value
        assert "invalid_field" in error.invalid_fields
        assert "Remove the 'invalid_field' field" in error.suggested_fixes[0]
        assert "API request failed schema validation" in error.message

    def test_schema_validation_error_with_required_field(self):
        """Test SchemaValidationError with missing required field."""
        schema_response = {
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sport": {"type": "string"}
                },
                "required": ["name", "sport"],
                "additionalProperties": False
            },
            "errors": [
                {
                    "instancePath": "",
                    "schemaPath": "#/required",
                    "keyword": "required",
                    "params": {"missingProperty": "sport"},
                    "message": "must have required property 'sport'"
                }
            ]
        }
        
        response = MockResponse(
            status_code=400,
            json_data=schema_response,
            headers={"Content-Type": "application/json"}
        )
        
        with pytest.raises(SchemaValidationError) as exc_info:
            raise SchemaValidationError(response)
        
        error = exc_info.value
        assert "sport" in error.invalid_fields
        assert "Add the required 'sport' field" in error.suggested_fixes[0]

    def test_schema_validation_error_with_type_mismatch(self):
        """Test SchemaValidationError with type mismatch."""
        schema_response = {
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "year": {"type": "number"}
                },
                "required": ["name"],
                "additionalProperties": False
            },
            "errors": [
                {
                    "instancePath": "/year",
                    "schemaPath": "#/properties/year/type",
                    "keyword": "type",
                    "params": {"type": "number"},
                    "message": "must be number"
                }
            ]
        }
        
        response = MockResponse(
            status_code=400,
            json_data=schema_response,
            headers={"Content-Type": "application/json"}
        )
        
        with pytest.raises(SchemaValidationError) as exc_info:
            raise SchemaValidationError(response)
        
        error = exc_info.value
        assert "year" in error.invalid_fields
        assert "should be of type 'number'" in error.suggested_fixes[0]

    def test_schema_validation_error_with_enum_violation(self):
        """Test SchemaValidationError with enum violation."""
        schema_response = {
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "season": {
                        "type": "string",
                        "enum": ["spring", "summer", "fall", "winter"]
                    }
                },
                "required": ["name"],
                "additionalProperties": False
            },
            "errors": [
                {
                    "instancePath": "/season",
                    "schemaPath": "#/properties/season/enum",
                    "keyword": "enum",
                    "params": {"allowedValues": ["spring", "summer", "fall", "winter"]},
                    "message": "must be equal to one of the allowed values"
                }
            ]
        }
        
        response = MockResponse(
            status_code=400,
            json_data=schema_response,
            headers={"Content-Type": "application/json"}
        )
        
        with pytest.raises(SchemaValidationError) as exc_info:
            raise SchemaValidationError(response)
        
        error = exc_info.value
        assert "season" in error.invalid_fields
        assert "spring, summer, fall, winter" in error.suggested_fixes[0]

    def test_get_allowed_fields(self):
        """Test getting allowed fields from schema."""
        schema_response = {
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sport": {"type": "string"},
                    "city": {"type": "string"}
                },
                "required": ["name"]
            },
            "errors": []
        }
        
        response = MockResponse(
            status_code=400,
            json_data=schema_response,
            headers={"Content-Type": "application/json"}
        )
        
        error = SchemaValidationError(response)
        allowed_fields = error.get_allowed_fields()
        assert "name" in allowed_fields
        assert "sport" in allowed_fields
        assert "city" in allowed_fields

    def test_get_required_fields(self):
        """Test getting required fields from schema."""
        schema_response = {
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sport": {"type": "string"}
                },
                "required": ["name", "sport"]
            },
            "errors": []
        }
        
        response = MockResponse(
            status_code=400,
            json_data=schema_response,
            headers={"Content-Type": "application/json"}
        )
        
        error = SchemaValidationError(response)
        required_fields = error.get_required_fields()
        assert "name" in required_fields
        assert "sport" in required_fields

    def test_get_field_info(self):
        """Test getting field information from schema."""
        schema_response = {
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "year": {"type": "number", "minimum": 2000}
                },
                "required": ["name"]
            },
            "errors": []
        }
        
        response = MockResponse(
            status_code=400,
            json_data=schema_response,
            headers={"Content-Type": "application/json"}
        )
        
        error = SchemaValidationError(response)
        name_info = error.get_field_info("name")
        year_info = error.get_field_info("year")
        
        assert name_info["type"] == "string"
        assert year_info["type"] == "number"
        assert year_info["minimum"] == 2000

    def test_schema_validation_error_no_schema_data(self):
        """Test SchemaValidationError with no schema data."""
        response = MockResponse(
            status_code=400,
            json_data={"error": "Bad request"},
            headers={"Content-Type": "application/json"}
        )
        
        error = SchemaValidationError(response)
        assert "Schema validation failed" in error.message
        assert error.get_allowed_fields() == []
        assert error.get_required_fields() == []


class TestMalformedResponse:
    """Test the MalformedResponse exception class."""

    def test_malformed_response_error(self):
        """Test MalformedResponse exception."""
        error_msg = "Test malformed response"
        with pytest.raises(MalformedResponse) as exc_info:
            raise MalformedResponse(error_msg)
        assert str(exc_info.value) == error_msg
