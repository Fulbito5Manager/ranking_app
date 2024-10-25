
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
# from unittest import TestCase
from services.ranking_service import calculate_player_ranking
from unittest.mock import patch, MagicMock
from models.player_model import Player
from utils.db import db
from app import create_app

class TestPlayerService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')  # Use the test config
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Create all tables for the test
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()  # Drop all tables after test
        cls.app_context.pop()

    def setUp(self):
        self.connection = db.engine.connect()  # Start a connection
        self.transaction = self.connection.begin()  # Begin a transaction
        db.session.bind = self.connection  # Bind the session to the connection

        # Insert mock players into the test database
        self.players = [
            Player(id=1, points=50, rank="Iron"),
            Player(id=2, points=60, rank="Bronze"),
            Player(id=3, points=70, rank="Bronze"),
            Player(id=4, points=50, rank="Bronze"),
            Player(id=8, points=110, rank="Silver")
        ]
        db.session.bulk_save_objects(self.players)
        db.session.commit()

    def tearDown(self):
        self.transaction.rollback()  # Rollback the transaction after the test
        self.connection.close()  # Close the connection

    @patch('services.match_service.get_winner_team_id_by_match_id')
    @patch('services.team_service.get_teams_data_by_match_id')
    @patch('services.player_service.is_player_indb')
    @patch('services.rank_utils.get_rank_by_players_id')
    @patch('services.rank_utils.determine_rank')
    @patch('services.player_service.add_player_to_db')
    @patch('services.player_service.create_new_player')
    def test_handle_calculate_ranking(self, mock_create_new_player, mock_add_player_to_db, mock_determine_rank, mock_get_rank_by_players_id, mock_is_player_indb, mock_get_teams_data_by_match_id, mock_get_winner_team_id_by_match_id):
        
        # Mock external service data
        mock_get_winner_team_id_by_match_id.return_value = 1 
        
        mock_get_teams_data_by_match_id.return_value = (
            {'id': 1, 'jugadores': [1, 2, 3, 4, 5]},  # Team A players
            {'id': 24, 'jugadores': [6, 7, 8, 9, 10]}  # Team B players
        )

        print(f"Mock get_teams_data_by_match_id return: {mock_get_teams_data_by_match_id.return_value}")

        # Mocking is_player_indb to return None for new players
        mock_is_player_indb.side_effect = lambda id: next((p for p in self.players if p.id == id), None)

        # Mock the player creation
        mock_create_new_player.side_effect = lambda id: Player(id=id, points=50, rank="Bronze")

        # Mock the add_player_to_db to just simulate adding without actual DB operation
        mock_add_player_to_db.side_effect = lambda player: None  # Simulate a no-op

        mock_get_rank_by_players_id.side_effect = [
            [50, 60, 70, 80, 90],  # Team A player rankings
            [55, 65, 75, 85, 95]   # Team B player rankings
        ]
        mock_determine_rank.return_value = 'Gold'  # Mock rank determination

        match_id = 1

        result = calculate_player_ranking(match_id)  # This is the function you're testing

        print("This is the result:", result)
        self.assertIsNotNone(result)
        self.assertEqual(result['rank'], 'Gold')
        self.assertEqual(result['points'], 20)  # Adjust based on expected points logic

        print("Test completed successfully.")

    if __name__ == '__main__':
        unittest.main()

