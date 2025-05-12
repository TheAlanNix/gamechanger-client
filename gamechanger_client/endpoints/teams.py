# -*- coding: utf-8 -*-
"""GameChanger 'Teams' API wrapper."""

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class TeamsEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'teams')

    def associations(self, team_id):
        return super().get(f'{team_id}/associations')

    def game_summaries(self, team_id):
        return super().get(f'{team_id}/game-summaries')

    def event_video_stream_assets(self, team_id, event_id):
        return super().get(f'{team_id}/schedule/events/{event_id}/video-stream/assets')

    def event_video_stream_playback_info(self, team_id, event_id):
        return super().get(f'{team_id}/schedule/events/{event_id}/video-stream/assets/playback')

    def players(self, team_id):
        return super().get(f'{team_id}/players')

    def public_players(self, team_public_id):
        return super().get(f'public/{team_public_id}/players')

    def schedule(self, team_id):
        return super().get(f'{team_id}/schedule')

    def season_stats(self, team_id):
        return super().get(f'{team_id}/season-stats')

    def video_stream_assets(self, team_id):
        return super().get(f'{team_id}/video-stream/assets')

    def video_stream_videos(self, team_id):
        return super().get(f'{team_id}/video-stream/videos')
