from flask import request
from app.model import Player, Ranking, Team
from app.view import player_view, ranking_view
from services.player_service import get_player_data
from services.ranking_service import calculate_ranking
from services.team_service import get_team_data

def handle_event(event_data):
    player_data = get_player_data(event_data['player_id'], event_data['jwt'])

    team1_data = get_team_data(event_data['team_id'], event_data['jwt'])
    team2_data = get_team_data(event_data['team_id'], event_data['jwt'])
    
    team1 = Team(team1_data['id'], team1_data['jugadores'])
    team2 = Team(team1_data['id'], team1_data['jugadores'])

    ranking_data = calculate_ranking(player_data, event_data['winner_team_id'], team1, team2) # add team_data
    # matches_history = Matches_history(event_data['match_date'], event_data['result']) # also to compare teams I need a team list from both teams

    player = Player(event_data['player_id'], player_data) # add team_data or add team model
    ranking = Ranking(event_data['player_id'], ranking_data['rank'], ranking_data['points'])

    return player_view(player), ranking_view(ranking)

# {
#     "id":0,
#     "tipo": "string",
#     "partidoId": 0,
#     "jugadores": [0, 1, 2, 3]
# }