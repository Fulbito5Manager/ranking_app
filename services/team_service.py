import requests, random
from settings import PLAYER_SERVICE_URL

def get_team_by_id(team_id, match_id = "",  jwt= ""):
    headers = {
        'Authorization': f'Bearer {jwt}'
    }
    
    response = requests.get(f'{PLAYER_SERVICE_URL}api/equipos/{team_id}', headers=headers)
    response.json()
    
    team_id = random.randint(1, 2)

    return team_id

def get_teams_data_by_match_id(match_id):
    response = requests.get(f'{PLAYER_SERVICE_URL}api/equipos/partido/{match_id}'); # headers=headers # team service url
    match_data = response.json()
    
    team_a_data = match_data[0];
    team_b_data = match_data[1];
    return team_a_data, team_b_data

def get_team_by_player(player, match_id):

    team_a_data, team_b_data = get_teams_data_by_match_id(match_id)
    player_team = team_a_data['id'] if (player.id in team_a_data['id']) else team_b_data['id']

    return player_team

def get_teamplayers_by_team_id(team_id):
    response = requests.get(f'{PLAYER_SERVICE_URL}api/equipos/{team_id}'); # headers=headers
    data = response.json()

    player_list = data.get('jugadores', [])

    return player_list