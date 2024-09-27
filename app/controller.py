from flask import request, jsonify, blueprints, Blueprint
from services.ranking_service import calculate_ranking
import requests
from services.player_service import is_player_indb, create_new_player
from services.match_service import is_match_indb, bring_api_teams_by_match_id

ranking_controller = Blueprint('ranking_controller', __name__)

"""
Ideas: If we incorporate streak to it, it's covenient to have it as a property so it can be incoporated to the points as an argument
in that case we don't calculate the streak inside based on how many times on a row player won.

date.

"""

@ranking_controller.route('/rank/<int:player_id>/<int:match_id>', methods=['GET'])
def get_rank_by_match_id(match_id, player_id):

    found_match = is_match_indb(match_id)
    found_player = is_player_indb(player_id)

    if (found_player == False):
        found_player = create_new_player(player_id) # Give player default rank: Bronze and Bronze points.
        # player doesnt exist exection !!!!!! 

    team_A, team_B = bring_api_teams_by_match_id(match_id)
    winner_team = found_match.winner_team # equipoganadorID
    
    # List of players by team: calls for team_service

    if is_player_in_match(found_player.id, found_match.players_list):
        ranking_data = calculate_ranking(found_player, winner_team, team_A, team_B)

    # Check for player in player match list.
    def is_player_in_match(target_id, players_list):
        return target_id in players_list
    
    # ranking_data.date = found_match.date
    return jsonify(ranking_data)

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