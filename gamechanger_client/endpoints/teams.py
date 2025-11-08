# -*- coding: utf-8 -*-
"""GameChanger 'Teams' API wrapper."""

import uuid
from typing import Any, Dict

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class TeamsEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'teams')

    def associations(self, team_id):
        return super().get(f'{team_id}/associations')

    def avatar_image(self, team_id):
        return super().get(f'{team_id}/avatar-image')

    def create(self,
               name: str,
               sport: str,
               city: str,
               state: str,
               country: str,
               season_name: str,
               season_year: int,
               age_group: str,
               competition_level: str,
               *,  # Force keyword-only arguments after this
               team_type: str = 'admin',
               ngb: list = None,
               additional_fields: Dict[str, Any] = None,
               **kwargs) -> dict:
        """
        Create a new team.
        
        Args:
            name: Team name
            sport: Sport type
            city: Team city
            state: Team state
            country: Team country  
            season_name: Season name
            season_year: Season year
            age_group: Age group
            competition_level: Competition level
            team_type: Type of team (default: 'admin')
            ngb: National governing body list (default: [])
            additional_fields: Dict of additional fields to include
            **kwargs: Additional fields passed as keyword arguments
            
        Returns:
            dict: API response with created team data
        """
        team_data = {
            'id': str(uuid.uuid1()),
            'name': name,
            'sport': sport,
            'city': city,
            'state': state,
            'country': country,
            'season_name': season_name,
            'season_year': season_year,
            'age_group': age_group,
            'competition_level': competition_level,
            'team_type': team_type,
            'ngb': ngb or []
        }
        
        # Merge additional fields
        if additional_fields:
            team_data.update(additional_fields)
            
        # Merge kwargs
        team_data.update(kwargs)

        return super().post(None, team=team_data)

    def create_event(self,
                     team_id: str,
                     event_type: str,
                     status: str,
                     start_time: str,
                     end_time: str,
                     arrive_time: str,
                     location: str,
                     *,  # Force keyword-only arguments after this
                     sub_type: list = None,
                     full_day: bool = False,
                     time_zone: str = 'America/New_York',
                     should_notify: bool = False,
                     message: str = '',
                     opponent_id: str = None,
                     opponent_name: str = None,
                     title: str = None,
                     additional_fields: Dict[str, Any] = None,
                     **kwargs) -> dict:
        """
        Create a new event for a team.
        
        Args:
            team_id: Team ID
            event_type: Type of event
            status: Event status
            start_time: Event start time
            end_time: Event end time
            arrive_time: Event arrival time
            location: Event location
            sub_type: Event sub-type list (default: [])
            full_day: Whether event is full day (default: False)
            time_zone: Event timezone (default: 'America/New_York')
            should_notify: Whether to send notifications (default: False)
            message: Notification message (default: '')
            opponent_id: Opponent team ID (optional)
            opponent_name: Opponent team name (optional)
            title: Event title (optional)
            additional_fields: Dict of additional fields to include
            **kwargs: Additional fields passed as keyword arguments
            
        Returns:
            dict: API response with created event data
        """
        event_data = {
            'id': str(uuid.uuid1()),
            'team_id': team_id,
            'event_type': event_type,
            'sub_type': sub_type or [],
            'status': status,
            'full_day': full_day,
            'timezone': time_zone,
            'start': {
                'datetime': start_time
            },
            'end': {
                'datetime': end_time
            },
            'arrive': {
                'datetime': arrive_time
            },
            'location': {
                'name': location
            }
        }

        if title:
            event_data['title'] = title
            
        # Merge additional fields
        if additional_fields:
            event_data.update(additional_fields)
            
        # Merge kwargs
        event_data.update(kwargs)

        pregame_data = None
        if opponent_id and opponent_name:
            pregame_data = {
                'opponent_id': opponent_id,
                'opponent_name': opponent_name
            }

        notification_data = {
            'should_notify': should_notify,
            'message': message
        }

        if pregame_data:
            return super().post(f'{team_id}/schedule/events/', event=event_data, notification=notification_data, pregame_data=pregame_data)
        else:
            return super().post(f'{team_id}/schedule/events/', event=event_data, notification=notification_data)

    def create_player(self, 
                      team_id: str, 
                      first_name: str, 
                      last_name: str, 
                      number: int,
                      *,  # Force keyword-only arguments after this
                      batting_side: str = None,
                      throwing_hand: str = None,
                      additional_fields: Dict[str, Any] = None,
                      **kwargs) -> dict:
        """
        Create a new player for a team.
        
        Args:
            team_id: Team ID
            first_name: Player's first name
            last_name: Player's last name
            number: Player's number
            batting_side: Player's batting side (optional)
            throwing_hand: Player's throwing hand (optional)
            additional_fields: Dict of additional fields to include
            **kwargs: Additional fields passed as keyword arguments
            
        Returns:
            dict: API response with created player data
        """
        player_data = {
            'id': str(uuid.uuid1()),
            'team_id': team_id,
            'first_name': first_name,
            'last_name': last_name,
            'number': number
        }

        if batting_side or throwing_hand:
            player_data['bats'] = {
                'batting_side': batting_side,
                'throwing_hand': throwing_hand
            }
            
        # Merge additional fields
        if additional_fields:
            player_data.update(additional_fields)
            
        # Merge kwargs
        player_data.update(kwargs)

        return super().post(f'{team_id}/players/', player=player_data)

    def delete(self, 
               team_id: str,
               *,  # Force keyword-only arguments after this
               additional_params: Dict[str, Any] = None,
               **kwargs) -> str:
        """
        Delete a team.
        
        Args:
            team_id: Team ID to delete
            additional_params: Dict of additional parameters to include in the request
            **kwargs: Additional parameters passed as keyword arguments
            
        Returns:
            str: API response text
        """
        # Build request parameters
        request_params = {}
        if additional_params:
            request_params.update(additional_params)
        if kwargs:
            request_params.update(kwargs)
            
        if request_params:
            return super().delete(f'{team_id}', **request_params)
        else:
            return super().delete(f'{team_id}')

    def delete_event(self, 
                     team_id: str, 
                     event_id: str,
                     *,  # Force keyword-only arguments after this
                     should_notify: bool = False,
                     message: str = '',
                     additional_fields: Dict[str, Any] = None,
                     **kwargs) -> dict:
        """
        Delete (cancel) an event for a team.
        
        Args:
            team_id: Team ID
            event_id: Event ID to delete
            should_notify: Whether to send notifications (default: False)
            message: Notification message (default: '')
            additional_fields: Dict of additional fields to include in the event update
            **kwargs: Additional fields passed as keyword arguments for the event update
            
        Returns:
            dict: API response with updated event data
        """
        event_data = {'event': {'status': 'canceled'}}
        
        # Merge additional event fields if provided
        if additional_fields:
            event_data['event'].update(additional_fields)
            
        # Merge kwargs into event data
        if kwargs:
            event_data['event'].update(kwargs)
            
        notification_data = {'should_notify': should_notify, 'message': message}

        return super().patch(f'{team_id}/schedule/events/{event_id}', updates=event_data, notification=notification_data)

    def game_summaries(self, team_id):
        return super().get(f'{team_id}/game-summaries')

    def event_player_stats(self, team_id, event_id):
        return super().get(f'{team_id}/schedule/events/{event_id}/player-stats')

    def event_video_stream_assets(self, team_id, event_id):
        return super().get(f'{team_id}/schedule/events/{event_id}/video-stream/assets')

    def event_video_stream_playback_info(self, team_id, event_id):
        return super().get(f'{team_id}/schedule/events/{event_id}/video-stream/assets/playback')

    def opponents(self, team_id):
        return super().get(f'{team_id}/opponents')

    def players(self, team_id):
        return super().get(f'{team_id}/players')

    def public_players(self, team_public_id):
        return super().get(f'public/{team_public_id}/players')

    def public_team_profile_id(self, team_id):
        return super().get(f'{team_id}/public-team-profile-id')

    def relationships(self, team_id):
        return super().get(f'{team_id}/relationships')

    def schedule(self, team_id):
        return super().get(f'{team_id}/schedule')

    def season_stats(self, team_id):
        return super().get(f'{team_id}/season-stats')
    
    def users(self, team_id):
        return super().get(f'{team_id}/users')

    def video_stream_assets(self, team_id):
        return super().get(f'{team_id}/video-stream/assets')

    def video_stream_videos(self, team_id):
        return super().get(f'{team_id}/video-stream/videos')
