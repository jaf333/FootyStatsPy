import unittest
import pandas as pd
from FootyStatsPy.fotmob import FotMob

class TestFotMob(unittest.TestCase):

    def setUp(self):
        self.fotmob = FotMob()

    def test_get_season_tables(self):
        result = self.fotmob.get_season_tables('Premier League', '2023/2024')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_get_players_stats_season(self):
        result = self.fotmob.get_players_stats_season('Premier League', '2023/2024', 'goals')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_get_teams_stats_season(self):
        result = self.fotmob.get_teams_stats_season('Premier League', '2023/2024', 'rating_team')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_get_match_shotmap(self):
        result = self.fotmob.get_match_shotmap(4193851)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_get_general_match_stats(self):
        result = self.fotmob.get_general_match_stats(4193851)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

if __name__ == '__main__':
    unittest.main()

