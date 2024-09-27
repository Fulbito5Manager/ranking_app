from services.player_service import get_player_by_id

def calculate_ranking(player_data, winner_team_id, team1, team2):

    #INCLUDED FUNCTION REQUEST????

    if winner_team_id != None or winner_team_id != "1" or winner_team_id != "2":
        print('could not process current rank (falsy values)')
        return {'rank': "", 'points': ""} 

    if not player_data['points']: # ISSUE WITH WINNER complicated validation for NONE
        print('could not process current rank (falsy values)')
        return {'rank': "", 'points': ""} 
    
    # Don't bring negative values. Return 0
    player_data['points'] = 0 if player_data['points'] < 0 else player_data['points']

    total_player_per_team = len(team1['player_ids'])

    match_result = "W" if player_data['id'] in team1['player_ids'] and winner_team_id == team1['team_id'] else ("L" if winner_team_id == "1" else "Tie")

    rankings_team1 = get_rank_by_players_id(team1, player_data)
    rankings_team2 = get_rank_by_players_id(team2, player_data)

    points = get_ranking(rankings_team1, rankings_team2, match_result, total_player_per_team)

    # Added points to previous ones
    points = points + player_data['points']

    #try and except
    rank = determine_rank(points)

    return {'rank': rank, 'points': points}

def determine_rank(points):
    # Simplified rank determination logic // Needs modification
    if points > 150:
        return 'Gold'
    elif points > 100:
        return 'Silver'
    elif points > 50:
        return 'Bronze'
    else:
        return 'Iron'

def get_rank_by_players_id(team, player_data):
        team_ranking_points = []
        for player_id in team['player_ids']:
            if player_id == player_data['id']:
                team_ranking_points.append(player_data['points'])  # Use provided player_data for the specific player so mock data dont overwrite player_data
            else:
                other_player_data = get_player_by_id(player_id)  # Fetch data for other players
                team_ranking_points.append(other_player_data['points'])
        return team_ranking_points

def get_ranking(rankings_team1, rankings_team2, match_result, total_player_per_team):
    

    key_factor = 20
    # Key Factor == constant of performing speed
    points_per_division = 100 

    # EXAMPLE base points

    base_points = 1 if match_result == "W" else (0.5 if match_result == "Tie" else 0) 

    rating_A = sum(rankings_team1) / total_player_per_team
    rating_B = sum(rankings_team2)  / total_player_per_team

    rating_teams_diff = rating_B - rating_A

    expected = 1/ (1+10 **( rating_teams_diff/points_per_division ))

    points = round((base_points - expected) * key_factor)

    return points
    # points = player_data['points'] + key_factor * (base_points - expected) # logaritmic recommendation adjustment from ChatGPT