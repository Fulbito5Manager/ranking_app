from services.player_service import get_player_data

def calculate_ranking(player_id, winner_team_id, team1, team2):  # Do I need player_data? 
    # Placeholder for the ranking calculation logic
    teams_data = [team1, team2]

    rankings_team1 = get_rank_by_players_id(team1)
    rankings_team2 = get_rank_by_players_id(team2)

    match_result = "W" if player_id['id'] in team1['player_ids'] and winner_team_id == team1['team_id'] else "L"

    key_factor = 35
    # key factor == constant of performing speed
    points_per_division = 50 

    base_points = 10 if match_result == "W" else -10 # EXAMPLE base points

    rating_A = sum(rankings_team1)
    rating_B = sum(rankings_team2)

    rating_teams_diff = rating_A - rating_B

    expected = 1/ (1+10^( rating_teams_diff/points_per_division ))

    points = (base_points + expected) * key_factor

    rank = determine_rank(points)
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

def get_rank_by_players_id(team):
    team_rankings = []
    for player_id in team['players_id']:
        player_data = get_player_data(player_id) # and jwt?
        team_rankings.append(player_data['ranking'])
    return team_rankings