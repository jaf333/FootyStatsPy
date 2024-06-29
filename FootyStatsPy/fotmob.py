import requests
import pandas as pd
import time
from .exceptions import InvalidStat, MatchDoesntHaveInfo
from .config import headers

class FotMob:
    def __init__(self):
        self.player_possible_stats = [
            'goals', 'goal_assist', 'goals_per_90', 'expected_goals', 'expected_assists'
        ]
        self.team_possible_stats = [
            'rating_team', 'goals_team_match', 'possession_percentage_team', 'clean_sheet_team'
        ]

    def get_season_tables(self, league, season, table='all'):
        league_id = self.get_league_id(league)
        season_id = self.get_season_id(league, season)
        response = requests.get(f'https://www.fotmob.com/api/leagues?id={league_id}&ccode3=ARG&season={season_id}', headers=headers)
        time.sleep(3)
        tables = response.json().get('table', [{}])[0].get('data', {}).get('table', {})
        table_df = pd.DataFrame(tables.get(table, []))
        return table_df

    def get_players_stats_season(self, league, season, stat):
        if stat not in self.player_possible_stats:
            raise InvalidStat(stat, self.player_possible_stats)
        league_id = self.get_league_id(league)
        season_id = self.get_season_id(league, season)
        response = requests.get(f'https://www.fotmob.com/api/leagueseasondeepstats?id={league_id}&season={season_id}&type=players&stat={stat}', headers=headers)
        time.sleep(3)
        stats_data = response.json().get('statsData', [])
        if not stats_data:
            raise MatchDoesntHaveInfo(f"No stats data found for {stat} in {league} {season}")
        df = pd.DataFrame(stats_data)
        return df

    def get_teams_stats_season(self, league, season, stat):
        if stat not in self.team_possible_stats:
            raise InvalidStat(stat, self.team_possible_stats)
        league_id = self.get_league_id(league)
        season_id = self.get_season_id(league, season)
        response = requests.get(f'https://www.fotmob.com/api/leagueseasondeepstats?id={league_id}&season={season_id}&type=teams&stat={stat}', headers=headers)
        time.sleep(3)
        stats_data = response.json().get('statsData', [])
        if not stats_data:
            raise MatchDoesntHaveInfo(f"No stats data found for {stat} in {league} {season}")
        df = pd.DataFrame(stats_data)
        return df

    def get_match_shotmap(self, match_id):
        response = self.request_match_details(match_id)
        time.sleep(1)
        shotmap_data = response.json().get('content', {}).get('shotmap', {}).get('shots', [])
        if not shotmap_data:
            raise MatchDoesntHaveInfo(match_id)
        df_shotmap = pd.DataFrame(shotmap_data)
        ongoalshot = df_shotmap.onGoalShot.apply(pd.Series).rename(columns={'x': 'goalMouthY', 'y': 'goalMouthZ'})
        shotmap = pd.concat([df_shotmap, ongoalshot], axis=1).drop(columns=['onGoalShot'])
        return shotmap

    def get_general_match_stats(self, match_id):
        response = self.request_match_details(match_id)
        time.sleep(1)
        total_df = pd.DataFrame()
        stats_df = response.json().get('content', {}).get('stats', {}).get('Periods', {}).get('All', {}).get('stats', [])
        for stat in stats_df:
            df = pd.DataFrame(stat['stats'])
            df = pd.concat([df, df.stats.apply(pd.Series).rename(columns={0: 'home', 1: 'away'})], axis=1).drop(columns=['stats']).dropna(subset=['home', 'away'])
            total_df = pd.concat([total_df, df])
        return total_df

    def get_league_id(self, league):
        league_ids = {'Premier League': 47, 'La Liga': 87}
        return league_ids.get(league, 0)

    def get_season_id(self, league, season):
        season_ids = {'2023/2024': '2023%2F2024', '2022/2023': '2022%2F2023'}
        return season_ids.get(season, '0')

    def request_match_details(self, match_id):
        response = requests.get(f'https://www.fotmob.com/api/matchDetails?matchId={match_id}', headers=headers)
        time.sleep(3)
        return response
