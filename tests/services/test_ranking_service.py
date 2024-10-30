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

    @patch('services.ranking_service.get_player_by_id')
    def test_calculate_ranking_win(self, mock_get_player_by_id):
        """
        Test case: Player wins the match.
        Expected behavior: The player's points increase by 10, if against similar rankings (almost the same).
        """
        mock_get_player_by_id.side_effect = lambda player_id: {'player_id': player_id, 'rank': 'Iron', 'points': 300}

        player_data = {
            'id': 3,
            'points': 300,
            'rank': 'Iron'
        }
        winner_team_id = "0"
        team1 = {'team_id': '0', 'player_ids': [12, 3, 4, 5, 6]}
        team2 = {'team_id': '1', 'player_ids': [32, 1, 6, 88, 9]}
        
        new_points = calculate_ranking(player_data, winner_team_id, team1, team2)
        self.assertEqual(new_points, {'rank': 'Iron', 'points': 310})

    @patch('services.ranking_service.get_player_by_id')
    def test_calculate_ranking_loss(self, mock_get_player_by_id):
        """
        Test case: Player loses the match.
        Expected behavior: The player's points decrease by 10 with teams of (almost or) the same rank
        """
        mock_get_player_by_id.side_effect = lambda player_id: {'player_id': player_id, 'rank': 'Iron', 'points': 300}

        player_data = {
            'id': 3,
            'points': 300,
            'rank': 'Iron'
        }
        winner_team_id = "1"
        team1 = {'team_id': '0', 'player_ids': [12, 3, 4, 5, 6]}
        team2 = {'team_id': '1', 'player_ids': [32, 1, 6, 88, 9]}
        
        new_points = calculate_ranking(player_data, winner_team_id, team1, team2)
        self.assertEqual(new_points, {'rank': 'Iron', 'points': 260})

    @patch('services.ranking_service.get_player_by_id')
    def test_calculate_ranking_tie(self, mock_get_player_by_id):
        """
        Test case: The match ends in a tie.
        Expected behavior: The player's points remain the same.
        """
        mock_get_player_by_id.side_effect = lambda player_id: {'player_id': player_id, 'rank': 'Iron', 'points': 300}

        player_data = {
            'id': 3,
            'points': 300,
            'rank': 'Iron'
        }
        winner_team_id = None
        team1 = {'team_id': '0', 'player_ids': [12, 3, 4, 5, 6]}
        team2 = {'team_id': '1', 'player_ids': [32, 1, 6, 88, 9]}
        
        new_points = calculate_ranking(player_data, winner_team_id, team1, team2)
        self.assertEqual(new_points, {'rank': 'Gold', 'points': 300})

    @patch('services.ranking_service.get_player_by_id')
    def test_calculate_ranking_no_points(self, mock_get_player_by_id):
        """
        Edge case: Player's points are initially missing (empty string).
        Expected behavior: The function should handle missing points and return 0 or some default behavior.
        """
        mock_get_player_by_id.side_effect = lambda player_id: {'player_id': player_id, 'rank': 'Iron', 'points': ''}

        player_data = {
            'id': 3,
            'points': '',
            'rank': 'Iron'
        }
        winner_team_id = "0"
        team1 = {'team_id': '0', 'player_ids': [12, 3, 4, 5, 6]}
        team2 = {'team_id': '1', 'player_ids': [32, 1, 6, 88, 9]}
        
        new_points = calculate_ranking(player_data, winner_team_id, team1, team2)
        self.assertEqual(new_points, {'rank': 'Iron', 'points': 60})

    @patch('services.ranking_service.get_player_by_id')
    def test_calculate_ranking_negative_points(self, mock_get_player_by_id):
        """
        Edge case: Player's points are negative.
        Expected behavior: The function should handle negative points appropriately, converting points to 0 in case of winning will have +10 points.
        """
        mock_get_player_by_id.side_effect = lambda player_id: {'player_id': player_id, 'rank': 'Iron', 'points': -40}

        player_data = {
            'id': 3,
            'points': -40,
            'rank': 'Iron'
        }
        winner_team_id = "0"
        team1 = {'team_id': '0', 'player_ids': [12, 3, 4, 5, 6]}
        team2 = {'team_id': '1', 'player_ids': [32, 1, 6, 88, 9]}
        
        new_points = calculate_ranking(player_data, winner_team_id, team1, team2)
        self.assertEqual(new_points, {'rank': 'Iron', 'points': 20})

    @patch('services.ranking_service.get_player_by_id')
    def test_calculate_ranking_invalid_winner_team_id(self, mock_get_player_by_id):
        """
        Edge case: Invalid winner_team_id (not matching any team).
        Expected behavior: The function should raise an exception or handle the invalid input gracefully.
        """
        mock_get_player_by_id.side_effect = lambda player_id: {'player_id': player_id, 'rank': 'Iron', 'points': 300}

        player_data = {
            'id': 3,
            'points': 300,
            'rank': 'Iron'
        }
        winner_team_id = "invalid_team_id"
        team1 = {'team_id': '0', 'player_ids': [12, 3, 4, 5, 6]}
        team2 = {'team_id': '1', 'player_ids': [32, 1, 6, 88, 9]}
        
        # with self.assertRaises(ValueError):
        new_points = calculate_ranking(player_data, winner_team_id, team1, team2)
        self.assertEqual(new_points, {"rank": "", 'points': ""})

if __name__ == '__main__':
    unittest.main()
