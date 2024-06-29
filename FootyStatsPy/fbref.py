import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from datetime import datetime
import time
from .exceptions import PlayerDoesntHaveInfo, MatchDoesntHaveInfo
from .config import headers

class Fbref:
    def __init__(self):
        self.possible_stats = [
            'stats', 'keepers', 'keepersadv', 'shooting', 'passing',
            'passing_types', 'gca', 'defense', 'possession', 'playingtime', 'misc'
        ]

    def get_teams_season_stats(self, stat, league, season=None, save_csv=False, stats_vs=False, change_columns_names=False, add_page_name=False):
        """Gets you a table of the stats for the teams in a certain league.

        Args:
            stat (str): Stat available for that league in Fbref
            league (str): Possible leagues in get_available_leagues("Fbref")
            season (str, optional): String showing the season for the data to be extracted. Defaults to None.
            save_csv (bool, optional): If true it save an excel file. Defaults to False.
            stats_vs (bool, optional): If true it gives you the VS stats of that table. Defaults to False.
            change_columns_names (bool, optional): If you would like to change the columns names. Defaults to False.
            add_page_name (bool, optional): It add the stat name to the columns. Defaults to False.

        Returns:
            data: DataFrame with the data of the stats of the teams.
        """
        print("Starting to scrape teams data from Fbref...")
        # Validate the stat parameter
        if stat not in self.possible_stats:
            raise ValueError(f"Invalid stat: {stat}. Possible values are: {self.possible_stats}")

        # Define the URL path based on parameters
        path = f'https://fbref.com/en/comps/{league}/{season}/{stat}/{league}-{season}-Stats' if season else f'https://fbref.com/en/comps/{league}/{stat}/{league}-Stats'

        # Make the request and parse the response
        response = requests.get(path, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table', {'id': 'results'})

        # Convert the table to a DataFrame
        df = pd.read_html(str(table))[0]

        # Handle the optional parameters
        if change_columns_names:
            df.columns = df.columns.map(lambda x: x.split('Unnamed: ')[1] if 'Unnamed: ' in x else x)
            if add_page_name:
                df.columns = [f'{stat}_{col}' for col in df.columns]
        else:
            df.columns = df.columns.droplevel(0)

        # Save to CSV if requested
        if save_csv:
            today = datetime.now().strftime('%Y-%m-%d')
            df.to_csv(f'{league}_{season}_{stat}_{today}.csv', index=False)

        return df

    def get_player_season_stats(self, stat, league, season=None, save_csv=False, add_page_name=False):
        """Get players season stats for a particular stat.

        Args:
            stat (str): Stat available for that league in Fbref
            league (str): Possible leagues in get_available_leagues("Fbref")
            season (str, optional): String showing the season for the data to be extracted. Defaults to None.
            save_csv (bool, optional): If true it save an excel file. Defaults to False.
            add_page_name (bool, optional): It add the stat name to the columns. Defaults to False.

        Returns:
            data: DataFrame with the data of the stats of the players.
        """
        print("Starting to scrape player data from Fbref...")
        # Validate the stat parameter
        if stat not in self.possible_stats:
            raise ValueError(f"Invalid stat: {stat}. Possible values are: {self.possible_stats}")

        # Define the URL path based on parameters
        path = f'https://fbref.com/en/comps/{league}/{season}/{stat}/players/{league}-{season}-Stats' if season else f'https://fbref.com/en/comps/{league}/{stat}/players/{league}-Stats'

        # Make the request and parse the response
        response = requests.get(path, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table', {'id': 'results'})

        # Convert the table to a DataFrame
        df = pd.read_html(str(table))[0]

        # Handle the optional parameters
        if add_page_name:
            df.columns = [f'{stat}_{col}' for col in df.columns]

        # Save to CSV if requested
        if save_csv:
            today = datetime.now().strftime('%Y-%m-%d')
            df.to_csv(f'{league}_{season}_{stat}_players_{today}.csv', index=False)

        return df

    def get_all_teams_season_stats(self, league, season, save_csv=False, stats_vs=False, change_columns_names=False, add_page_name=False):
        """Gets a table of ALL the stats for the teams in a certain league and season.

        Args:
            league (str): Possible leagues in get_available_leagues("Fbref")
            season (str): Possible seasons in get_available_season_for_leagues("Fbref", league)
            save_csv (bool, optional): If true it save an excel file. Defaults to False.
            stats_vs (bool, optional): If true it gives you the VS stats of that table. Defaults to False.
            change_columns_names (bool, optional): If you would like to change the columns names. Defaults to False.
            add_page_name (bool, optional): It add the stat name to the columns. Defaults to False.

        Returns:
            data: DataFrame with all the stats of the teams.
        """
        print("Starting to scrape all teams data from Fbref...")
        data = pd.DataFrame()
        for stat in self.possible_stats:
            df = self.get_teams_season_stats(stat, league, season, False, stats_vs, change_columns_names, add_page_name)
            data = pd.concat([data, df], axis=1)

        if save_csv:
            today = datetime.now().strftime('%Y-%m-%d')
            data.to_csv(f'{league}_{season}_all_team_stats_{today}.csv', index=False)

        return data

    def get_all_teams_season_stats(self, league, season, save_csv=False, stats_vs=False, change_columns_names=False, add_page_name=False):
        """Gets a table of ALL the stats for the teams in a certain league and season.

        Args:
            league (str): Possible leagues in get_available_leagues("Fbref")
            season (str): Possible seasons in get_available_season_for_leagues("Fbref", league)
            save_csv (bool, optional): If true it save an excel file. Defaults to False.
            stats_vs (bool, optional): If true it gives you the VS stats of that table. Defaults to False.
            change_columns_names (bool, optional): If you would like to change the columns names. Defaults to False.
            add_page_name (bool, optional): It add the stat name to the columns. Defaults to False.

        Returns:
            data: DataFrame with all the stats of the teams.
        """
        print("Starting to scrape all teams data from Fbref...")
        data = pd.DataFrame()
        for stat in self.possible_stats:
            df = self.get_teams_season_stats(stat, league, season, False, stats_vs, change_columns_names, add_page_name)
            data = pd.concat([data, df], axis=1)

        if save_csv:
            today = datetime.now().strftime('%Y-%m-%d')
            data.to_csv(f'{league}_{season}_all_team_stats_{today}.csv', index=False)

        return data

    def get_match_shots(self, path):

        """Get match shots data.

        Args:
            path (str): URL to the match page in Fbref.

        Returns:
            data: DataFrame with match shots data.
        """
        self.match_info_exception(path)
        data = self.get_all_dfs(path)[17]
        data.columns = data.columns.droplevel(0)
        return data

    def get_general_match_team_stats(self, path):

        """Get general match team stats.

        Args:
            path (str): URL to the match page in Fbref.

        Returns:
            local_df: DataFrame with local team stats.
            visit_df: DataFrame with visiting team stats.
        """
        self.match_info_exception(path)
        data = self.get_all_dfs(path)
        local_df, visit_df = data[3], data[10]
        return local_df, visit_df

    def get_tournament_table(self, path):

        """Gets the table of the league.

        Args:
            path (str): URL of the page of the league.

        Returns:
            data: DataFrame with the league table.
        """
        data = self.get_all_dfs(path)[0]
        return data





