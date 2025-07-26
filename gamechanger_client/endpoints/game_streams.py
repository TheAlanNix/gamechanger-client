# -*- coding: utf-8 -*-
"""GameChanger 'Game Streams' API wrapper."""

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class GameStreamsEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'game-streams')

    def events(self, game_id):
        return super().get(f'{game_id}/events')
