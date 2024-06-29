import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from .exceptions import PlayerDoesntHaveInfo, MatchDoesntHaveInfo
from .config import headers

class Fbref:
    def __init__(self):
        self.possible_stats = [
            'stats', 'keepers', 'keepersadv', 'shooting', 'passing',
            'passing_types', 'gca', 'defense', 'possession', 'playingtime', 'misc'
        ]

    def get_teams_season_stats(self, stat, league, season=None, save_csv=False, stats_vs=False, change_columns_names=False, add_page_name=False):
        print("Starting to scrape teams data from Fbref...")
        if stat not in self.possible_stats:
            raise ValueError(f"Invalid stat: {stat}. Possible values are: {self.possible_stats}")

        path = f'https://fbref.com/en/comps/Big5/{stat}/players/Big-5-European-Leagues-Stats'
        response = requests.get(path, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table')

        if table is None:
            raise ValueError(f"Could not find the table on the page {path}")

        df = pd.read_html(str(table))[0]
        df.columns = [' '.join(col).strip() for col in df.columns]
        df = df.reset_index(drop=True)

        new_columns = []
        for col in df.columns:
            if 'level_0' in col:
                new_col = col.split()[-1]  # takes the last name
            else:
                new_col = col
            new_columns.append(new_col)

        df.columns = new_columns
        df = df.fillna(0)

        if change_columns_names:
            df.columns = df.columns.map(lambda x: x.split('Unnamed: ')[1] if 'Unnamed: ' in x else x)
            if add_page_name:
                df.columns = [f'{stat}_{col}' for col in df.columns]

        if save_csv:
            today = datetime.now().strftime('%Y-%m-%d')
            df.to_csv(f'{league}_{season}_{stat}_{today}.csv', index=False)

        return df

    def get_player_season_stats(self, stat, league, season=None, save_csv=False, add_page_name=False):
        print("Starting to scrape player data from Fbref...")
        if stat not in self.possible_stats:
            raise ValueError(f"Invalid stat: {stat}. Possible values are: {self.possible_stats}")

        path = f'https://fbref.com/en/comps/Big5/{stat}/players/Big-5-European-Leagues-Stats'
        response = requests.get(path, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table')

        if table is None:
            raise ValueError(f"Could not find the table on the page {path}")

        df = pd.read_html(str(table))[0]
        df.columns = [' '.join(col).strip() for col in df.columns]
        df = df.reset_index(drop=True)

        new_columns = []
        for col in df.columns:
            if 'level_0' in col:
                new_col = col.split()[-1]  # takes the last name
            else:
                new_col = col
            new_columns.append(new_col)

        df.columns = new_columns
        df = df.fillna(0)

        if add_page_name:
            df.columns = [f'{stat}_{col}' for col in df.columns]

        if save_csv:
            today = datetime.now().strftime('%Y-%m-%d')
            df.to_csv(f'{league}_{season}_{stat}_players_{today}.csv', index=False)

        return df

    def get_all_teams_season_stats(self, league, season, save_csv=False, stats_vs=False, change_columns_names=False, add_page_name=False):
        print("Starting to scrape all teams data from Fbref...")
        data = pd.DataFrame()
        for stat in self.possible_stats:
            try:
                df = self.get_teams_season_stats(stat, league, season, False, stats_vs, change_columns_names, add_page_name)
                data = pd.concat([data, df], axis=1)
            except ValueError as e:
                print(e)

        if save_csv:
            today = datetime.now().strftime('%Y-%m-%d')
            data.to_csv(f'{league}_{season}_all_team_stats_{today}.csv', index=False)

        return data

    def get_match_shots(self, path):
        print("Starting to scrape match shots data from Fbref...")
        self.match_info_exception(path)
        data = self.get_all_dfs(path)[17]
        data.columns = data.columns.droplevel(0)
        return data

    def get_general_match_team_stats(self, path):
        print("Starting to scrape general match team stats from Fbref...")
        self.match_info_exception(path)
        data = self.get_all_dfs(path)
        local_df, visit_df = data[3], data[10]
        return local_df, visit_df

    def get_tournament_table(self, path):
        print("Starting to scrape tournament table data from Fbref...")
        data = self.get_all_dfs(path)[0]
        return data

    def get_all_dfs(self, path):
        response = requests.get(path, headers=headers)
        data = pd.read_html(response.content)
        return data

    def match_info_exception(self, path):
        data = self.get_all_dfs(path)
        try:
            data[17]
        except IndexError:
            raise MatchDoesntHaveInfo(path)
