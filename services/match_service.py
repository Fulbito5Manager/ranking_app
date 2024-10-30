import requests
from config import MATCH_SERVICE_URL
from models.match_model import Match
from utils.db import db
from services.team_service import get_team_by_id
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # You can change the level to DEBUG for more detailed logs
logger = logging.getLogger(__name__)

def get_matches(jwt):
    
    jwt =  retrieve_token() # llamar a token service // verlo por postman primero
    
    headers = {
        'Authorization': f'Bearer {jwt}'
    }
    
    response = requests.get(f'{MATCH_SERVICE_URL}/api/partidos', headers=headers)
    return response.json()

def retrieve_token():
    response = requests.post('/login', json={'username': '123', 'password': '123'})
    return response.json()['token']

def is_match_indb(id):
    return Match.query.filter_by(id=id).first()

def create_match(data):

    match_id = data.get('partido_id')
    print('match id with get:', match_id)

    existing_match = Match.query.get(match_id)

    if existing_match:
        logger.warning(f"Attempted to create a match with a duplicate ID: {match_id}")
        return None

    match_date = data.get('date')
    status = data.get('estado')
    # match.status = data.get('estado')  # e.g., 'Cancelled', 'Finished', etc.

    match = Match(id=match_id, date=match_date, winner_team=None, players_list=[], status=status)  # Create a new match record
    match.players_list = data.get('jugadores', [])
    match.winner_team = data.get('equipoganadorID')
    
    db.session.add(match)
    db.session.commit()

    return match

def get_winner_team_id_by_match_id(match_id = "",  jwt= ""):
    headers = {
        'Authorization': f'Bearer {jwt}'
    }

    print("it gets here and then stops.")
    
    response = requests.get(f'{MATCH_SERVICE_URL}/api/partidos/{match_id}', headers=headers)
    data = response.json()

    winner_team_id = data['equipoGanadorID']

    return winner_team_id


# def bring_api_teams_by_match_id():

#         # TEAM DATA

#         # api/equipos/{id}
#         # {
#         # "id":0,
#         # "tipo": "string",
#         # "partido.Id": 0,
#         # "jugadores": [0, 1, 2, 3]
#         # }
    
#         team_A = get_team_by_id(0)['players']
#         team_B = get_team_by_id(1)['players']
#         return team_A, team_B