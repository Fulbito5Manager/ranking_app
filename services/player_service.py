import requests
from config import PLAYER_SERVICE_URL
from utils.db import db
from models.player_model import Player
from services.team_service import get_team_by_player
from services.ranking_service import calculate_player_ranking
from services.rank_utils import is_team_winner

def get_player_by_id(player_id):
    
    jwt =  retrieve_token() # llamar a token service // verlo por postman primero
    
    headers = {
        'Authorization': f'Bearer {jwt}'
    }
    
    response = requests.get(f'{PLAYER_SERVICE_URL}api/jugadores/{player_id}', headers=headers)

    # player_data = {
    #         'id': 3,
    #         'username': "user"
    #     }

    return response.json()

def retrieve_token():
    response = requests.post('/login', json={'username': 'pet1', 'password': '123'})
    return response.json()['token']

def is_player_indb(id):
    return Player.query.filter_by(id=id).first()

# HANDLE NEW PLAYERS AND OLD PLAYERS

def bring_old_and_new_players(data):

    new_players, old_players = [], [] 

    try:
        # Fetch the current list of players from the match
        incoming_players = data.get('jugadores', [])  # This should already be a list of player IDs
        if not incoming_players:
            incoming_players = []
        print("Incoming players:", incoming_players)

        # Fetch all players in the database
        players_in_db = Player.query.all()  # Assuming Player model exists
        players_in_db_ids = [player.id for player in players_in_db]  # Extract player IDs

        # Determine new and old players
        new_players = [p for p in incoming_players if p not in players_in_db_ids]
        old_players = [p for p in incoming_players if p in players_in_db_ids]

        print("New players:", new_players)
        print("Old players:", old_players)

        return new_players, old_players

    except Exception as e:
        print(f"Error handling players: {str(e)}")
        return [], []
    
def create_new_player(id):
    starting_points = 50
    starting_rank = "Bronze"
    new_player = Player(id=id, points=starting_points, rank=starting_rank)
    return new_player

def add_player_to_db(new_player):

    try:
        # Add the player to the database
        db.session.add(new_player)
        db.session.commit() 
        
    except Exception as e:
    # Create a new player object
        print("Could not add to DB:", e)
    
    finally:
        db.session.rollback()

    # # You don't need to query again if the object is the one you just created
    # print(f"New player ID without query (after commit): {new_player.id}")
    # # return new_player

# Update and handle new players
# def handle_new_players(new_players, winner_team_id, match_id):
#     for player_id in new_players:
#         # should I add player at the end so as to avoid any issues? Or I could just trow a rollback  in case of something happened?
#         print(f"Processing player ID: {player_id}")

#         if not winner_team_id:
#             winner_team_id = False

#         add_player_to_db(player_id)

#         # However, you can query the player again if you want to ensure retrieval from the DB
#         player = Player.query.filter_by(id=player_id).first()
#         if player:
#             print(f"Player ID with query: {player.id}")
#         else:
#             print(f"Player with ID {player_id} not found in the database.")

#         # Assuming `get_team_by_player` uses the player object
#         player_team = get_team_by_player(player, match_id)

#         match_result = is_team_winner(winner_team_id, player_team);

#         return match_result, players
        # concluded_player_rank = calculate_player_ranking(player, match_result)

        # print(concluded_player_rank)

        # new_player = Player(id=concluded_player_rank['id'], name=concluded_player_rank['name'], 
        #                     team=concluded_player_rank['points'], rank=concluded_player_rank['rank'])
        
def update_old_players(old_players):
    
    for player in old_players:

        # team = get_team_by_player(player)

        existing_player = Player.query.get(player['id'])
        existing_player.team = player['team']
        db.session.commit()

def process_ranking(players, match_id, match_result):

    for player in players:
        player_data = is_player_indb(player.id)
    return