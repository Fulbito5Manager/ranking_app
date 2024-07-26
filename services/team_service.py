import requests
from config import PLAYER_SERVICE_URL

def get_team_data(team_id, jwt):
    headers = {
        'Authorization': f'Bearer {jwt}'
    }
    
    response = requests.get(f'{PLAYER_SERVICE_URL}/equipos/{team_id}', headers=headers)
    return response.json()