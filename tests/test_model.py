import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.model import Ranking

class TestRanking(unittest.TestCase):

        def test_update_ranking(self):
                ranking = Ranking(player_id='123', rank='Bronze', points=10)
                ranking.update_ranking(10)
                self.assertEqual(ranking.points, 24)
                print(f"Player ID: {ranking.player_id}, Points: {ranking.points}")

if __name__ == '__main__':
        unittest.main()

#CHAT GPT ADVICE 
# TO INTEGRATE: 
# pip install pytest
# pytest

# OLD TEST FILE -------------------------

# from app.model import Ranking

# def test_update_ranking(self):
#         ranking = Ranking(player_id='123', rank='Bronze', points=0)
#         ranking.update_ranking(10)
#         self.assertEqual(ranking.points, 10)

