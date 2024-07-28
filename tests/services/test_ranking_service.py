import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from unittest import TestCase
from unittest.mock import patch
from services.ranking_service import calculate_ranking

#given when & then
# given player data...
# when this calculates (function to try)
# then expected result

class TestRankingService(TestCase):

    @patch('services.ranking_service.get_player_data')
    def test_calculate_ranking(self, mock_get_player_data):
        
        

        player_data = {
            'id': 3,
            'points': 2,
            'rank': 'Iron'
        }

        mock_get_player_data.side_effect = lambda player_id: {'player_id': player_id, 'rank':'Iron', 'points': 2}

        winner_team_id = "1"

        team1 = {
            'team_id': '0',
            'player_ids': [12,3,4,5,6]
        }

        team2 = {
            'team_id': '1',
            'player_ids': [32,1,6,88,9]
        }
        new_points = calculate_ranking(player_data, winner_team_id, team1, team2) # add team_data?
        print(new_points)
        # Check if the data is retrieved correctly
        self.assertEqual(new_points, {'rank': 'Bronze', 'points': 5})

if __name__ == '__main__':
    unittest.main()
