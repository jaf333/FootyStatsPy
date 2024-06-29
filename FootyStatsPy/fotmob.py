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
        """Get standing tables for a certain season in a league.

        Args:
            league (str): Possible leagues in get_available_leagues("Fotmob")
            season (str): Possible season in get_available_season_for_leagues("Fotmob", league)
            table (str, optional): Type of table shown in FotMob UI. Defaults to 'all'.

        Returns:
            table_df: DataFrame with the table.
        """
        league_id = self.get_league_id(league)
        season_id = self.get_season_id(league, season)
        response = requests.get(f'https://www.fotmob.com/api/leagues?id={league_id}&ccode3=ARG&season={season_id}', headers=headers)
        time.sleep(3)
        tables = response.json()['table'][0]['data']['table']
        table_df = pd.DataFrame(tables[table])
        return table_df

    def get_players_stats_season(self, league, season, stat):
        """Get players for a certain season and league stats. Possible stats are player_possible_stats.

        Args:
            league (str): Possible leagues in get_available_leagues("Fotmob")
            season (str): Possible season in get_available_season_for_leagues("Fotmob", league)
            stat (str): Value inside player_possible_stats

        Raises:
            InvalidStat: Raised when the input of stat is not inside the possible list values.

        Returns:
            df: DataFrame with the values and player names for that stat.
        """
        if stat not in self.player_possible_stats:
            raise InvalidStat(stat, self.player_possible_stats)
        league_id = self.get_league_id(league)
        season_id = self.get_season_id(league, season)
        response = requests.get(f'https://www.fotmob.com/api/leagueseasondeepstats?id={league_id}&season={season_id}&type=players&stat={stat}', headers=headers)
        time.sleep(3)
        df_1 = pd.DataFrame(response.json()['statsData'])
        df_2 = pd.DataFrame(response.json()['statsData']).statValue.apply(pd.Series)
        df = pd.concat([df_1, df_2], axis=1)
        return df

    def get_teams_stats_season(self, league, season, stat):
        """Get teams for a certain season and league stats. Possible stats are team_possible_stats.

        Args:
            league (str): Possible leagues in get_available_leagues("Fotmob")
            season (str): Possible season in get_available_season_for_leagues("Fotmob", league)
            stat (str): Value inside team_possible_stats

        Raises:
            InvalidStat: Raised when the input of stat is not inside the possible list values.

        Returns:
            df: DataFrame with stat values for teams in a league and season.
        """
        if stat not in self.team_possible_stats:
            raise InvalidStat(stat, self.team_possible_stats)
        league_id = self.get_league_id(league)
        season_id = self.get_season_id(league, season)
        response = requests.get(f'https://www.fotmob.com/api/leagueseasondeepstats?id={league_id}&season={season_id}&type=teams&stat={stat}', headers=headers)
        time.sleep(3)
        df_1 = pd.DataFrame(response.json()['statsData'])
        df_2 = pd.DataFrame(response.json()['statsData']).statValue.apply(pd.Series)
        df = pd.concat([df_1, df_2], axis=1)
        return df

    def get_match_shotmap(self, match_id):
        """Scrape a match shotmap, if it has one.

        Args:
            match_id (str): Id of a FotMob match, could be found in the URL.

        Raises:
            MatchDoesntHaveInfo: Raised when the match associated with the match_id doesn't have a shotmap.

        Returns:
            shotmap: DataFrame with the data for all the shots shown in the FotMob UI.
        """
        response = self.request_match_details(match_id)
        time.sleep(1)
        df_shotmap = pd.DataFrame(response.json()['content']['shotmap']['shots'])
        if df_shotmap.empty:
            raise MatchDoesntHaveInfo(match_id)
        ongoalshot = df_shotmap.onGoalShot.apply(pd.Series).rename(columns={'x': 'goalMouthY', 'y': 'goalMouthZ'})
        shotmap = pd.concat([df_shotmap, ongoalshot], axis=1).drop(columns=['onGoalShot'])
        return shotmap

    def get_general_match_stats(self, match_id):
        """Get general match stats for a certain match.

        Args:
            match_id (str): Id of a FotMob match, could be found in the URL.

        Returns:
            total_df: DataFrame with the stats of the teams for a certain match
        """
        response = self.request_match_details(match_id)
        time.sleep(1)
        total_df = pd.DataFrame()
        stats_df = response.json()['content']['stats']['Periods']['All']['stats']
        for stat in stats_df:
            df = pd.DataFrame(stat['stats'])
            df = pd.concat([df, df.stats.apply(pd.Series).rename(columns={0: 'home', 1: 'away'})], axis=1).drop(columns=['stats']).dropna(subset=['home', 'away'])
            total_df = pd.concat([total_df, df])
        return total_df

    def get_league_id(self, league):
        # Mock implementation to return league id
        league_ids = {'Premier League': 47, 'La Liga': 87}
        return league_ids.get(league, 0)

    def get_season_id(self, league, season):
        # Mock implementation to return season id
        season_ids = {'2023/2024': '2023%2F2024', '2022/2023': '2022%2F2023'}
        return season_ids.get(season, '0')

    def request_match_details(self, match_id):
        response = requests.get(f'https://www.fotmob.com/api/matchDetails?matchId={match_id}', headers=headers)
        time.sleep(3)
        return response

