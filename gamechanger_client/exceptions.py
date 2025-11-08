# -*- coding: utf-8 -*-
"""
Package exceptions.
"""

import logging
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class GameChangerException(Exception):
    """
    Base class for all GameChanger package exceptions.
    """

    pass


class ApiError(GameChangerException):
    """
    Errors returned in response to requests sent to the GameChanger APIs.

    Several data attributes are available for inspection.
    """

    def __init__(self, response):
        """Create an instance of the APIError class."""
        assert isinstance(response, requests.Response)

        # Extended exception attributes
        self.response = response
        """The :class:`requests.Response` object returned from the API call."""

        self.request = self.response.request
        """The :class:`requests.PreparedRequest` of the API call."""

        self.status_code = self.response.status_code
        """The HTTP status code from the API response."""

        self.status = self.response.reason
        """The HTTP status from the API response."""

        self.details = None
        """The parsed JSON details from the API response."""
        if 'application/json' in self.response.headers.get('Content-Type', '').lower():
            try:
                self.details = self.response.json()
            except ValueError:
                logger.warning('Error parsing JSON response body')

        if self.details:
            if 'error' in self.details.keys():
                self.message = self.details.get('error')
            elif 'message' in self.details.keys():
                self.message = self.details.get('message')
        else:
            self.message = None
        """The error message from the parsed API response."""

        super().__init__(
            '[{status_code}]{status} - {message}'.format(
                status_code=self.status_code,
                status=' ' + self.status if self.status else '',
                message=self.message or 'Unknown Error',
            )
        )

    def __repr__(self):
        return '<{exception_name} [{status_code}]>'.format(
            exception_name=self.__class__.__name__,
            status_code=self.status_code,
        )


class MalformedResponse(GameChangerException):
    """Raised when a malformed response is received from GameChanger."""

    pass


class SchemaValidationError(ApiError):
    """
    Raised when the API returns a 400 response due to schema validation errors.
    
    This exception provides detailed information about what fields are invalid,
    what the expected schema looks like, and suggestions for fixing the issues.
    """

    def __init__(self, response):
        """Create an instance of the SchemaValidationError class."""
        # Initialize schema validation specific attributes first
        self.schema = None
        self.validation_errors = []
        self.invalid_fields = []
        self.suggested_fixes = []
        
        # Store response info we'll need
        assert isinstance(response, requests.Response)
        self.response = response
        self.request = self.response.request
        self.status_code = self.response.status_code
        self.status = self.response.reason
        
        # Parse response details
        self.details = None
        if 'application/json' in self.response.headers.get('Content-Type', '').lower():
            try:
                self.details = self.response.json()
            except ValueError:
                logger.warning('Error parsing JSON response body')
        
        # Set our custom message logic
        schema_message = "Schema validation failed"
        
        # Parse the response to extract schema details
        if self.details and isinstance(self.details, dict):
            self.schema = self.details.get('schema')
            self.validation_errors = self.details.get('errors', [])
            
            # Only update message if we actually have schema validation data
            if self.schema and self.validation_errors:
                # Parse validation errors to extract useful information
                self._parse_validation_errors()
                
                # Now set the proper message
                schema_message = self.get_user_friendly_message()
        
        # Set the message (this prevents parent class from overriding it)
        self.message = schema_message
        
        # Call the Exception base class directly to avoid ApiError's message logic
        GameChangerException.__init__(
            self,
            '[{status_code}]{status} - {message}'.format(
                status_code=self.status_code,
                status=' ' + self.status if self.status else '',
                message=self.message or 'Unknown Error',
            )
        )
    
    def _parse_validation_errors(self):
        """Parse the validation errors to extract user-friendly information."""
        for error in self.validation_errors:
            if not isinstance(error, dict):
                continue
                
            # Extract the field that caused the error
            instance_path = error.get('instancePath', '')
            keyword = error.get('keyword', '')
            params = error.get('params', {})
            message = error.get('message', '')
            
            # Handle different types of validation errors
            if keyword == 'additionalProperties':
                additional_prop = params.get('additionalProperty')
                if additional_prop:
                    self.invalid_fields.append(additional_prop)
                    self.suggested_fixes.append(
                        f"Remove the '{additional_prop}' field as it's not allowed by the API schema"
                    )
                    
            elif keyword == 'required':
                missing_prop = params.get('missingProperty')
                if missing_prop:
                    self.invalid_fields.append(missing_prop)
                    self.suggested_fixes.append(
                        f"Add the required '{missing_prop}' field"
                    )
                    
            elif keyword == 'type':
                expected_type = params.get('type')
                field_path = instance_path.lstrip('/')
                if field_path:
                    self.invalid_fields.append(field_path)
                    self.suggested_fixes.append(
                        f"Field '{field_path}' should be of type '{expected_type}'"
                    )
                    
            elif keyword == 'enum':
                allowed_values = params.get('allowedValues', [])
                field_path = instance_path.lstrip('/')
                if field_path and allowed_values:
                    self.invalid_fields.append(field_path)
                    self.suggested_fixes.append(
                        f"Field '{field_path}' must be one of: {', '.join(map(str, allowed_values))}"
                    )
    
    def get_user_friendly_message(self) -> str:
        """Get a user-friendly error message with suggestions."""
        if not self.validation_errors:
            return "Schema validation failed, but no specific errors were provided."
        
        message_parts = ["API request failed schema validation:"]
        
        for i, fix in enumerate(self.suggested_fixes, 1):
            message_parts.append(f"  {i}. {fix}")
            
        if self.invalid_fields:
            message_parts.append(f"\nInvalid fields: {', '.join(set(self.invalid_fields))}")
            
        return '\n'.join(message_parts)
    
    def get_allowed_fields(self) -> List[str]:
        """Extract allowed fields from the schema."""
        if not self.schema or not isinstance(self.schema, dict):
            return []
            
        properties = self.schema.get('properties', {})
        return list(properties.keys())
    
    def get_required_fields(self) -> List[str]:
        """Extract required fields from the schema."""
        if not self.schema or not isinstance(self.schema, dict):
            return []
            
        return self.schema.get('required', [])
    
    def get_field_info(self, field_name: str) -> Dict[str, Any]:
        """Get information about a specific field from the schema."""
        if not self.schema or not isinstance(self.schema, dict):
            return {}
            
        properties = self.schema.get('properties', {})
        return properties.get(field_name, {})
    
    def __str__(self):
        """Override string representation to show user-friendly message."""
        return self.get_user_friendly_message()
