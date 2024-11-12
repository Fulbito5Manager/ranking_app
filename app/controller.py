from flask import Blueprint, jsonify
from services.ranking_service import calculate_player_ranking
from services.player_service import is_player_indb, create_new_player, add_player_to_db
from services.match_service import is_match_indb

ranking_controller = Blueprint('ranking_controller', __name__)

"""
Ideas: If we incorporate streak to it, it's covenient to have it as a property so it can be incoporated to the points as an argument
in that case we don't calculate the streak inside based on how many times on a row player won.

date.

"""

@ranking_controller.route('/api/ranking/<int:player_id>', methods=['GET']) # ID or User, whatever
def get_rank_by_id(player_id):
    found_player = is_player_indb(player_id)
    if found_player:
        return {"rank": found_player.points, "points": found_player.points}
    return {"error": "Player not found."}

@ranking_controller.route('/api/test-db/<int:player_id>', methods=['POST'])
def test_db(player_id):
    try:
        player = create_new_player(player_id)
        add_player_to_db(player)

        return jsonify({
            'status': 'success',
            'id': player.id,
            'points': player.points
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
"""
# MATCH DATA

# api/partido/ids
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