# -*- coding: utf-8 -*-
"""
Package exceptions.
"""

import logging

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
