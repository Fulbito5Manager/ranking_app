from models.player_model import Player

def calculate_player_ranking(match_id):

    from services.team_service import get_teams_data_by_match_id
    from services.player_service import add_player_to_db, is_player_indb, create_new_player
    from services.match_service import get_winner_team_id_by_match_id
    from services.rank_utils import get_rank_by_players_id, determine_rank, is_team_winner

    #INCLUDED FUNCTION REQUEST????
    #VALIDATIONS

    # Don't bring negative values. Return 0

    winner_team_id = get_winner_team_id_by_match_id(match_id)
    team_a_data, team_b_data = get_teams_data_by_match_id(match_id)

    # team_a_list = get_teamplayers_by_team_id(team_a_data['id']) # LIST
    # team_b_list = get_teamplayers_by_team_id(team_b_data['id'])

    rankings_teamA = get_rank_by_players_id(team_a_data['jugadores']) # SHOUDL GIVE ME A LIST WITH POINTS
    rankings_teamB = get_rank_by_players_id(team_b_data['jugadores']) # [12, 51, 36, 25, 74]

    for team_id in [team_a_data['id'], team_b_data['id']]:

        team_list = get_teams_data_by_match_id(team_id) # LIST
        total_players_per_team = len(team_list)
        
        # points = get_ranking(rankings_team1, rankings_team2, match_result, total_player_per_team) # OLD 
        # Added points to previous ones

        for player_id in team_list:

            # match_result = "W" if player_data['id'] in team1['player_ids'] and winner_team_id == team1['team_id'] else ("L" if winner_team_id == "1" else "Tie")
            player_match_result = is_team_winner(winner_team_id, team_id)
            points = get_ranking(player_match_result, total_players_per_team, rankings_teamA, rankings_teamB)

            player_data = is_player_indb(player_id)
            if player_data is None:
                player_data = create_new_player(player_id)
                add_player_to_db(player_data)

            player_data.points = points + player_data.points
            #try and except
            rank = determine_rank(points)
            
            print("see if works:", points, rank)

            return {'rank': player_data.rank, 'points': player_data.points}

def get_ranking(match_result, total_player_per_team, rankings_teamA, rankings_teamB):

    key_factor = 20
    # Key Factor == constant of performing speed
    points_per_division = 100 

    # EXAMPLE base points

    base_points = 1 if match_result == "W" else (0.5 if match_result == "Tie" else 0) 

    rating_A = sum(rankings_teamA) / total_player_per_team
    rating_B = sum(rankings_teamB)  / total_player_per_team

    rating_teams_diff = rating_B - rating_A

    expected = 1/ (1+10 **( rating_teams_diff/points_per_division ))

    points = round((base_points - expected) * key_factor)

    return points
    # points = player_data['points'] + key_factor * (base_points - expected) # logaritmic recommendation adjustment from ChatGPT