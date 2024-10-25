from utils.db import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    winner_team = db.Column(db.String(5))
    date = db.Column(db.Integer)
    # players_list = db.Column(db.JSON)
    status = db.Column(db.String(20), nullable=False)

    def __init__(self, id, winner_team, date, players_list, status):
        self.id = id
        self.winner_team = winner_team 
        self.date = date
        # self.players_list = players_list
        self.status = status

    # @classmethod
    # def filter_by_player(cls, player_id):
    #     # Query the database to find all matches that include the specific player
    #     return cls.query.filter(Match.players_list.contains([player_id])).all()
