import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from unittest.mock import Mock, patch, MagicMock
from services.rank_utils import get_rank_by_players_id

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
