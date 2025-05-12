# -*- coding: utf-8 -*-
"""GameChanger API wrapper."""

import logging

logger = logging.getLogger('gamechanger-client.rest-endpoint')


class RestEndpoint:
    """A class used to implement base functionality for GameChanger API Endpoints."""

    def __init__(self, session, endpoint_root):
        """
        Initialize the RestEndpoint class.

        Args:
            session (HttpSession): An instance of the HttpSession class.
            endpoint_root (str, optional): The URL endpoint root to use.
        """
        super().__init__()
        self._session = session
        self._endpoint_root = endpoint_root

    def _build_url(self, url=None):
        """Builds the URL to use based on the endpoint path, and ID.

        Args:
          id (str): A string representing the ID of an object to use in the URL

        Returns:
            str: a formatted URL

        """
        result = f"{self._session._base_url}/{self._endpoint_root}"

        if url:
            result += f"/{url}"

        return result

    def _build_dict_from_items(self, *dicts, **items):
        """A method to build a dictionary based on inputs, pruning items that are None.

        Args:
          dicts (dict): Some number of dictionaries the join together
          items (any): Some number of keyword items to add to the joined dicts

        Returns:
          dict: A single dict built from the input.

        """
        dict_list = list(dicts)
        dict_list.append(items)
        result = {}

        for dictionary in dict_list:
            result = {
                **result,
                **self._convert_dictionary(dictionary, list(result.keys())),
            }

        return result

    def _convert_dictionary(self, dictionary, existing_keys):
        """Iteratively process a dictionary to convert it to expected JSON.

        Args:
          dictionary (dict): a dictionary
          existing_keys (list): a list of keys to append to

        Returns:
          dict: A single dictionary of key/value pairs.

        Raises:
          KeyError: In case there is a duplicate key name in the dictionary.

        """
        result = {}

        for key, value in dictionary.items():
            if value is None:
                continue
            if key in existing_keys:
                raise KeyError(f"Attempted to insert duplicate key '{key}'")
            if isinstance(value, dict):
                value = self._convert_dictionary(value, [])

            existing_keys.append(key)
            result[key] = value

        return result

    def get(self, url=None, **request_params):
        """A method to perform a get request.

        Args:
          id (str): A string representing additional url.
          request_params (any): A dictionary of parameters to add to the request.

        Returns:
            dict: JSON containing the retrieved object(s)
        """
        params = self._build_dict_from_items(request_params)

        response = self._session.get(
            self._build_url(url), params=params
        )

        return response.json()

    def post(self, url=None, **request_params):
        """A method to perform a post request.

        Args:
          params (any):  Parameters
          request_params (any): Request parameters.

        Returns:
            dict: JSON containing the new object info

        """
        json = self._build_dict_from_items(request_params)

        response = self._session.post(
            self._build_url(url), json=json
        )

        return response.json()
