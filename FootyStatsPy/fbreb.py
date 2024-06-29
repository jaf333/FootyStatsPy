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
        # Implementation goes here
        pass
    
    def get_player_season_stats(self, stat, league, season=None, save_csv=False, add_page_name=False):
        # Implementation goes here
        pass

