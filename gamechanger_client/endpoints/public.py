# -*- coding: utf-8 -*-
"""GameChanger 'Public' API wrapper."""

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class PublicEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'public')

    def organization_standings(self, organization_id):
        return super().get(f'organization/{organization_id}/standings')

    def organization_teams(self, organization_id):
        return super().get(f'organization/{organization_id}/teams')

    def teams(self, team_public_id):
        return super().get(f'teams/{team_public_id}')

    def teams_games_preview(self, team_public_id):
        return super().get(f'teams/{team_public_id}/games/preview')

    def teams_live(self, team_public_id):
        return super().get(f'teams/{team_public_id}/live')
