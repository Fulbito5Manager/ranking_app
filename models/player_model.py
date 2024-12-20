from utils.db import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    # username = db.Column(db.String(10), unique=True)
    points = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.String(10), nullable=False)

    def __init__(self, id, points, rank):
        self.id = id
        # self.username = username
        self.points = points
        self.rank = rank

    def update_ranking(self, new_points):
        self.points += new_points