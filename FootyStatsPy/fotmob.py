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
    
    def get_players_stats_season(self, league, season, stat):
        # Implementation goes here
        pass
    
    def get_teams_stats_season(self, league, season, stat):
        # Implementation goes here
        pass

