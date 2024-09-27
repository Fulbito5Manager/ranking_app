import requests
from config import PLAYER_SERVICE_URL
from models.player_model import Player

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

def create_new_player(id):
    starting_points = 50
    starting_rank = "Bronze"
    new_player = Player(id=id, points=starting_points, rank=starting_rank)
    return new_player