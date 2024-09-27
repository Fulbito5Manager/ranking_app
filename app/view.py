from flask import jsonify

def player_view(player):
    return jsonify({
        'player_id': player.player_id, #this might change to jugador_id
        'team_id': player.team_id,  #this might change to equipo_id
        'stats': player.stats 
        #'player_history': player.player_history' # or the histroy is include in "STATS"?
    })

def ranking_view(ranking):
    return jsonify({
        'player_id': ranking.player_id,
        'rank': ranking.rank,
        'points': ranking.points
    })

# def team_view(team):
#     return jsonify({
#         'team_id': team.team_id, 
#         'team_list': team.team_list
#     })