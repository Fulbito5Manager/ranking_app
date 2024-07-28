from services.player_service import get_player_data

def calculate_ranking(player_data, winner_team_id, team1, team2):  # Do I need player_data? 
    # Placeholder for the ranking calculation logic
    teams_data = [team1, team2]

    def get_rank_by_players_id(team):
        team_ranking_points = []
        for player_id in team['player_ids']:
            if player_id == player_data['id']:
                team_ranking_points.append(player_data['points'])  # Use provided player_data for the specific player
            else:
                other_player_data = get_player_data(player_id)  # Fetch data for other players
                team_ranking_points.append(other_player_data['points'])
        return team_ranking_points

    rankings_team1 = get_rank_by_players_id(team1)
    rankings_team2 = get_rank_by_players_id(team2)

    match_result = "W" if player_data['id'] in team1['player_ids'] and winner_team_id == team1['team_id'] else "L"

    key_factor = 12
    # key factor == constant of performing speed
    points_per_division = 100 

    base_points = 1 if match_result == "W" else (0.5 if match_result == "Tie" else 0) # EXAMPLE base points

    rating_A = sum(rankings_team1) / int(len(team1['player_ids']))
    # breakpoint()
    rating_B = sum(rankings_team2)  / int(len(team2['player_ids']))

    rating_teams_diff = rating_B - rating_A

    expected = 1/ (1+10 **( rating_teams_diff/points_per_division )) # 0.613

    # points = (base_points + expected) * key_factor
    points = player_data['points'] + key_factor * (base_points - expected) # logaritmic recommendation adjustment from ChatGPT
    

    rank = determine_rank(points + player_data['points'])
    # points = points + player_data['points']

    return {'rank': rank, 'points': points}

def determine_rank(points):
    # Simplified rank determination logic
    if points > 150:
        return 'Gold'
    elif points > 100:
        return 'Silver'
    elif points > 50:
        return 'Bronze'
    else:
        return 'Iron'

# def get_rank_by_players_id(team):
#     team_ranking_points = []
#     for player_id in team['player_ids']:
#         player_data = get_player_data(player_id) # and jwt?
#         # breakpoint()
#         team_ranking_points.append(player_data['points'])
#     return team_ranking_points

