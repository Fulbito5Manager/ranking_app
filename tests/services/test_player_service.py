import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# print("Current PYTHONPATH:", sys.path)
import unittest
from services.player_service import create_new_player, add_player_to_db
from unittest.mock import patch, MagicMock

class TestCreateNewPlayer(unittest.TestCase):

    @patch('services.player_service.Player')
    def test_create_player_limit_reached(self, MockPlayer):
        player_id = 51

        new_player = create_new_player(player_id)

        self.assertIsNone(new_player, "Exceptected None when limit is exceded.")
        
    @patch('services.player_service.Player')
    def test_create_player_within_limit(self, MockPlayer):
        MockPlayer.return_value = MagicMock(id=50, points=50, rank="Bronze")
        player_id = 50

        new_player = create_new_player(player_id)

        self.assertIsNotNone(new_player)
        self.assertEqual(new_player.id, 50)
        self.assertEqual(new_player.points, 50)
        self.assertEqual(new_player.rank, "Bronze")

        print(f"On Within limit, Player created successfully: ID={new_player.id}, Points={new_player.points}, Rank={new_player.rank}")

    @patch('services.player_service.Player')
    def test_create_player_exception_handling(self, MockPlayer):

        MockPlayer.side_effect = Exception("Player Creation Error")
        player_id = 50

        new_player = create_new_player(player_id)
        
        self.assertIsNone(new_player)

class TestCreateAddPlayerToDB(unittest.TestCase):

    @patch('services.player_service.db.session')
    @patch('services.player_service.Player')
    def test_add_player_to_db_fail_commit(self, MockPlayer, MockSession):
        mock_player_instance = MockPlayer.return_value

        MockSession.add = MagicMock()
        MockSession.commit.side_effect = Exception("Database error")
        MockSession.rollback = MagicMock()

        add_player_to_db(mock_player_instance)

        MockSession.add.assert_called_once_with(mock_player_instance)
        MockSession.commit.assert_called_once()

    @patch('services.player_service.db.session')
    @patch('services.player_service.Player')
    def test_add_player_to_db_commited(self, MockPlayer, MockSession):
        mock_player_instance = MockPlayer.return_value

        MockSession.add = MagicMock()
        MockSession.commit.side_effect = MagicMock()
        MockSession.rollback = MagicMock()

        add_player_to_db(mock_player_instance)

        MockSession.add.assert_called_once_with(mock_player_instance)
        MockSession.commit.assert_called_once()
        print("Player commited.")