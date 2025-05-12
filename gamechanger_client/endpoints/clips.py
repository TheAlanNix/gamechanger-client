# -*- coding: utf-8 -*-
"""GameChanger 'Clips' API wrapper."""

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class ClipsEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'me')

    def clips(self, team_id, kind='event'):
        return super().get(f'clips?kind={kind}&teamId={team_id}')
