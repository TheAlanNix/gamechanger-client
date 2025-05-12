# -*- coding: utf-8 -*-
"""GameChanger 'Me' API wrapper."""

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class MeEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'me')

    def organizations(self):
        return super().get('organizations')

    def teams(self):
        return super().get('teams')

    def teams_summary(self):
        return super().get('teams-summary')

    def user(self):
        return super().get('user')
