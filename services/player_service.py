from utils.db import db
from models.player_model import Player

# player_data = {
#         'id': 3,
#         'username': "user"
#     }

# def get_player_by_id(player_id):
    
#     response = requests.get(f'{PLAYER_SERVICE_URL}api/jugadores/{player_id}')

#     return response.json()

def is_player_indb(id):
    return Player.query.filter_by(id=id).first()

class PlayerLimitReachedException(Exception):
    pass
    
def create_new_player(id):

    limit = 50

    try:
        if id <= limit:
            starting_points = 50
            starting_rank = "Bronze"
            new_player = Player(id=id, points=starting_points, rank=starting_rank)
            return new_player
        else:
            raise PlayerLimitReachedException("Reached limit amount of players allowed.")
    except Exception as e:
        print("Failed to instance player: ", e)
        return None

def add_player_to_db(new_player):
    try:
        db.session.add(new_player)
        db.session.commit() 
        
    except Exception as e:
        db.session.rollback()
        print("Could not add to DB:", e)


# HANDLE NEW PLAYERS AND OLD PLAYERS

# def bring_old_and_new_players(data):

#     new_players, old_players = [], [] 

#     try:
#         # Fetch the current list of players from the match
#         incoming_players = data.get('jugadores', [])  # This should already be a list of player IDs
#         if not incoming_players:
#             incoming_players = []
#         print("Incoming players:", incoming_players)

#         # Fetch all players in the database
#         players_in_db = Player.query.all() 
#         players_in_db_ids = [player.id for player in players_in_db]  # Extract player IDs

#         # Determine new and old players
#         new_players = [p for p in incoming_players if p not in players_in_db_ids]
#         old_players = [p for p in incoming_players if p in players_in_db_ids]

#         print("New players:", new_players)
#         print("Old players:", old_players)

#         return new_players, old_players

#     except Exception as e:
#         print(f"Error handling players: {str(e)}")
#         return [], []
