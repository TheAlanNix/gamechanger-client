# -*- coding: utf-8 -*-
"""
HttpSession class for package HTTP functions.
"""

import json
import logging
import requests

from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from gamechanger_client import version
from gamechanger_client.config import (
    DEFAULT_ACCESS_TOKEN_EXPIRATION,
    DEFAULT_BASE_DOMAIN,
    DEFAULT_SUCCESS_RESPONSE_CODES,
)
from gamechanger_client.exceptions import ApiError, MalformedResponse

logger = logging.getLogger('gamechanger-client.http-session')


class HttpSession:
    """
    Package HttpSession class.
    """

    _gc_token = None

    def __init__(self, gc_token, base_domain=None):
        """
            Initializes the HttpSession object.

        Args:
            gc_token (str): a GameChanger token
            base_domain (str): a domain (defaults to "api.team-manager.gc.com")

        Returns:
            HttpSession: An instance of this class
        """

        super().__init__()

        # Create a requests session
        self._session = self._retry_session()

        # Set the base parameters
        self._base_domain = base_domain or DEFAULT_BASE_DOMAIN

        self._base_url = f"https://{self._base_domain}"

        self._gc_token = gc_token
        # Get an access token
        self._check_access_token()

    def _retry_session(
        self,
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=None,
    ):
        """
        A method to set up automatic retries on HTTP requests that fail.
        """

        # Create a new requests session
        session = requests.Session()

        # Establish the retry criteria
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=allowed_methods,
            raise_on_status=False,
        )

        # Build the adapter with the retry criteria
        adapter = HTTPAdapter(max_retries=retry_strategy)

        # Bind the adapter to HTTP/HTTPS calls
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _check_access_token(self):
        """
        A method to check the validity of the access token.
        """
        if self._gc_token:
            # TODO: I want to add some token checking here later on with automatic refresh
            return

    def _check_response_code(self, response, expected_response_codes):
        """
        Check the requests.response.status_code to make sure it's one that we expected.
        """
        if response.status_code in DEFAULT_SUCCESS_RESPONSE_CODES:
            pass
        # elif response.status_code == RATE_LIMIT_RESPONSE_CODE:
        #     raise RateLimitError(response)
        else:
            print(response.raw)
            raise ApiError(response)

    def _print_debug_response(self, response):
        """
        Print the debug logging, based on the returned content type.
        """

        logger.debug(response.headers)

        # If it's supposed to be a JSON response, parse and log, otherwise, log the raw text
        if "application/json" in response.headers.get("Content-Type", "").lower():
            try:
                if response.status_code != 204:
                    logger.debug(json.dumps(response.json(), indent=2))
                else:
                    logger.debug("204 No Content Returned")
            except ValueError:
                logger.warning("Error parsing JSON response body")
        else:
            logger.debug(response.text)

    def _get_gc_token(self):
        """
        A method to fetch a new token from GameChanger.

        Returns:
            str: a GameChanger token
        """

        raise NotImplementedError

    def _get_request_headers(self, org_access=False):
        """
        A method to build the HTTP request headers for GameChanger.

        Args:
            org_access (bool): Whether the request should be performed at the Organization level
        """

        # Build the request headers
        headers = self._session.headers

        headers['gc-token'] = self._gc_token
        headers['user-agent'] = 'gamechanger-python-client'
        headers['x-pagination'] = 'true'

        logger.debug('Request headers: \n' + json.dumps(dict(headers), indent=2))

        return headers

    def _request(self, method, uri, **kwargs):
        """
        A method to abstract building requests to GameChanger.

        Args:
            method (str): The HTTP request method ("GET", "POST", ...)
            uri (str): The URI of the API endpoint
            kwargs (Any): passed on to the requests package

        Returns:
            requests.models.Response: a Requests response object

        Raises:
             ApiError if anything but expected response code is returned
        """

        self._check_access_token()

        logger.info(f"{method} request to URI: {uri}")

        headers = self._get_request_headers()

        # Check for 'data' or 'json'
        data = kwargs.get("data", "")
        json = kwargs.get("json", "")
        if data or json:
            logger.debug(f"{method} request data:\nData: {data}\nJSON: {json}")

        # Make the HTTP request to the API endpoint
        response = self._session.request(method, uri, headers=headers, **kwargs)

        # Validate the response
        self._print_debug_response(response)
        self._check_response_code(response, DEFAULT_SUCCESS_RESPONSE_CODES)

        return response

    def get(self, uri, params=None, **kwargs):
        """
        A method to build a GET request to interact with GameChanger.

        Args:
            uri (str): uri to send the HTTP GET request to
            params (dict): parameters for the HTTP request
            kwargs (Any): passed on to the requests package

        Returns:
            requests.models.Response: a Requests response object

        Raises:
             ApiError if anything but expected response code is returned
        """

        # Perform a GET request
        response = self._request("GET", uri, params=params, **kwargs)

        return response

    def patch(self, uri, data=None, json=None, **kwargs):
        """
        A method to build a PATCH request to interact with GameChanger.

        Args:
            uri (str): uri to send the HTTP POST request to
            data (Any) : data to be sent in the body of the request
            json (dict): data to be sent in JSON format in the body of the request
            kwargs (Any): passed on to the requests package

        Returns:
            requests.models.Response: a Requests response object

        Raises:
             ApiError if anything but expected response code is returned
        """

        # Perform a PATCH request
        response = self._request("PATCH", uri, data=data, json=json, **kwargs)

        return response

    def post(self, uri, data=None, json=None, **kwargs):
        """
        A method to build a POST request to interact with GameChanger.

        Args:
            uri (str): uri to send the HTTP POST request to
            data (Any) : data to be sent in the body of the request
            json (dict): data to be sent in JSON format in the body of the request
            kwargs (Any): passed on to the requests package

        Returns:
            requests.models.Response: a Requests response object

        Raises:
             ApiError if anything but expected response code is returned
        """

        # Perform a POST request
        response = self._request("POST", uri, data=data, json=json, **kwargs)

        return response

    def put(self, uri, data=None, json=None, **kwargs):
        """
        A method to build a PUT request to interact with GameChanger.

        Args:
            uri (str): uri to send the HTTP POST request to
            data (Any) : data to be sent in the body of the request
            json (dict): data to be sent in JSON format in the body of the request
            kwargs (Any): passed on to the requests package

        Returns:
            requests.models.Response: a Requests response object

        Raises:
             ApiError if anything but expected response code is returned
        """

        # Perform a PUT request
        response = self._request("PUT", uri, data=data, json=json, **kwargs)

        return response

    def delete(self, uri, data=None, json=None, **kwargs):
        """A method to build a DELETE request to interact with GameChanger.

        Args:
            uri (str): uri to send the HTTP POST request to
            data (Any) : data to be sent in the body of the request
            json (dict): data to be sent in JSON format in the body of the request
            kwargs (Any): passed on to the requests package

        Returns:
            requests.models.Response: a Requests response object

        Raises:
             ApiError if anything but expected response code is returned
        """

        # Perform a DELETE request
        response = self._request("DELETE", uri, data=data, json=json, **kwargs)

        return response