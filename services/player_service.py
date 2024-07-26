import requests
from config import PLAYER_SERVICE_URL

def get_player_data(player_id, jwt):
    
    # jwt =  retrieve_token() # llamar a token service // verlo por postman primero
    
    headers = {
        'Authorization': f'Bearer {jwt}'
    }
    
    response = requests.get(f'{PLAYER_SERVICE_URL}/jugador/{player_id}', headers=headers)
    return response.json()

