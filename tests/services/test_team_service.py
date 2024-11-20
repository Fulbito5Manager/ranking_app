import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from unittest.mock import patch, Mock
from services.team_service import get_teams_data_by_match_id

class TestGetTeamsData(unittest.TestCase):

    @patch('services.team_service.requests.get')
    def test_get_teams_data_by_id(self, mock_get):
        match_id = 1
        
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 1, 'players': ['Player 1', 'Player 2']},
            {'id': 2, 'players': ['Player 3', 'Player 4']}
        ]
        mock_get.return_value = mock_response

        team_a, team_b = get_teams_data_by_match_id(match_id)
        
        self.assertEqual(team_a, {'id': 1, 'players': ['Player 1', 'Player 2']})
        self.assertEqual(team_b, {'id': 2, 'players': ['Player 3', 'Player 4']})
        print("Successfully fetched teams data.")

    @patch('services.team_service.requests.get')
    def test_get_teams_data_by_id_falsy_value(self, mock_get):
        match_id = 1
        
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        team_a, team_b = get_teams_data_by_match_id(match_id)
        
        self.assertIsNone(team_a)
        self.assertIsNone(team_b)
