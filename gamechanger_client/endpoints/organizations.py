# -*- coding: utf-8 -*-
"""GameChanger 'Organizations' API wrapper."""

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class OrganizationsEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'organizations')

    def standings(self, organization_id):
        return super().get(f'{organization_id}/standings')

    def teams(self, organization_id, page=0):
        return super().get(f'{organization_id}/teams?page_starts_at={page}')
