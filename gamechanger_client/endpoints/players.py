# -*- coding: utf-8 -*-
"""GameChanger 'Players' API wrapper."""

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class PlayersEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'players')

    def delete(self, player_id):
        return super().delete(f'{player_id}')

    def family_relationships(self, player_id):
        return super().get(f'{player_id}/family-relationships')

    def update_family_relationships(self, player_id, action='add', entities=[]):
        email_list = []
        for entity in entities:
            email_list.append({'email': entity})

        patch_data = {
            'updates': {
                f'{action}': email_list
            }
        }

        return super().patch(f'{player_id}/family-relationships')
