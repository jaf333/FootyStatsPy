import unittest
from MyFootballStats.fbref import Fbref

class TestFbref(unittest.TestCase):

    def setUp(self):
        self.fbref = Fbref()

    def test_get_teams_season_stats(self):
        result = self.fbref.get_teams_season_stats('stats', 'Premier League', '2023-2024')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_get_player_season_stats(self):
        result = self.fbref.get_player_season_stats('stats', 'Premier League', '2023-2024')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_get_all_teams_season_stats(self):
        result = self.fbref.get_all_teams_season_stats('Premier League', '2023-2024')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_get_match_shots(self):
        result = self.fbref.get_match_shots('https://fbref.com/en/matches/77d7e2d6/Arsenal-Luton-Town-April-3-2024-Premier-League')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_get_general_match_team_stats(self):
        local_df, visit_df = self.fbref.get_general_match_team_stats('https://fbref.com/en/matches/77d7e2d6/Arsenal-Luton-Town-April-3-2024-Premier-League')
        self.assertIsInstance(local_df, pd.DataFrame)
        self.assertIsInstance(visit_df, pd.DataFrame)
        self.assertFalse(local_df.empty)
        self.assertFalse(visit_df.empty)

    def test_get_tournament_table(self):
        result = self.fbref.get_tournament_table('https://fbref.com/en/comps/9/Premier-League-Stats')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

if __name__ == '__main__':
    unittest.main()

