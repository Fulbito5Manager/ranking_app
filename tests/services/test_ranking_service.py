import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from services.ranking_service import calculate_ranking

#given when & then
# given player data...
# when this calculates (function to try)
# then expected result

class TestRankingService(unittest.TestCase):

    def test_calculate_ranking(self):
        player_data = {
            'id': 3
        }
        winner_team_id = "0"

        team1 = {
            'team_id': '1',
            'player_ids': [12,3,4,5,6]
        }

        team2 = {
            'team_id': '1',
            'player_ids': [32,1,6,88,9]
        }
        new_points = calculate_ranking(player_data, winner_team_id, team1, team2) # add team_data?

        # Check if the data is retrieved correctly
        self.assertEqual(new_points, 115)

if __name__ == '__main__':
    unittest.main()
