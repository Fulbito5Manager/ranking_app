import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# print("Current PYTHONPATH:", sys.path)
import unittest
from services.player_service import create_new_player
from models.player_model import Player
from unittest.mock import patch

class TestCreateNewPlayer(unittest.TestCase):

    # @patch('services.player_service.create_new_player')
    @patch('models.player_model.Player')
    def test_create_player_limit_id(self, MockPlayer):

        mock_player_instance = MockPlayer.return_value
        mock_player_instance.id = 1
        mock_player_instance.points = 50
        mock_player_instance.rank = "Bronze"

        player_id = 1
        new_player = create_new_player(player_id)

        self.assertIsInstance(new_player, Player, "The returned object should be a Player instance.")
        self.assertEqual(new_player.id, player_id, "Player ID should match the provided ID.")
        self.assertEqual(new_player.points, 60, "Player should have 50 starting points.")
        self.assertEqual(new_player.rank, "Bronze", "Player rank should be 'Bronze' at the start.")

if __name__ == '__main__':
    unittest.main()