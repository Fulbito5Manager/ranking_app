from flask import request, jsonify, blueprints, Blueprint
from services.ranking_service import calculate_player_ranking
import requests
from services.player_service import is_player_indb, create_new_player
from services.match_service import is_match_indb

ranking_controller = Blueprint('ranking_controller', __name__)

"""
Ideas: If we incorporate streak to it, it's covenient to have it as a property so it can be incoporated to the points as an argument
in that case we don't calculate the streak inside based on how many times on a row player won.

date.

"""

@ranking_controller.route('/rank/<int:match_id>', methods=['GET'])
def get_rank_by_match_id(match_id, player_id):

    # I could add points gained based on match id.

    return 

# This should birng player's rank based on all matches that player had

#  TOO MUCH RESPONSABILITY  ONLY GIVES BASIC INFO : RANK AND POINTS.
@ranking_controller.route('/rank/<int:player_id>', methods=['GET']) # ID or User, whatever
def get_rank_by_id(player_id):

    found_player = is_player_indb(player_id)

    return {"rank": found_player.points, "points": found_player.points}
    
    # MATCH DATA

    # Here we have an issue, how do I know whats the match they played?
    # Im considering adding a service dad UPDATES matches. So if there are missing matches it will update player stasts
    # UPDATE will check if num of matches player participated = matches recorded in database 
    # We compare if (=) do nothing else UPDATE
    # UPDATE brings all matches from API.Partidos with the filtered ID.

def getToken():
    response = requests.post('http://127.0.0.1:5000/login', json={'username': 'pet1', 'password': '123'})
    return response.json()['token']

"""
# MATCH DATA

# api/partido/id
# {
#   match_id
#   date
#   canchaID
#   estado
#   equipoganadorID: 0 - 1
    jugadores ? NO
# }

# PLAYER DATA

# api/player/id
#   {
#    'id': 3,
#    'username': "user"
#   }

# TEAM DATA

# api/equipos/{id}
# {
#   "id":0,
#   "tipo": "string",
#   "partido.Id": 0,
#   "jugadores": [0, 1, 2, 3]
# }

"""