import unittest
from FootyStatsPy.euro2024 import scrape_euro2024_data
import pandas as pd

class TestEuro2024(unittest.TestCase):

    def test_scrape_euro2024_data(self):
        df = scrape_euro2024_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

if __name__ == '__main__':
    unittest.main()

