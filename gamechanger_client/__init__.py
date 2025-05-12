# -*- coding: utf-8 -*-
"""
Community-developed Python SDK for interacting with Gamechanger APIs.
"""

import logging
import os
import random
import string
import uuid

from gamechanger_client.http_session import HttpSession

from .endpoints.clips import ClipsEndpoint
from .endpoints.me import MeEndpoint
from .endpoints.organizations import OrganizationsEndpoint
from .endpoints.public import PublicEndpoint
from .endpoints.search import SearchEndpoint
from .endpoints.teams import TeamsEndpoint
from .version import __version__  # noqa: F401

logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s] %(message)s')
logger = logging.getLogger('gamechanger-client')
logger.setLevel(os.getenv('LOG_LEVEL', logging.INFO))


class GameChangerClient:

    def __init__(self,
                 username=None,
                 password=None,
                 token=None):


        self._gc_username = username or os.getenv('GC_USERNAME')
        self._gc_password = password or os.getenv('GC_PASSWORD')
        self._gc_token = token or os.getenv('GC_TOKEN')

        self._client_id = uuid.uuid1()
        # self._client_key = self._ge

        # Create a new requests session
        self._session = HttpSession(self._gc_token)

        self.clips = ClipsEndpoint(self._session)
        self.me = MeEndpoint(self._session)
        self.organizations = OrganizationsEndpoint(self._session)
        self.public = PublicEndpoint(self._session)
        self.search = SearchEndpoint(self._session)
        self.teams = TeamsEndpoint(self._session)


    def _generate_random_hex(self, length = 32):
        random_string = ''.join(random.SystemRandom().choice(string.hexdigits) for _ in range(length))

        return random_string

    def _generate_random_string(self, length = 32):
        random_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

        return random_string

    def _generate_random_base64(self, length = 32):
        random_string = self._generate_random_string(length)
        random_string_bytes = random_string.encode('ascii')

        random_base64_bytes = base64.b64encode(random_string_bytes)
        random_base64_string = random_base64_bytes.decode('ascii')

        return random_base64_string

    def auth(self):
        auth_url = f'{self._base_url}/auth'

        print(self._generate_random_hex().lower())
        exit()


        # Build the request headers
        auth_init_headers = self._session.headers
        auth_init_headers['Content-Type'] = 'application/json; charset=utf-8'
        auth_init_headers['Gc-App-Name'] = 'web'
        auth_init_headers['Gc-App-Version'] = '0.0.0'
        auth_init_headers['Gc-Client-Id'] = str(self._client_id)
        auth_init_headers['Gc-Timestamp'] = str(time.time())

        auth_init_payload = {
            'type': 'client-auth',
            'client_id': str(self._client_id)
        }

        response = self._session.options(auth_url)
        print(response.text)
        exit()
