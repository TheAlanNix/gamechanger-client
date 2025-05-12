#!/bin/python/env
# -*- coding: utf-8 -*-

import json

from gamechanger_client import GameChangerClient


def main():
    gamechanger = GameChangerClient()

    team = gamechanger.me.teams()[0]
    print(json.dumps(team, indent=2))

    schedule = gamechanger.teams.schedule(team['id'])
    print(json.dumps(schedule, indent=2))

    user = gamechanger.me.user()
    print(json.dumps(user, indent=2))

    organizations = gamechanger.me.organizations()
    print(json.dumps(organizations, indent=2))

    search_results = gamechanger.search.search(
        name='Smyrna Little League AA',
        types=['org_league'],
        seasons=[{"name": "spring", "year": 2025}],
        sport='baseball',
        states=['GA']
    )
    print(json.dumps(search_results, indent=2))

    organization_teams = gamechanger.organizations.teams(search_results['hits'][0]['result']['id'])

    important_stats = ['AVG', 'SLG', 'OPS', 'H', '2B', '3B', 'HR', 'SO']
    player_stats = []

    for organization_team in organization_teams:
        players = gamechanger.teams.public_players(organization_team['team_public_id'])
        season_stats = gamechanger.teams.season_stats(organization_team['root_team_id'])

        for player in players:
            stat_line = f'{player['first_name']} {player['last_name']} (#{player['number']})'

            offensive_stats = season_stats['stats_data']['players'].get(player['id'], {}).get('stats', {}).get('offense', {})

            if offensive_stats:
                for stat in important_stats:
                    stat_line += f',{round(offensive_stats[stat], 3)}'

                player_stats.append(stat_line)

    with open('league_stats.csv', 'a') as league_stats:
        league_stats.write(f'Name,{','.join(important_stats)}\n')
        for stat_line in player_stats:
            league_stats.write(f'{stat_line}\n')


if __name__ == '__main__':
    main()