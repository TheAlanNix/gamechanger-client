# -*- coding: utf-8 -*-
"""GameChanger 'Search' API wrapper."""

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class SearchEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'search')

    def search(self, name, types=[], seasons=[], sport=None, city=None, states=[], page=0):
        return super().post(name=name, types=types, seasons=seasons, sport=sport, city=city, states=states)
