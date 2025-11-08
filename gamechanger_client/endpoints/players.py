# -*- coding: utf-8 -*-
"""GameChanger 'Players' API wrapper."""

from typing import Any, Dict, List

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class PlayersEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'players')

    def delete(self, player_id):
        return super().delete(f'{player_id}')

    def family_relationships(self, player_id):
        return super().get(f'{player_id}/family-relationships')

    def update_family_relationships(self, 
                                    player_id: str,
                                    *,  # Force keyword-only arguments after this
                                    action: str = 'add',
                                    entities: List[str] = None,
                                    additional_fields: Dict[str, Any] = None,
                                    **kwargs) -> dict:
        """
        Update family relationships for a player.
        
        Args:
            player_id: Player ID
            action: Action to perform ('add' or 'remove', default: 'add')
            entities: List of email entities to add/remove (default: [])
            additional_fields: Dict of additional fields to include in the updates
            **kwargs: Additional fields passed as keyword arguments
            
        Returns:
            dict: API response with updated relationship data
        """
        email_list = []
        for entity in (entities or []):
            email_list.append({'email': entity})

        patch_data = {
            'updates': {
                f'{action}': email_list
            }
        }
        
        # Merge additional fields into the updates
        if additional_fields:
            patch_data['updates'].update(additional_fields)
            
        # Merge kwargs into the updates
        if kwargs:
            patch_data['updates'].update(kwargs)

        return super().patch(f'{player_id}/family-relationships', **patch_data)
