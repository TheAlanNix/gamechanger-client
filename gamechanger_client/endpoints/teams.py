# -*- coding: utf-8 -*-
"""GameChanger 'Teams' API wrapper."""

import uuid

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class TeamsEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'teams')

    def associations(self, team_id):
        return super().get(f'{team_id}/associations')

    def avatar_image(self, team_id):
        return super().get(f'{team_id}/avatar-image')

    def create(self,
               name,
               sport,
               city,
               state,
               country,
               season_name,
               season_year,
               age_group,
               competition_level,
               team_type='admin',
               ngb=[]):
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
            'ngb': ngb
        }

        return super().post('/', team=team_data)

    def create_event(self,
                     team_id,
                     event_type,
                     status,
                     start_time,
                     end_time,
                     arrive_time,
                     location,
                     sub_type=[],
                     full_day=False,
                     time_zone='America/New_York',
                     should_notify=False,
                     message='',
                     opponent_id=None,
                     opponent_name=None,
                     title=None):
        event_data = {
            'id': str(uuid.uuid1()),
            'team_id': team_id,
            'event_type': event_type,
            'sub_type': sub_type,
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

    def create_player(self, team_id, first_name, last_name, number, batting_side=None, throwing_hand=None):
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

        return super().post(f'{team_id}/players/', player=player_data)

    def delete(self, team_id):
        return super().delete(f'{team_id}')

    def delete_event(self, team_id, event_id, should_notify=False, message=''):
        event_data = {'event': {'status': 'canceled'}}
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
