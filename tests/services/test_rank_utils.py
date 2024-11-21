import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from unittest.mock import Mock, patch, MagicMock
from services.rank_utils import get_rank_by_players_id, determine_rank, is_team_winner

class TestGetRankByPlayersId(unittest.TestCase):

    @patch('services.rank_utils.Player')
    def test_get_players_rank_by_id_empty_string(self, MockPlayer):

        mock_filter_by = MockPlayer.filter_by
        mock_filter_by.return_value = []

        team = []

        team_ranking_points = get_rank_by_players_id(team)

        self.assertIsNone(team_ranking_points)
        mock_filter_by.assert_not_called()

    @patch('services.rank_utils.Player')
    def test_get_players_rank_by_id_missing_players(self, MockPlayer):

        mock_filter_by = MockPlayer.query.filter_by.return_value
        mock_filter_by.first.side_effect = [MagicMock(points=10), None, MagicMock(points=30)]

        team = [1,2,3]

        team_ranking_points = get_rank_by_players_id(team)
        self.assertIsNone(team_ranking_points)

    @patch('services.rank_utils.Player')
    def test_get_players_rank_by_id_append_points(self, MockPlayer):

        mock_filter_by = MockPlayer.query.filter_by.return_value
        mock_filter_by.first.side_effect = [MagicMock(points=10), MagicMock(points=10), MagicMock(points=30)]

        team = [1,2,3]

        team_ranking_points = get_rank_by_players_id(team)
        self.assertEqual(team_ranking_points, [10, 10, 30], "Points appended.")

class TestDetermineRank(unittest.TestCase):
    def test_determine_rank_negative_rank(self):
        rank = determine_rank(-100)

        self.assertEqual(rank, "Iron")

    def test_determine_rank_high_rank(self):
        rank = determine_rank(1000)

        self.assertEqual(rank, "Gold")
    
    def test_determine_rank_str(self):
        rank = determine_rank("")

        self.assertIsNone(rank)

    def test_determine_rank_false_value(self):
        rank = determine_rank(None)

        self.assertIsNone(rank)
    
class TestTeamWinner(unittest.TestCase):
    def test_is_team_winner_win(self):
        winner_team_id = 1
        team_id = 1
        result = is_team_winner(winner_team_id, team_id)

        self.assertEqual(result, "W")

    def test_is_team_winner_tie(self):
        winner_team_id = None
        team_id = 1
        result = is_team_winner(winner_team_id, team_id)

        self.assertEqual(result, "Tie")

    def test_is_team_winner_lost(self):
        winner_team_id = 2
        team_id = 1
        result = is_team_winner(winner_team_id, team_id)

        self.assertEqual(result, "L")
    
    def test_is_team_winner_empty_str(self):
        winner_team_id = ""
        team_id = 1
        result = is_team_winner(winner_team_id, team_id)

        self.assertIsNone(result)
    
