import requests
from settings import PLAYER_SERVICE_URL
from utils.db import db
from models.player_model import Player
from services.team_service import get_team_by_player
from services.ranking_service import calculate_player_ranking
from services.rank_utils import is_team_winner

# player_data = {
#         'id': 3,
#         'username': "user"
#     }

def get_player_by_id(player_id):
    
    # headers = {
    #     'Authorization': f'Bearer {jwt}'
    # }
    
    response = requests.get(f'{PLAYER_SERVICE_URL}api/jugadores/{player_id}')

    # headers = request.headers
    # if Security.verify_token(response.headers):
    #     return response.json()
    # return {"Error":"Invalid token"}, 401

    return response.json()

def is_player_indb(id):
    return Player.query.filter_by(id=id).first()

    
def create_new_player(id):
    starting_points = 50
    starting_rank = "Bronze"
    new_player = Player(id=id, points=starting_points, rank=starting_rank)
    return new_player

def add_player_to_db(new_player):

    try:
        db.session.add(new_player)
        db.session.commit() 
        
    except Exception as e:
        print("Could not add to DB:", e)
    
    finally:
        db.session.rollback()

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